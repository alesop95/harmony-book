# Snapshot di sincronizzazione

> Da leggere per primo a inizio sessione. Fotografa lo stato del progetto al commit di
> riferimento e mappa ogni scheda al suo stato di verifica. È la fonte di verità su cosa è fatto,
> non le spunte del diario.

## Stato

```
Branch attivo:        main
Commit di riferimento: 9acc2e0 (schede riancorate con sync-context il 2026-08-05)
Data snapshot:        2026-08-05
```

## Stato di verifica delle schede

| Scheda | last-verified | Stato |
|---|---|---|
| STACK.md | 9acc2e0 | nessun drift nelle aree coperte; resta il gap noto, `tools/` non e in `covers-paths` e i suoi otto script non sono descritti in scheda |
| design-and-security.md | 9acc2e0 | nessun drift; diagrammi registrati e riconciliati, paradigmi da popolare |
| deployment.md | 017b02a | da popolare (covers-paths vuoto, nessun confronto di drift applicabile) |
| dev-testing.md | 017b02a | da popolare (covers-paths vuoto, nessun confronto di drift applicabile) |
| current-work.md | 9acc2e0 | aggiornata il 2026-08-05 con la voce sulla rigenerazione di `armonia-libro` |
| roadmap.md | 017b02a | aggiornata (covers-paths vuoto, nessun confronto di drift applicabile) |

**Sync del 2026-08-05**: confronto `4942de1..9acc2e0` per STACK.md e design-and-security.md,
`dd1c4d5..9acc2e0` per current-work.md. Zero file cambiati nelle aree coperte da ciascuna scheda,
quindi il bump e un checkpoint e non una riconciliazione. Le tre schede con `covers-paths` vuoto
restano fuori dal confronto e non si bumpano.

**Drift chiuso il 2026-07-17**: i quattro commit intercorsi (`f3a6c45`, `f2d8d9c`, `bb78fca`,
`2c49269`, `4942de1`) sono stati riconciliati con `sync-context`. L'unico cambiamento sostanziale
nelle aree coperte era l'ambiente `apertura` aggiunto a `style/harmony-macros.sty` (introdotto in
`f3a6c45`), ora documentato in `STACK.md`; i diagrammi in `design-and-security.md` erano già
corretti nel contenuto, solo l'ancoraggio era stale. `deployment.md`, `dev-testing.md` e
`roadmap.md` non hanno `covers-paths` popolati e restano fuori da questo confronto.

## Punto di ripresa

Aggiornato a mano il 2026-08-05. Il ciclo di lavoro fitto va dal 2026-07-29 al 2026-08-03; il
2026-08-05 non ha aggiunto contenuto al libro, ha rimesso in pari la skill `armonia-libro` e sanato
due note stale, come racconta la voce in testa al work-log. La guida operativa alla ripresa e la nota
del 2026-08-03 in testa a `_notes/RESUME-PROMPT.md`, e la guida alla rilettura del capitolo e
`_notes/STATO-CAPITOLO-TRITONO.md`, rivista il 2026-08-05.

Una cosa da sapere prima di usare gli strumenti di freschezza, perche e costata un ciclo di deriva
invisibile: `python tools/skill-freshness.py <skill> --update` riallinea gli hash e non tocca il
contenuto, quindi si lancia soltanto dopo aver rigenerato i file della skill, mai prima. Il 2026-08-03
e stato lanciato senza rigenerare, e l'intero lavoro di quel giorno e rimasto fuori da `armonia-libro`
fino al 2026-08-05.

Ambiente e catena di build LaTeX/LilyPond verificati (ADR-003). Il capitolo sul tritono e una bozza
matura, 48314 caratteri e nove movimenti, ma vive ancora in `_notes/appunti-da-inserire-nel-libro/` e
NON e nel manoscritto: `manuscript/chapters/` contiene solo introduzione e scheletro del capitolo 1, e
`build/main.pdf` e fermo al 2026-07-16. La trascrizione in `.lytex` resta il passo piu urgente e piu
rinviato.

Cosa e cambiato in questo ciclo. Sono nate tre skill: `armonia-libro`, che digerisce la dottrina del
libro dell'utente, `libro-berkman`, che rende interrogabile Berkman 2013, e `fonte-nuova`, che e la
procedura per far entrare una fonte dichiarandone il livello di verifica. Le prime due sono ignorate
da git per ADR-007 perche sono contenuto, la terza e tracciata perche e procedura. La bibliografia e
passata da 91 a 101 voci, con sette fonti nuove, e ogni voce dichiara ora in testa al campo `note` il
proprio livello di verifica secondo ADR-008. Sono nati quattro strumenti Python che implementano
affermazioni del libro invece di documentarle, secondo ADR-009, e due di essi hanno cambiato il
contenuto del capitolo: `tritoni-scale.py` ha smentito l'intuizione sulla corrispondenza biunivoca fra
scale e coppie di tritoni, `derivazione-scale.py` ha fatto emergere la scala napoletana minore, che
era registrata come direzione futura sospesa per mancanza di fonti.

Il risultato di contenuto piu importante: girando la macchina delle dominanti secondarie su tutti i
gradi di Do maggiore, con una sola alterazione per accordo, escono due tonalita confinanti e quattro
scale derivate, cioe due minori melodiche, una minore armonica e la napoletana minore. La spiegazione
e che il tritono di una scala diatonica e formato dai due estremi della catena di quinte: alterare un
estremo fa slittare la catena e produce la tonalita vicina, alterare un interno la spezza e produce
una scala nuova con due tritoni.

Tre correzioni dell'agente in questo ciclo, tutte registrate in `_notes/STATO-CAPITOLO-TRITONO.md`,
l'ultima rilevata dall'utente e formalizzata in ADR-009. Da tenere presente alla ripresa: quando si
usa la macchina delle derivazioni, la definizione di dominante e quella del libro, cioe il tritono fra
terza maggiore e settima minore, non la quinta giusta.

Cosa aspetta l'utente: materiale privato sulla scala napoletana, annunciato e non consegnato, che
sblocchera l'espansione della tabella con le armonizzazioni. Cosa aspetta una sua parola: l'analisi
del livello II della macchina, calcolata e rinviata; il risultato 4 sui tre tipi di coppia di
tritoni, calcolato e mai proposto perche toccherebbe i movimenti F e H insieme; sei ragionamenti
ancora in stato "da proporre" in `_notes/ragionamenti-da-portare-nel-libro.md`; se spezzare il
movimento E, oggi al 22 per cento; e due nodi bibliografici da sciogliere prima di andare in LaTeX,
cioe il riferimento [8] che copre due fonti Sarti distinte e la fonte Springsteen che nel capitolo e
[10] ma non ha voce nel registro.

Nota sui numeri bibliografici, ricalcolati sui file reali il 2026-08-05 e da preferire a quelli
scritti altrove: il registro ha 172 voci, di cui 99 verificate, 65 da verificare e 8 scartate, e
`manuscript/bib/references.bib` ne contiene 101.

A ogni avanzamento significativo sulla stesura vera e propria: aggiornare le schede impattate e il
work-log, poi l'utente committa e si rilancia `sync-context` per bumpare `last-verified-commit`. Da
collaudare ancora la parita Linux degli script `.sh`. Da riconciliare `STACK.md`, che non descrive i
quattro strumenti nuovi sotto `tools/`.
