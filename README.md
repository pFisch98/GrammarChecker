grammar_check.py ermöglicht es, auf Basis einer kontextfreien Grammatik zu überprüfen, ob sich ein als Parameter übergebenes Wort mittels besagter
Grammatik erzeugen lässt.
Zugelassen ist nur Typ-3 Chomsky Grammatik; abweichende Eingaben erzeugen kein definiertes Verhalten.
Der Aufruf des Programms geschieht wie folgt:

python grammar_check.py file 'word'

In file ist die geforderte Grammatik zu definieren.
Einschränkungen hierbei stellen dar:
  Kontextfreiheit; Namen der Knoten: 0...n lückenlos (wie in Beispieldatei veranschaulicht); keine nichtleere-Schnittmenge der Knoten-Namen und der 
  Zeichenmenge.
