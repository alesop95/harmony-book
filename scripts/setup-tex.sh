#!/bin/sh
# Bootstrap dell'ambiente LaTeX (TinyTeX) per Unix/macOS, guidato dal manifesto.
# Sezione 13 di .claude/PROJECT-SYSTEM.md. Localizza TinyTeX (installazione user-local
# condivisa), se assente lo installa, installa i pacchetti da tex-packages.txt con tlmgr,
# e verifica con una compilazione minima in LuaLaTeX. Segnala se LilyPond (binario esterno
# per gli esempi musicali) non e' sul PATH. Invoca i binari per percorso, niente shell
# interattiva, identico in locale e in CI.
#
# Uso:
#   sh scripts/setup-tex.sh [--reinstall] [--tex-dir DIR] [--skip-packages] [--manifest FILE]
set -eu

REINSTALL=0
SKIP_PACKAGES=0
TEX_DIR=""
MANIFEST=""

while [ $# -gt 0 ]; do
  case "$1" in
    --reinstall)      REINSTALL=1 ;;
    --skip-packages)  SKIP_PACKAGES=1 ;;
    --tex-dir)        TEX_DIR="$2"; shift ;;
    --manifest)       MANIFEST="$2"; shift ;;
    *) echo "[setup-tex] Argomento sconosciuto: $1" >&2; exit 2 ;;
  esac
  shift
done

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PROJECT_ROOT=$(dirname -- "$SCRIPT_DIR")
[ -n "$MANIFEST" ] || MANIFEST="$PROJECT_ROOT/tex-packages.txt"
[ -n "$TEX_DIR" ] || TEX_DIR="$HOME/.TinyTeX"

find_tlmgr() {
  if command -v tlmgr >/dev/null 2>&1; then command -v tlmgr; return 0; fi
  for root in "$TEX_DIR" "$HOME/.TinyTeX" "$HOME/Library/TinyTeX"; do
    for p in "$root"/bin/*/tlmgr; do
      [ -x "$p" ] && { echo "$p"; return 0; }
    done
  done
  return 1
}

if [ "$REINSTALL" -eq 1 ] && [ -d "$TEX_DIR" ]; then
  echo "[setup-tex] Rimuovo l'installazione esistente: $TEX_DIR"
  rm -rf "$TEX_DIR"
fi

if ! TLMGR=$(find_tlmgr); then
  echo "[setup-tex] TinyTeX non trovato. Installazione in: $TEX_DIR"
  export TINYTEX_DIR="$TEX_DIR"
  if command -v wget >/dev/null 2>&1; then
    wget -qO- "https://yihui.org/tinytex/install-bin-unix.sh" | sh
  elif command -v curl >/dev/null 2>&1; then
    curl -fsSL "https://yihui.org/tinytex/install-bin-unix.sh" | sh
  else
    echo "[setup-tex] Servono wget o curl per scaricare l'installer." >&2; exit 1
  fi
  TLMGR=$(find_tlmgr) || { echo "[setup-tex] Installazione fallita: tlmgr non trovato." >&2; exit 1; }
fi
echo "[setup-tex] tlmgr: $TLMGR"
TEX_BIN=$(dirname -- "$TLMGR")

echo "[setup-tex] Aggiorno tlmgr ..."
"$TLMGR" update --self

if [ "$SKIP_PACKAGES" -eq 0 ]; then
  [ -f "$MANIFEST" ] || { echo "[setup-tex] Manifesto non trovato: $MANIFEST" >&2; exit 1; }
  PKGS=$(sed -e 's/#.*$//' -e 's/[[:space:]]*$//' "$MANIFEST" | grep -v '^[[:space:]]*$' || true)
  if [ -n "$PKGS" ]; then
    echo "[setup-tex] Installo i pacchetti dal manifesto ..."
    # shellcheck disable=SC2086
    "$TLMGR" install $PKGS
  fi
fi

echo "[setup-tex] Verifica: compilo un documento di prova con LuaLaTeX ..."
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
cat > "$TMP/probe.tex" <<'EOF'
\documentclass{memoir}
\usepackage{fontspec}
\usepackage[italian]{babel}
\usepackage[final,expansion=true,protrusion=true]{microtype}
\usepackage{csquotes}
\begin{document}
Prova di tipografia editoriale: \enquote{armonia} con microtype attivo.
\end{document}
EOF
"$TEX_BIN/lualatex" -interaction=nonstopmode -halt-on-error -output-directory "$TMP" "$TMP/probe.tex" >/dev/null
[ -f "$TMP/probe.pdf" ] || { echo "[setup-tex] Verifica fallita: nessun PDF prodotto." >&2; exit 1; }
echo "[setup-tex] OK. Ambiente LaTeX (LuaLaTeX) pronto."

# --- Controllo di LilyPond (binario esterno, non parte di TinyTeX) -------------
if command -v lilypond >/dev/null 2>&1 && command -v lilypond-book >/dev/null 2>&1; then
  echo "[setup-tex] LilyPond trovato: $(command -v lilypond)"
else
  echo "[setup-tex] ATTENZIONE: LilyPond / lilypond-book NON trovati sul PATH." >&2
  echo "[setup-tex] Gli esempi musicali richiedono LilyPond, binario esterno a TinyTeX."
  echo "[setup-tex] Installalo (es. dal gestore pacchetti o da https://lilypond.org) e"
  echo "[setup-tex] assicurati che 'lilypond' e 'lilypond-book' siano sul PATH."
fi

echo "[setup-tex] Per compilare il progetto: sh scripts/build.sh"
echo "[setup-tex] Nota: aggiungi '$TEX_BIN' al PATH per usare lualatex/latexmk a mano."
