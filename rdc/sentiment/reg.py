import re

sensitive = [
    (re.compile(r"Y(O)+"), 1),
    (re.compile(r"WE(N)+"), 1),
    (re.compile(r"NO WA(Y)+"), 7),
    (re.compile(r"YESSI(R)+"), 0),
    (re.compile(r"AY(E)+"), 0),
    (re.compile(r"LO(L)+"), 2),
    (re.compile(r"LMFA(O)+"), 2),
    (re.compile(r"LMA(O)+"), 2)
]

insensitive = [
    (re.compile(r"\bso sorry\b"), 5),
    (re.compile(r"\blma(o)+\b"), 0),
    (re.compile(r"\blmfa(o)+\b"), 0),
    (re.compile(r"\bbig bro\b"), 0),
    (re.compile(r"\b(w)+\b"), 0),
    (re.compile(r"\blo(l)+\b"), 3),
    (re.compile(r"\bwo(w)+\b"), 7),
    (re.compile(r"\bno way\b"), 7),
    (re.compile(r"\byessi(r)+\b"), 0),
    (re.compile(r"\bgood shit\b"), 2),
    (re.compile(r"\bwe(n)+\b"), 0),
    (re.compile(r"\bgoated\b"), 0),
    (re.compile(r"\btuf(f)+\b"), 0),
    (re.compile(r"\by(o)+\b"), 0),
    (re.compile(r"\bcome o(n)+\b"), 4),
    (re.compile(r"\bcmo(n)+\b"), 4),
    (re.compile(r"\bmickey\b"), 5)
]

general_emotes = [
    (re.compile(r"\bDinoDance\b"), 0),
    (re.compile(r"\bGriddyGoose\b"), 0),
    (re.compile(r"\bVoteYea\b"), 0)
]

rdc_emotes = [
    (re.compile(r"\brdcFantastic\b"), 0),
    (re.compile(r"\brdcJayRich\b"), 0),
    (re.compile(r"\brdcDiddyLee\b"), 0),
    (re.compile(r"\brdcWohn\b"), 0),
    (re.compile(r"\brdcDreamGang\b"), 0),
    (re.compile(r"\brdcWark\b"), 0),
    (re.compile(r"\brdcWylan\b"), 0),
    (re.compile(r"\brdcWewand\b"), 0),
    (re.compile(r"\brdcWes\b"), 0),
    (re.compile(r"\brdcWen\b"), 0),
    (re.compile(r"\brdcSalute\b"), 0)
]
