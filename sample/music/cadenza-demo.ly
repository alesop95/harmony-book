\version "2.24.0"
% Esempio dimostrativo: cadenza perfetta V-I in Do maggiore.
% Serve solo a verificare la catena lilypond-book -> LuaLaTeX; non e' contenuto del libro.
\score {
  \new PianoStaff <<
    \new Staff { \clef treble \time 4/4 <b d' g'>2 <c' e' g'>2 \bar "|." }
    \new Staff { \clef bass \time 4/4 <g, g>2 <c, c>2 \bar "|." }
  >>
  \layout { }
}
