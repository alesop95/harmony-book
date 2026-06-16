# Configurazione di latexmk per una build riproducibile (sezione 13 di PROJECT-SYSTEM.md).
# Engine fissato a LuaLaTeX: Unicode nativo, font OpenType via fontspec, microtype completo
# (espansione + protrusione). Letto automaticamente da latexmk quando eseguito nella radice.

$pdf_mode = 4;   # 4 = lualatex (1 = pdflatex, 5 = xelatex)
$lualatex = 'lualatex -interaction=nonstopmode -halt-on-error -synctex=1 -file-line-error %O %S';

# Bibliografia: biblatex + biber. latexmk rileva ed esegue biber da solo.
$bibtex_use = 2;

# Glossario: fa eseguire makeglossaries quando esistono voci di glossario, cosi' il glossario
# del libro si rigenera automaticamente nel ciclo di build (l'indice via makeindex e' gia' nativo).
add_cus_dep('glo', 'gls', 0, 'run_makeglossaries');
add_cus_dep('acn', 'acr', 0, 'run_makeglossaries');
sub run_makeglossaries { return system('makeglossaries', $_[0]); }

# Estensioni ausiliarie da rimuovere con `latexmk -c` / `-C` (coerenti col .gitignore).
# Incluse quelle di biblatex/biber (bbl blg bcf run.xml), glossaries (glo gls glg ist) e
# indice (idx ind ilg), oltre a quelle LilyPond/lilypond-book residue.
$clean_ext = 'synctex.gz aux fdb_latexmk fls run.xml bcf nav snm vrb out toc lof lot bbl blg glo gls glg ist acn acr alg idx ind ilg';
