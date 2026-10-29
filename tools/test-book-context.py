"""Verify retrieval, revision boundaries and refusal of changed evidence."""
from pathlib import Path
import hashlib,importlib.util,json,re,shutil,sqlite3,sys,unittest,uuid
from zipfile import ZipFile
TOOL=Path(__file__).with_name('book-context.py')
def load(source=None):
    spec=importlib.util.spec_from_file_location('book_context_under_test',TOOL);v=importlib.util.module_from_spec(spec)
    if source is None:spec.loader.exec_module(v)
    else:exec(compile(source,str(TOOL),'exec'),v.__dict__)
    return v
ctx=load()

class ContextTests(unittest.TestCase):
    def setUp(self):
        self.folder=ctx.NOTES/'99-cache'/('test-contesto-'+uuid.uuid4().hex);self.folder.mkdir(parents=True)
    def tearDown(self):
        ctx.docx_parts.cache_clear();assert self.folder.resolve().is_relative_to((ctx.NOTES/'99-cache').resolve()) and self.folder.name.startswith('test-contesto-');shutil.rmtree(self.folder)
    def note(self,text):
        path=self.folder/'nota.md';path.write_text(text,encoding='utf-8');return path,ctx.digest(text.encode())
    def row(self,path,h):return ('reading-note','Nota','paragrafo',json.dumps({'path':ctx.relative(path)}),h,'[]','authored-note','{}')
    def test_changed_evidence_is_rejected(self):
        path,h=self.note('proposizione iniziale');row=self.row(path,h);path.write_text('proposizione cambiata',encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'Document changed'):ctx.recover(row)
    def test_evidence_recovers_exact_text(self):
        text='Una nota con accenti e localizzatore.';path,h=self.note(text);out=ctx.recover(self.row(path,h));self.assertEqual(out['text'],text);self.assertFalse(out['ready_for_unchecked_manuscript_citation'])
    def test_query_is_text_not_fts_instructions(self):
        value=ctx.query_expression('alpha" OR beta');self.assertEqual(value,'("alpha") AND ("OR") AND ("beta")')
    def test_concept_alias_is_explicit(self):self.assertIn('"tritone"',ctx.query_expression('tritono'))
    def test_private_boundary(self):
        with self.assertRaisesRegex(ValueError,'private project'):ctx.private_path('../outside.md')
    def docx(self):
        path=self.folder/'commentato.docx';ns='http://schemas.openxmlformats.org/wordprocessingml/2006/main'
        body=f'<w:document xmlns:w="{ns}"><w:body><w:p><w:r><w:t>prima </w:t></w:r><w:commentRangeStart w:id="7"/><w:r><w:t>selezione uno</w:t></w:r></w:p><w:p><w:r><w:t>selezione due</w:t></w:r><w:commentRangeEnd w:id="7"/><w:r><w:commentReference w:id="7"/></w:r><w:del w:id="3"><w:r><w:delText>testo eliminato</w:delText></w:r></w:del><w:ins w:id="4"><w:r><w:t>testo aggiunto</w:t></w:r></w:ins></w:p></w:body></w:document>'
        comments=f'<w:comments xmlns:w="{ns}"><w:comment w:id="7"><w:p><w:r><w:t>Commento da discutere.</w:t></w:r></w:p></w:comment><w:comment w:id="8"><w:p><w:r><w:t>Commento senza ancora.</w:t></w:r></w:p></w:comment></w:comments>'
        with ZipFile(path,'w') as doc:doc.writestr('word/document.xml',body);doc.writestr('word/comments.xml',comments)
        return path
    def test_comment_span_crosses_paragraphs_once(self):
        path=self.docx();rows=ctx.docx_parts(ctx.relative(path),ctx.digest(path.read_bytes()));item=next(v for v in rows if v['key']=='comment:7')
        self.assertEqual([(v['paragraph'],v['selected_text']) for v in item['anchors']],[(1,'selezione uno'),(2,'selezione due')]);self.assertTrue(item['range_is_complete']);self.assertEqual(item['text'].count('selezione due'),1)
    def test_unanchored_comment_is_preserved(self):
        path=self.docx();rows=ctx.docx_parts(ctx.relative(path),ctx.digest(path.read_bytes()));item=next(v for v in rows if v['key']=='comment:8');self.assertIn('senza ancora',item['text']);self.assertFalse(item['anchor_found'])
    def test_revisions_preserve_deleted_text_without_acceptance(self):
        path=self.docx();before=path.read_bytes();rows=ctx.docx_parts(ctx.relative(path),ctx.digest(before));deleted=[v for v in rows if v.get('revision_kind')=='deleted'];self.assertEqual([v['text'] for v in deleted],['testo eliminato']);self.assertEqual(path.read_bytes(),before);self.assertNotIn('testo eliminato',' '.join(v['text'] for v in rows if v['kind']=='author-paragraph'))
    def test_changed_docx_is_rejected(self):
        path=self.docx();h=ctx.digest(path.read_bytes());path.write_bytes(path.read_bytes()+b'changed')
        with self.assertRaisesRegex(ValueError,'Author document changed'):ctx.docx_parts(ctx.relative(path),h)
    def test_cached_docx_does_not_hide_a_new_revision(self):
        path=self.docx();h=ctx.digest(path.read_bytes());self.assertTrue(ctx.docx_parts(ctx.relative(path),h));path.write_bytes(path.read_bytes()+b'changed')
        with self.assertRaisesRegex(ValueError,'Author document changed'):ctx.docx_parts(ctx.relative(path),h)

def run():return unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromTestCase(ContextTests))
if __name__=='__main__':
    original=TOOL.read_bytes();base=ctx
    if '--mutation-check' not in sys.argv:raise SystemExit(not run().wasSuccessful())
    assert run().wasSuccessful()
    source=original.decode();guard="if digest(text.encode())!=h:raise ValueError('Document changed; rebuild context index')";assert source.count(guard)==1
    ctx=load(source.replace(guard,'if False:raise ValueError(\'Document changed; rebuild context index\')'));mutant=run();failed=[test.id().rsplit('.',1)[-1] for test,_ in mutant.failures];assert failed==['test_changed_evidence_is_rejected'] and not mutant.errors
    ctx=base;assert TOOL.read_bytes()==original and run().wasSuccessful()
    print(json.dumps(dict(tests=10,mutation_detected_by=failed,original_source_unchanged=True)))
