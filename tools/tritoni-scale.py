#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tritoni-scale.py - Contenuto di tritoni delle scale, ed esame della corrispondenza
fra una scala e la sua coppia di tritoni.

Nasce per verificare l'intuizione registrata nel movimento E del capitolo sul tritono: se
ogni scala minore melodica di prima derivazione porta esattamente due tritoni, e se quella
coppia individua la scala, allora fra scale e coppie di tritoni c'e una corrispondenza
biunivoca. E' una proprieta combinatoria, quindi si verifica contando, non cercando una
fonte: e il precedente metodologico esiste, perche Browne nel 1981 ricavo l'ipotesi degli
intervalli rari contando le molteplicita degli intervalli nel set diatonico.

Rappresentazione: una scala e un insieme di classi di altezza, cioe di interi modulo 12. Un
tritono e una coppia non ordinata {p, p+6}, quindi esistono soltanto 6 tritoni distinti:
{0,6} {1,7} {2,8} {3,9} {4,10} {5,11}. Una coppia di tritoni e un sottoinsieme di 2 dei 6,
quindi le coppie possibili sono 15.

Uso:
    python tools/tritoni-scale.py                  # rapporto completo
    python tools/tritoni-scale.py --famiglia melodica-minore
    python tools/tritoni-scale.py --scala 9,11,0,2,4,6,8   # una scala arbitraria
"""

import argparse
import itertools
import sys
from collections import defaultdict

NOMI = ["Do", "Do#", "Re", "Mib", "Mi", "Fa", "Fa#", "Sol", "Lab", "La", "Sib", "Si"]

# Famiglie di scale, per gradi in semitoni dalla fondamentale.
FAMIGLIE = {
    "maggiore":          (0, 2, 4, 5, 7, 9, 11),
    "melodica-minore":   (0, 2, 3, 5, 7, 9, 11),
    "armonica-minore":   (0, 2, 3, 5, 7, 8, 11),
    "armonica-maggiore": (0, 2, 4, 5, 7, 8, 11),
}

# I sei tritoni distinti, come coppie di classi di altezza.
TRITONI = [frozenset((i, i + 6)) for i in range(6)]


def nome_tritono(t):
    a, b = sorted(t)
    return f"{NOMI[a]}-{NOMI[b]}"


def scala(famiglia, fondamentale):
    return frozenset((fondamentale + g) % 12 for g in FAMIGLIE[famiglia])


def tritoni_di(pcs):
    """I tritoni interamente contenuti nell'insieme di classi di altezza."""
    return frozenset(t for t in TRITONI if t <= set(pcs))


def trasponi(pcs, n):
    return frozenset((x + n) % 12 for x in pcs)


def stabilizzatore(pcs):
    """Le trasposizioni che lasciano l'insieme invariato. E' il gruppo di simmetria
    per trasposizione, e la sua ampiezza spiega la degenerazione del descrittore."""
    return [n for n in range(12) if trasponi(pcs, n) == frozenset(pcs)]


def spiega_degenerazione(famiglia, out):
    """Perche una coppia di tritoni non puo mai individuare una scala sola.

    Teorema 1. Per qualunque insieme di note, S e la sua trasposizione di tritono hanno
    lo stesso identico contenuto di tritoni. Dimostrazione in una riga: un tritono e
    {a, a+6}, e traslarlo di 6 da {a+6, a+12} cioe {a+6, a}, che e lo stesso insieme.
    Quindi T6 fissa ogni tritono, e percio fissa il contenuto di qualunque scala. Ne
    segue che nessun descrittore fondato sui soli tritoni potra MAI distinguere una
    scala dalla sua trasposizione di tritono: e un limite di principio, non un difetto
    del metodo.

    Teorema 2. La degenerazione del descrittore, cioe quante scale condividono la stessa
    coppia, e uguale all'ampiezza dello stabilizzatore dell'insieme di note che la coppia
    forma. Se quelle quattro note formano una sesta eccedente francese, invariante solo
    per T0 e T6, la degenerazione e 2, che e il minimo possibile per il teorema 1. Se
    formano una settima diminuita, invariante per T0, T3, T6 e T9, la degenerazione e 4.
    """
    s = scala(famiglia, 0)
    ts = tritoni_di(s)
    note = frozenset().union(*ts) if ts else frozenset()
    stab = stabilizzatore(note)
    mappa = {}
    for r in range(12):
        mappa.setdefault(tritoni_di(scala(famiglia, r)), []).append(r)
    deg = max(len(v) for v in mappa.values())
    out(f"  {famiglia:18} note della coppia: {', '.join(NOMI[x] for x in sorted(note))}")
    out(f"  {'':18} invariante per trasposizione di: {', '.join(str(x) for x in stab)} semitoni")
    out(f"  {'':18} degenerazione attesa {len(stab)}, osservata {deg}  "
        f"{'coincide' if len(stab) == deg else 'NON COINCIDE, da indagare'}")
    out(f"  {'':18} {'ottimale: e il minimo consentito dal teorema 1' if deg == 2 else 'peggiore del minimo: il descrittore perde informazione'}")


def rapporto_famiglia(famiglia, out):
    out(f"\n=== {famiglia} ===")
    mappa = defaultdict(list)
    conteggi = defaultdict(int)
    for r in range(12):
        s = scala(famiglia, r)
        ts = tritoni_di(s)
        conteggi[len(ts)] += 1
        mappa[ts].append(r)
        etichette = ", ".join(sorted(nome_tritono(t) for t in ts)) or "nessuno"
        out(f"  {NOMI[r]:4} {famiglia:18} tritoni: {len(ts)}  [{etichette}]")
    out(f"  conteggio: " + ", ".join(f"{n} tritoni in {c} scale" for n, c in sorted(conteggi.items())))
    collisioni = {k: v for k, v in mappa.items() if len(v) > 1}
    if collisioni:
        out(f"  COLLISIONI dentro la famiglia: {len(collisioni)}")
        for k, v in collisioni.items():
            out(f"    {sorted(nome_tritono(t) for t in k)} <- {[NOMI[r] for r in v]}")
    else:
        out(f"  nessuna collisione: la coppia individua la scala DENTRO questa famiglia")
    return mappa


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[2])
    p.add_argument("--famiglia", choices=sorted(FAMIGLIE), help="esamina una sola famiglia")
    p.add_argument("--scala", help="insieme di classi di altezza separate da virgola, es. 9,11,0,2,4,6,8")
    a = p.parse_args()
    out = print

    if a.scala:
        pcs = frozenset(int(x) % 12 for x in a.scala.split(","))
        ts = tritoni_di(pcs)
        out("note: " + ", ".join(NOMI[x] for x in sorted(pcs)))
        out(f"tritoni: {len(ts)}  [" + ", ".join(sorted(nome_tritono(t) for t in ts)) + "]")
        return 0

    famiglie = [a.famiglia] if a.famiglia else sorted(FAMIGLIE)
    out("Coppie di tritoni possibili in totale: "
        f"{len(list(itertools.combinations(TRITONI, 2)))} (2 tritoni scelti fra 6)")

    tutte = {}
    for f in famiglie:
        for chiave, radici in rapporto_famiglia(f, out).items():
            for r in radici:
                tutte.setdefault(chiave, []).append((f, r))

    if len(famiglie) > 1:
        out("\n=== incrocio fra famiglie ===")
        soloduetritoni = {k: v for k, v in tutte.items() if len(k) == 2}
        out(f"scale con esattamente 2 tritoni, su tutte le famiglie: {sum(len(v) for v in soloduetritoni.values())}")
        out(f"coppie di tritoni distinte da esse realizzate: {len(soloduetritoni)}")
        ambigue = {k: v for k, v in soloduetritoni.items() if len(v) > 1}
        out(f"coppie condivise da piu di una scala: {len(ambigue)}")
        for k, v in sorted(ambigue.items(), key=lambda kv: sorted(nome_tritono(t) for t in kv[0])):
            et = ", ".join(sorted(nome_tritono(t) for t in k))
            chi = "; ".join(f"{NOMI[r]} {f}" for f, r in v)
            out(f"    [{et}] <- {chi}")

        out("\n=== perche la degenerazione e quella, e non un'altra ===")
        out("Teorema 1: un tritono e {a, a+6}, e traslarlo di 6 lo lascia identico. Quindi T6 fissa")
        out("ogni tritono, e nessun descrittore fondato sui soli tritoni potra mai distinguere una")
        out("scala dalla sua trasposizione di tritono. Due a uno e il MINIMO possibile, non un limite")
        out("di questo metodo.")
        out("Teorema 2: la degenerazione e uguale all'ampiezza dello stabilizzatore delle note che la")
        out("coppia forma. Verifica famiglia per famiglia:\n")
        for f in famiglie:
            spiega_degenerazione(f, out)
            out("")
    return 0


if __name__ == "__main__":
    sys.exit(main())
