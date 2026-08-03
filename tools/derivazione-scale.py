#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
derivazione-scale.py - La macchina delle dominanti secondarie, primo e secondo livello.

Implementa l'operazione su cui poggia il libro: si prende un accordo di settima diatonico
che abbia gia la settima minore, gli si da la terza maggiore, e si legge la scala che la
risoluzione lascia dietro di se.

Definizioni fissate dall'utente il 2026-08-03.
  Livello I  - le scale che si ottengono alterando UNA SOLA nota a partire dalla tonalita
               diatonica di partenza.
  Livello II - le scale che si ottengono applicando la stessa operazione a ciascuna delle
               scale di livello I, cioe rendendo dominante un accordo di quelle scale.

Punto delicato, corretto dall'utento il 2026-08-03 dopo un errore dell'agente: a una
dominante la quinta NON serve. Cio che la rende dominante e il tritono fra terza maggiore
e settima minore. Quindi al semidiminuito del settimo grado basta alzare la terza, e la
quinta diminuita resta dov'e: si ottiene un accordo di settima con quinta bemolle, che e
una dominante a tutti gli effetti, con UNA sola alterazione. Pretendere la quinta giusta
farebbe contare due alterazioni e falserebbe tutta la classificazione.

La doppia eredita del tritono si verifica confrontando i tritoni della scala derivata con
quelli della scala di partenza.

Uso:
    python tools/derivazione-scale.py                 # livello I da Do maggiore
    python tools/derivazione-scale.py --livello 2     # anche il secondo livello
    python tools/derivazione-scale.py --da 9,11,0,2,4,5,7   # da una scala arbitraria
"""

import argparse
import sys

NOMI = ["Do", "Do#", "Re", "Mib", "Mi", "Fa", "Fa#", "Sol", "Lab", "La", "Sib", "Si"]
TRITONI = [frozenset((i, i + 6)) for i in range(6)]

CATALOGO = {
    "maggiore": (0, 2, 4, 5, 7, 9, 11),
    "melodica minore": (0, 2, 3, 5, 7, 9, 11),
    "armonica minore": (0, 2, 3, 5, 7, 8, 11),
    "armonica maggiore": (0, 2, 4, 5, 7, 8, 11),
    "napoletana minore": (0, 1, 3, 5, 7, 8, 11),
    "napoletana maggiore": (0, 1, 3, 5, 7, 9, 11),
    "doppia armonica": (0, 1, 4, 5, 7, 8, 11),
    "melodica minore #4": (0, 2, 3, 6, 7, 9, 11),
}


def nn(x):
    return NOMI[x % 12]


def tritoni_di(pcs):
    return frozenset(t for t in TRITONI if t <= set(pcs))


def etichetta(t):
    a, b = sorted(t)
    return f"{nn(a)}-{nn(b)}"


def riconosci(pcs):
    for nome, gradi in CATALOGO.items():
        for r in range(12):
            if frozenset((r + g) % 12 for g in gradi) == frozenset(pcs):
                return f"{nn(r)} {nome}"
    return "non catalogata"


def settime(scala_ord):
    """Le sette settime diatoniche, come (indice del grado, insieme di 4 note)."""
    n = len(scala_ord)
    return [(i, frozenset(scala_ord[(i + k) % n] for k in (0, 2, 4, 6))) for i in range(n)]


def deriva(scala_ord):
    """Applica la macchina a ogni grado. Ritorna solo le derivazioni legittime, cioe
    quelle che partono da un accordo che ha gia la settima minore e che costano una sola
    alterazione."""
    base = frozenset(scala_ord)
    esiti = []
    for i, acc in settime(scala_ord):
        r = scala_ord[i]
        settima_min = (r + 10) % 12
        if settima_min not in acc:
            continue                      # non ha la settima minore: fuori
        terza_mag = (r + 4) % 12
        if terza_mag in acc:
            continue                      # e gia una dominante
        terza_vecchia = next((x for x in acc if (x - r) % 12 == 3), None)
        if terza_vecchia is None:
            continue
        dom = (acc - {terza_vecchia}) | {terza_mag}
        nuova = (base - acc) | dom
        alterazioni = sorted(nuova - base)
        if len(alterazioni) != 1:
            continue                      # non e di questo livello
        quinta_giusta = (r + 7) % 12 in dom
        ts, tb = tritoni_di(nuova), tritoni_di(base)
        esiti.append({
            "grado": i + 1,
            "fondamentale": r,
            "accordo": nn(r) + ("7" if quinta_giusta else "7b5"),
            "alterazione": alterazioni[0],
            "scala": nuova,
            "nome": riconosci(nuova),
            "ereditati": sorted(etichetta(t) for t in ts & tb),
            "nuovi": sorted(etichetta(t) for t in ts - tb),
        })
    return esiti


def stampa(esiti, base, indent=""):
    tb = ", ".join(sorted(etichetta(t) for t in tritoni_di(base)))
    print(f"{indent}da {riconosci(base)}   tritoni di partenza: {tb}")
    if not esiti:
        print(f"{indent}  nessuna derivazione a una sola alterazione")
    for e in esiti:
        de = "SI" if e["ereditati"] and e["nuovi"] else "no"
        print(f"{indent}  grado {e['grado']}  {e['accordo']:7} (+{nn(e['alterazione']):3}) "
              f"-> {e['nome']:24} eredita {de}")
        print(f"{indent}          {'':7}  {'':4}    tritoni: ereditato "
              f"{e['ereditati'] or '-'}, nuovo {e['nuovi'] or '-'}")


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[2])
    p.add_argument("--livello", type=int, default=1, choices=(1, 2))
    p.add_argument("--da", help="scala di partenza, classi di altezza separate da virgola")
    a = p.parse_args()

    base = sorted(int(x) % 12 for x in a.da.split(",")) if a.da else [0, 2, 4, 5, 7, 9, 11]
    print("=== LIVELLO I ===\n")
    liv1 = deriva(base)
    stampa(liv1, frozenset(base))

    if a.livello >= 2:
        print("\n=== LIVELLO II ===\n")
        viste = {frozenset(base)} | {e["scala"] for e in liv1}
        nuove = {}
        for e in liv1:
            figlie = deriva(sorted(e["scala"]))
            print(f"partendo da {e['nome']} (dal grado {e['grado']} della scala madre)")
            stampa(figlie, e["scala"], indent="  ")
            print()
            for f in figlie:
                if f["scala"] not in viste:
                    nuove.setdefault(f["nome"], set()).add(e["nome"])
        print("scale MAI viste al primo livello, comparse al secondo:")
        for nome, da in sorted(nuove.items()):
            print(f"  {nome:26} da: {', '.join(sorted(da))}")
        if not nuove:
            print("  nessuna")
    return 0


if __name__ == "__main__":
    sys.exit(main())
