#!/usr/bin/env python3
"""Recover private book evidence, editorial notes and author comments locally.

The contentless FTS index stores terms and pointers, not a second plain-text
corpus. Source documents and the existing extraction database remain canonical.
An indexed model claim remains unreviewed; indexing never changes reading levels.
"""
from __future__ import annotations
import argparse
from collections import Counter
from datetime import datetime,timezone
from functools import lru_cache
import hashlib,importlib.util,io,json,os,re,sqlite3,sys,uuid
from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
NOTES=ROOT/'_notes'
BASE=NOTES/'10-biblioteca/contesto'
DB=NOTES/'99-cache/contesto-libro/indice.sqlite'
CORPUS=NOTES/'10-biblioteca/lettura-locale/corpus.sqlite'
spec=importlib.util.spec_from_file_location('book_context_storage',Path(__file__).with_name('cache-storage.py'))
storage=importlib.util.module_from_spec(spec);spec.loader.exec_module(storage)
NAMESPACE={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
W='{'+NAMESPACE['w']+'}'
SCOPES={'reviewed':{'reading-note','editorial-map'},'automatic':{'model-card'},'raw':{'extracted-unit'},'author':{'author-paragraph','author-comment','author-revision'},'all':None}
SYNONYMS={'tritono':['tritone'],'tritone':['tritono'],'dominante':['dominant'],'dominant':['dominante'],'rivolto':['inversion'],'inversion':['rivolto'],'condotta':['voice leading'],'diteggiatura':['fingering']}

def digest(data):return hashlib.sha256(data).hexdigest()
def relative(path):return path.relative_to(ROOT).as_posix()
def private_path(value):
    path=(ROOT/value).resolve()
    if not path.is_relative_to(NOTES.resolve()) and not path.is_relative_to((ROOT/'manuscript').resolve()):raise ValueError('Context path must remain inside private project content')
    return path
def json_read(path):
    actual=storage.cache_variant(path)
    if actual is None:raise FileNotFoundError(str(path))
    with storage.open_text(actual) as stream:return json.load(stream)
def readonly(path):
    con=sqlite3.connect(path.resolve().as_uri()+'?mode=ro',uri=True,timeout=60);con.execute('PRAGMA query_only=ON');return con
def logical(path):return Path(str(path).removesuffix('.gz').removesuffix('.xz').removesuffix('.bz2'))

def docx_parts(path_string,expected_hash):
    path=private_path(path_string);raw=path.read_bytes()
    if digest(raw)!=expected_hash:raise ValueError('Author document changed; rebuild the context index')
    return _docx_parts_cached(path_string,expected_hash,raw)

@lru_cache(maxsize=8)
def _docx_parts_cached(path_string,expected_hash,raw):
    path=private_path(path_string)
    result=[]
    with ZipFile(io.BytesIO(raw)) as doc:
        if sum(v.file_size for v in doc.infolist())>256*1024*1024:raise ValueError('DOCX exceeds the bounded XML reader size')
        paragraphs=[];anchors={};range_started=set();range_ended=set()
        for name in sorted(doc.namelist()):
            if not re.fullmatch(r'word/(?:document|footnotes|endnotes|header\d+|footer\d+)\.xml',name):continue
            root=ET.fromstring(doc.read(name))
            active=set()
            for number,p in enumerate(root.iter(W+'p'),1):
                current=''.join(x.text or '' for x in p.iter(W+'t'))
                # Keep deleted text in separate records instead of accepting revisions.
                if current.strip():paragraphs.append(dict(key=f'{name}:p{number}',kind='author-paragraph',title=path.name,locator=f'{name}, paragrafo {number}',text=current,component=name,paragraph=number))
                selected={cid:[] for cid in active};references=set()
                for node in p.iter():
                    cid=node.get(W+'id')
                    if node.tag==W+'commentRangeStart':active.add(cid);selected.setdefault(cid,[]);range_started.add(cid)
                    elif node.tag==W+'commentRangeEnd':active.discard(cid);selected.setdefault(cid,[]);range_ended.add(cid)
                    elif node.tag==W+'commentReference':references.add(cid)
                    elif node.tag in {W+'t',W+'delText'}:
                        for current_id in active:selected.setdefault(current_id,[]).append(node.text or '')
                for cid in set(selected)|references:
                    anchors.setdefault(cid,[]).append(dict(component=name,paragraph=number,context=current,selected_text=''.join(selected.get(cid,[]))))
                for k,tag in [('inserted',W+'ins'),('deleted',W+'del'),('moved-from',W+'moveFrom'),('moved-to',W+'moveTo')]:
                    for ri,node in enumerate(p.iter(tag),1):
                        text=''.join(v.text or '' for v in node.iter() if v.tag in {W+'t',W+'delText'})
                        if text.strip():result.append(dict(key=f'{name}:p{number}:{k}{ri}',kind='author-revision',title=path.name,locator=f'{name}, paragrafo {number}, {k} {ri}',text=text,revision_kind=k,component=name,paragraph=number))
        result=paragraphs+result
        if 'word/comments.xml' in doc.namelist():
            for node in ET.fromstring(doc.read('word/comments.xml')).iter(W+'comment'):
                cid=node.get(W+'id');text='\n'.join(''.join(v.text or '' for v in p.iter(W+'t')) for p in node.iter(W+'p'))
                attached=anchors.get(cid,[])
                result.append(dict(key='comment:'+str(cid),kind='author-comment',title=path.name+'; commento '+str(cid),locator='word/comments.xml, commento '+str(cid),text=text+'\n\nContesto nel documento:\n'+'\n'.join(v['context'] for v in attached),comment_id=cid,anchors=attached,anchor_found=bool(attached),range_is_complete=cid in range_started and cid in range_ended))
    return result

docx_parts.cache_clear=_docx_parts_cached.cache_clear

def model_text(output):
    card=output['card'];lines=list(card.get('topics',[]))
    for group in ['claims','terms','relations','references']:
        for item in card.get(group,[]):lines.append(' '.join(str(item.get(k,'')) for k in ['statement','from','relation','to','unit','evidence']))
    return '\n'.join(lines+card.get('limitations',[]))

@lru_cache(maxsize=1)
def citation_records():
    return json_read(NOTES/'book-bib-registry.json'),json_read(NOTES/'10-biblioteca/letture.json')['records']

def build(db=DB):
    db=private_path(str(db));db.parent.mkdir(parents=True,exist_ok=True);temp=db.with_name(db.name+'.'+uuid.uuid4().hex+'.building')
    reg=json_read(NOTES/'book-bib-registry.json');ledger=json_read(NOTES/'10-biblioteca/letture.json')['records']
    reviews=json_read(BASE/'revisioni.json') if storage.cache_variant(BASE/'revisioni.json') else {}
    corpus=readonly(CORPUS);corpus.execute('BEGIN')
    sources={sid:json.loads(data) for sid,data in corpus.execute('SELECT source_id,data FROM sources')}
    aliases={};file_records={};reading_paths=set()
    for rid,row in reg.items():
        for key in [row.get('citekey'),*row.get('citekey_aliases',[])]:
            if key:aliases.setdefault(key,set()).add(rid)
        row=ledger[rid]
        for event in row.get('reading_events',[]):
            path=event.get('digest')
            if path:reading_paths.add(path);file_records.setdefault(path,set()).add(rid)
        for field in ['digest','editorial_usage_map','retrieval_catalog','edition_frontier']:
            path=row.get(field)
            if isinstance(path,str):file_records.setdefault(path,set()).add(rid)
    counts=Counter();issues=[];excluded=[];expected={};docx_files=[];model_groups=Counter()
    con=sqlite3.connect(temp)
    con.executescript("""PRAGMA journal_mode=DELETE; PRAGMA synchronous=FULL;
    CREATE TABLE documents(id INTEGER PRIMARY KEY,kind TEXT NOT NULL,title TEXT NOT NULL,locator TEXT NOT NULL,source_ref TEXT NOT NULL,source_sha256 TEXT NOT NULL,record_ids TEXT NOT NULL,review_status TEXT NOT NULL,details TEXT NOT NULL);
    CREATE VIRTUAL TABLE search USING fts5(text,content='',tokenize='unicode61 remove_diacritics 2');
    CREATE TABLE meta(key TEXT PRIMARY KEY,value TEXT NOT NULL);
    CREATE INDEX document_kind ON documents(kind);
    """)
    def records_for(path):
        result=set(file_records.get(path,()))
        name=Path(path).name
        for key,rids in aliases.items():
            if name.startswith(key+'-') or name==key+'.md':result.update(rids)
        return sorted(result)
    def add(kind,title,locator,ref,checksum,text,records=(),status='unreviewed',details=None):
        if not isinstance(text,str):raise ValueError('Index text must be a string')
        cur=con.execute('INSERT INTO documents(kind,title,locator,source_ref,source_sha256,record_ids,review_status,details) VALUES(?,?,?,?,?,?,?,?)',(kind,title,locator,json.dumps(ref,ensure_ascii=False),checksum,json.dumps(sorted(set(records))),status,json.dumps(details or {},ensure_ascii=False,separators=(',',':'))))
        con.execute('INSERT INTO search(rowid,text) VALUES(?,?)',(cur.lastrowid,title+'\n'+locator+'\n'+text));counts[kind]+=1
    for rid,row in reg.items():
        add('source-record',row.get('title') or row.get('citekey') or rid,'Registro bibliografico e attestazione corrente',{'registry':rid},digest(json.dumps([row,ledger[rid]],ensure_ascii=False,sort_keys=True).encode()),json.dumps([row,ledger[rid]],ensure_ascii=False),[rid],'metadata-only',dict(citekey=row.get('citekey'),bib_status=row['bib_status'],reading_closed=bool(ledger[rid]['lettura_integrale_chiusa'])))
    expected['source-record']=len(reg)
    for uid,sid,unit,text,metadata in corpus.execute('SELECT id,source_id,unit_id,text,metadata FROM units ORDER BY id'):
        src=sources[sid]['source'];records=src.get('record_ids',[]);meta=json.loads(metadata)
        add('extracted-unit',src['relative_path'],unit,{'unit_row':uid,'source_id':sid,'unit_id':unit},digest(text.encode()),text,records,'extraction-not-reading',meta)
    expected['extracted-unit']=corpus.execute('SELECT count(*) FROM units').fetchone()[0]
    states=dict(corpus.execute('SELECT state,count(*) FROM chunks GROUP BY state'))
    for chunk,sid,state,path in corpus.execute('SELECT chunk_id,source_id,state,output FROM chunks WHERE output IS NOT NULL ORDER BY source_id,ordinal'):
        try:
            actual=storage.cache_variant(private_path(path))
            if actual is None:raise FileNotFoundError(path)
            with storage.open_text(actual) as stream:raw=stream.read()
            output=json.loads(raw)
            if output['chunk_id']!=chunk or output['source_sha256']!=sid:raise ValueError('Model output provenance mismatch')
            card=output['card'];src=sources[sid]['source'];records=src.get('record_ids',[])
            details=dict(chunk_id=chunk,state=state,validation_errors=output.get('validation_errors',[]),topics=card.get('topics',[]),item_counts={k:len(card.get(k,[])) for k in ['claims','terms','relations','references']})
            review=reviews.get(chunk)
            if review:
                if review['card_sha256']!=digest(raw.encode()):raise ValueError('Reviewed model card changed')
                with storage.open_text(private_path(review['note'])) as stream:review_text=stream.read()
                if digest(review_text.encode())!=review['note_sha256']:raise ValueError('Semantic review note changed')
                details['semantic_review']=review
            model_groups.update(details['item_counts'])
            add('model-card',src['relative_path']+'; '+', '.join(card.get('topics',[])[:4]),', '.join(card.get('covered_units',[])),{'path':relative(actual)},digest(raw.encode()),model_text(output),records,'automatic-needs-review' if review or state!='grounded-unreviewed' else 'automatic-unreviewed',details)
        except (OSError,ValueError,KeyError,TypeError) as e:issues.append(dict(kind='model-card',reference=path,error=str(e)))
    expected['model-card']=corpus.execute('SELECT count(*) FROM chunks WHERE output IS NOT NULL').fetchone()[0]
    seen=set()
    for path in sorted(NOTES.rglob('*')):
        if not path.is_file():continue
        rel=relative(path);parts=path.relative_to(NOTES).parts
        if parts[0] in {'80-strumenti','99-cache'} or path.is_relative_to(BASE):continue
        if parts[:3]==('10-biblioteca','lettura-locale','schede'):continue  # Same material is indexed as structured model cards.
        if path.is_relative_to(NOTES/'10-biblioteca/lettura-locale') and 'ripresa-gpu-' in rel:continue
        lp=logical(path)
        if lp.suffix.lower()!='.md':continue
        if str(lp) in seen:continue
        seen.add(str(lp));actual=storage.cache_variant(lp)
        if actual is None:raise FileNotFoundError(rel)
        try:
            with storage.open_text(actual) as stream:text=stream.read()
            ishistory=parts[0]=='90-archivio' or '_backup' in parts
            records=records_for(relative(lp));kind='historical-note' if ishistory else 'reading-note' if relative(lp) in reading_paths or parts[:2]==('10-biblioteca','digest') else 'editorial-map' if lp.name.startswith('USO-EDITORIALE-') else 'project-note'
            title=next((v.lstrip('# ').strip() for v in text.splitlines() if v.startswith('# ')),lp.stem)
            add(kind,title,relative(lp),{'path':relative(actual)},digest(text.encode()),text,records,'historical' if ishistory else 'authored-note',dict(uses=[v.strip() for v in text.split('\n\n') if v.startswith('Uso ')]))
        except (OSError,UnicodeError,ValueError) as e:issues.append(dict(kind='note',reference=rel,error=str(e)))
    for path in sorted((NOTES/'40-libro').rglob('*.docx')):
        rel=relative(path);h=digest(path.read_bytes())
        try:
            rows=docx_parts(rel,h);hist='_backup' in path.parts
            for item in rows:
                details={k:v for k,v in item.items() if k not in {'key','text','kind','title','locator'}};details['historical']=hist
                add(item['kind'],item['title'],item['locator'],{'docx':rel,'part_key':item['key']},h,item['text'],status='historical-author-input' if hist else 'author-input-unreviewed',details=details)
            docx_files.append(dict(path=rel,sha256=h,parts=len(rows),comments=sum(v['kind']=='author-comment' for v in rows),revisions=sum(v['kind']=='author-revision' for v in rows),historical=hist))
        except (OSError,ValueError,ET.ParseError) as e:issues.append(dict(kind='docx',reference=rel,error=str(e)))
    for path in sorted((ROOT/'manuscript').rglob('*')):
        if path.is_file() and path.suffix in {'.md','.tex','.ly','.lytex','.bib'}:
            text=path.read_text(encoding='utf-8-sig');add('manuscript',path.name,relative(path),{'path':relative(path)},digest(text.encode()),text,status='existing-manuscript')
    missing=[rid for rid in reg if rid not in ledger];assert not missing
    for kind,number in expected.items():
        if counts[kind]!=number:issues.append(dict(kind=kind,error='Coverage mismatch',expected=number,indexed=counts[kind]))
    info=dict(schema='book-context-1',generated_utc=datetime.now(timezone.utc).isoformat(),counts=dict(counts),expected=expected,model_chunk_states=states,model_items=dict(model_groups),registered_sources=len(reg),prepared_sources=len(sources),closed_readings=sum(bool(v['lettura_integrale_chiusa']) for v in ledger.values()),docx_files=docx_files,issues=issues,all_indexable_inputs_covered=not issues,reading_levels_changed=False,automatic_claims_reviewed=False,method='Contentless local FTS5 over semantic cards, notes, author input and existing extracted units; no vector similarity claim',authoritative_raw_database=relative(CORPUS),not_indexed_as_semantic_content=['Executables, temporary caches and operating telemetry','Binary original PDFs/audio/video: records and extracted units remain the entry points','Compressed historical archives: retained in place; no new extraction or reading attested'],source_record_policy='Every registered source remains visible, including unavailable or unread sources',plain_text_corpus_copied=False)
    con.execute('INSERT INTO meta VALUES(?,?)',('manifest',json.dumps(info,ensure_ascii=False,separators=(',',':'))));con.commit();con.execute("INSERT INTO search(search) VALUES('optimize')");con.commit();con.execute('VACUUM');assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok';con.close();corpus.close()
    if issues:
        storage.write_cached_text(BASE/'incompleto.json',json.dumps(info,ensure_ascii=False)+'\n');temp.unlink();raise ValueError('Incomplete context index; inspect its private coverage report')
    os.replace(temp,db);info['index_bytes']=db.stat().st_size
    storage.write_cached_text(BASE/'copertura.json',json.dumps(info,ensure_ascii=False,separators=(',',':'))+'\n')
    return info

def query_expression(query):
    words=re.findall(r'\w+',query,flags=re.UNICODE)
    if not words:raise ValueError('Empty query')
    def quoted(value):return '"'+value.replace('"','""')+'"'
    return ' AND '.join('('+ ' OR '.join(quoted(v) for v in [word,*SYNONYMS.get(word.casefold(),[])])+')' for word in words)

def recover(row):
    kind,title,locator,ref,h,records,status,details=row;ref=json.loads(ref);details=json.loads(details)
    review=details.get('semantic_review')
    if review:
        with storage.open_text(private_path(review['note'])) as stream:review_text=stream.read()
        if digest(review_text.encode())!=review['note_sha256']:raise ValueError('Semantic review changed; rebuild context index')
    if 'unit_row' in ref:
        with readonly(CORPUS) as raw:v=raw.execute('SELECT source_id,unit_id,text FROM units WHERE id=?',(ref['unit_row'],)).fetchone()
        if v is None or v[:2]!=(ref['source_id'],ref['unit_id']) or digest(v[2].encode())!=h:raise ValueError('Extraction changed; rebuild context index')
        text=v[2]
    elif 'registry' in ref:
        rid=ref['registry'];r=json_read(NOTES/'book-bib-registry.json')[rid];l=json_read(NOTES/'10-biblioteca/letture.json')['records'][rid];text=json.dumps([r,l],ensure_ascii=False)
        if digest(json.dumps([r,l],ensure_ascii=False,sort_keys=True).encode())!=h:raise ValueError('Reading record changed; rebuild context index')
    elif 'docx' in ref:
        match=[v for v in docx_parts(ref['docx'],h) if v['key']==ref['part_key']]
        if len(match)!=1:raise ValueError('Missing author paragraph or comment')
        text=match[0]['text']
    else:
        path=private_path(ref['path'])
        with storage.open_text(path) as stream:text=stream.read()
        if digest(text.encode())!=h:raise ValueError('Document changed; rebuild context index')
        if kind=='model-card':
            output=json.loads(text);text=model_text(output);details['semantic_card']=output['card']
    record_ids=json.loads(records);citations=[]
    if record_ids:
        reg,led=citation_records()
        for rid in record_ids:
            if rid not in reg:raise ValueError('Unresolved bibliographic identity in context')
            source=reg[rid];reading=led[rid]
            citations.append(dict(record_id=rid,citekey=source.get('citekey'),title=source.get('title'),bibliographic_status=source['bib_status'],reading_level=reading.get('livello_attuale'),reading_closed=reading['lettura_integrale_chiusa'],source_path=source['source_path'],local_copy_path=reading.get('local_copy_path'),editorial_usage_map=reading.get('editorial_usage_map'),edition_frontier=reading.get('edition_frontier')))
    return dict(kind=kind,title=title,locator=locator,record_ids=record_ids,review_status=status,reference=ref,sha256=h,text=text,details=details,citations=citations,ready_for_unchecked_manuscript_citation=False)

def search(query,limit=12,scope='all',db=DB):
    with readonly(db) as con:
        filt=SCOPES[scope];params=[query_expression(query)];where=''
        if filt:where=' AND d.kind IN ('+','.join('?' for _ in filt)+')';params+=sorted(filt)
        sql='SELECT d.id,d.kind,d.title,d.locator,d.source_ref,d.source_sha256,d.record_ids,d.review_status,d.details,bm25(search) FROM search JOIN documents d ON d.id=search.rowid WHERE search MATCH ?'+where+" ORDER BY CASE WHEN d.review_status LIKE 'historical%' THEN 7 ELSE CASE d.kind WHEN 'reading-note' THEN 0 WHEN 'editorial-map' THEN 0 WHEN 'author-comment' THEN 1 WHEN 'author-paragraph' THEN 1 WHEN 'project-note' THEN 2 WHEN 'model-card' THEN 3 WHEN 'extracted-unit' THEN 4 ELSE 5 END END,bm25(search) LIMIT ?"
        rows=con.execute(sql,params+[limit]).fetchall();out=[]
        for row in rows:
            item=recover(row[1:-1]);text=item.pop('text');tokens=re.findall(r'\w+',query);hit=next((m for word in tokens if (m:=re.search(re.escape(word),text,re.I))),None);start=max(0,(hit.start() if hit else 0)-200)
            card=item['details'].pop('semantic_card',None)
            if card:
                matches=[dict(group=group,**v) for group in ['claims','terms','relations','references'] for v in card.get(group,[]) if any(word.casefold() in json.dumps(v,ensure_ascii=False).casefold() for word in tokens)]
                item['semantic_matches']=matches[:4]
            item.update(id=row[0],excerpt=text[start:start+2200],excerpt_start_char=start,text_chars=len(text),score=row[-1]);out.append(item)
        return out

def show(doc_id,db=DB):
    with readonly(db) as con:row=con.execute('SELECT kind,title,locator,source_ref,source_sha256,record_ids,review_status,details FROM documents WHERE id=?',(doc_id,)).fetchone()
    if row is None:raise ValueError('Unknown context document')
    return recover(row)

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('command',choices=['build','status','search','show']);parser.add_argument('--query');parser.add_argument('--scope',choices=SCOPES,default='all');parser.add_argument('--limit',type=int,default=12);parser.add_argument('--id',type=int);args=parser.parse_args()
    if not 1<=args.limit<=50:parser.error('limit must be between 1 and 50')
    if args.command=='build':out=build();out={k:out[k] for k in ['generated_utc','counts','registered_sources','prepared_sources','model_items','all_indexable_inputs_covered','index_bytes']}
    elif args.command=='status':
        with readonly(DB) as con:out=json.loads(con.execute("SELECT value FROM meta WHERE key='manifest'").fetchone()[0])
    elif args.command=='search':out=search(args.query or '',args.limit,args.scope)
    else:out=show(args.id)
    print(json.dumps(out,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
