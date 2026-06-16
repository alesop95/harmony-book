#!/bin/sh
# Compila il libro (LuaLaTeX + LilyPond) in modo riproducibile (Unix/macOS).
# Sezione 13 di .claude/PROJECT-SYSTEM.md. Trova latexmk nell'ambiente TinyTeX user-local e,
# se il sorgente e' un .lytex con esempi musicali, esegue prima lilypond-book (binario esterno),
# poi compila con LuaLaTeX (engine fissato in .latexmkrc). Output e ausiliari in build/.
#
# Uso:
#   sh scripts/build.sh [--main FILE] [--no-lily] [--clean] [--clean-all] [--tex-dir DIR]
set -eu

MAIN=""
NO_LILY=0
MODE="build"
TEX_DIR=""
LILY_DIR="${LILYPOND_BIN:-}"

while [ $# -gt 0 ]; do
  case "$1" in
    --main)      MAIN="$2"; shift ;;
    --no-lily)   NO_LILY=1 ;;
    --clean)     MODE="clean" ;;
    --clean-all) MODE="cleanall" ;;
    --tex-dir)   TEX_DIR="$2"; shift ;;
    --lily-dir)  LILY_DIR="$2"; shift ;;
    *) echo "[build] Argomento sconosciuto: $1" >&2; exit 2 ;;
  esac
  shift
done

find_lily_bin() {
  # Cartella bin di LilyPond: override, poi PATH, poi posizioni comuni. Nessun path di macchina hardcoded.
  if [ -n "$LILY_DIR" ] && [ -x "$LILY_DIR/lilypond" ]; then echo "$LILY_DIR"; return 0; fi
  if command -v lilypond >/dev/null 2>&1; then dirname "$(command -v lilypond)"; return 0; fi
  for base in /opt /usr/local "$HOME" "$HOME/.local"; do
    [ -d "$base" ] || continue
    for p in "$base"/lilypond*/bin/lilypond "$base"/lilypond*/*/bin/lilypond; do
      [ -x "$p" ] && { dirname "$p"; return 0; }
    done
  done
  return 1
}

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PROJECT_ROOT=$(dirname -- "$SCRIPT_DIR")
STYLE_DIR="$PROJECT_ROOT/style"
OUT_DIR="$PROJECT_ROOT/build"
[ -n "$TEX_DIR" ] || TEX_DIR="$HOME/.TinyTeX"

find_bin() {
  name="$1"
  if command -v "$name" >/dev/null 2>&1; then command -v "$name"; return 0; fi
  for p in "$TEX_DIR"/bin/*/"$name"; do
    [ -x "$p" ] && { echo "$p"; return 0; }
  done
  return 1
}

if [ "$MODE" = "cleanall" ]; then
  rm -rf "$OUT_DIR"; echo "[build] Rimossa build/."; exit 0
fi

LATEXMK=$(find_bin latexmk) || { echo "[build] latexmk non trovato. Esegui prima sh scripts/setup-tex.sh." >&2; exit 1; }

# --- Determina il file principale ---
if [ -z "$MAIN" ]; then
  for cand in manuscript/main.lytex manuscript/main.tex sample/main.lytex sample/main.tex; do
    [ -f "$PROJECT_ROOT/$cand" ] && { MAIN="$PROJECT_ROOT/$cand"; break; }
  done
  [ -n "$MAIN" ] || { echo "[build] Nessun main trovato (manuscript/ o sample/). Specifica --main." >&2; exit 1; }
else
  case "$MAIN" in /*) : ;; *) MAIN="$PROJECT_ROOT/$MAIN" ;; esac
fi
[ -f "$MAIN" ] || { echo "[build] File principale inesistente: $MAIN" >&2; exit 1; }

SRC_DIR=$(dirname -- "$MAIN")
BASE=$(basename -- "$MAIN"); BASE="${BASE%.*}"
EXT="${MAIN##*.}"
mkdir -p "$OUT_DIR"

# Percorsi di ricerca TeX: ':' separatore, '//' ricorsivo, ':' finale = default di sistema.
export TEXINPUTS="$PROJECT_ROOT:$STYLE_DIR//:$SRC_DIR//:$OUT_DIR//:"
export BIBINPUTS="$SRC_DIR:$SRC_DIR/bib:$PROJECT_ROOT:"

if [ "$MODE" = "clean" ]; then
  ( cd "$OUT_DIR" && "$LATEXMK" -c "$BASE.tex" 2>/dev/null || true )
  echo "[build] Ausiliari rimossi in build/."; exit 0
fi

# --- Passata LilyPond (solo per .lytex, salvo --no-lily) ---
TEX_TO_COMPILE="$MAIN"
COMPILE_DIR="$SRC_DIR"
if [ "$EXT" = "lytex" ] && [ "$NO_LILY" -eq 0 ]; then
  if LILY_BIN=$(find_lily_bin); then PATH="$LILY_BIN:$PATH"; export PATH; fi
  if command -v lilypond-book >/dev/null 2>&1; then
    LILYBOOK=$(command -v lilypond-book)
  elif [ -n "${LILY_BIN:-}" ] && [ -x "$LILY_BIN/lilypond-book" ]; then
    LILYBOOK="$LILY_BIN/lilypond-book"
  else
    echo "[build] lilypond-book non trovato. Installa LilyPond e mettilo sul PATH, imposta LILYPOND_BIN / --lily-dir, o usa --no-lily." >&2
    exit 1
  fi
  echo "[build] lilypond-book ($LILYBOOK): preprocesso $(basename -- "$MAIN") -> build/ ..."
  "$LILYBOOK" --pdf --output="$OUT_DIR" --include="$STYLE_DIR" --include="$SRC_DIR" "$MAIN"
  TEX_TO_COMPILE="$OUT_DIR/$BASE.tex"
  COMPILE_DIR="$OUT_DIR"
fi

# --- Compilazione LuaLaTeX via latexmk ---
echo "[build] Compilo $(basename -- "$TEX_TO_COMPILE") con latexmk (LuaLaTeX) ..."
if [ "$COMPILE_DIR" = "$OUT_DIR" ]; then
  ( cd "$OUT_DIR" && "$LATEXMK" -lualatex "$(basename -- "$TEX_TO_COMPILE")" )
else
  ( cd "$COMPILE_DIR" && "$LATEXMK" -lualatex -outdir="$OUT_DIR" "$(basename -- "$TEX_TO_COMPILE")" )
fi

echo "[build] Fatto: $OUT_DIR/$BASE.pdf"
