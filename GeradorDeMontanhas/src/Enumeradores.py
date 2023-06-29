from enum import IntEnum, unique

@unique
class PontosCardeais(IntEnum):
    Norte = 0
    Leste = 1
    Sul = 2
    Oeste = 3

@unique
class Regioes(IntEnum):
    NL = 0
    SL = 1
    NO = 2
    SO = 3

@unique
class Posicionamento(IntEnum):
    Topo = 0
    Reta = 1
    Base = 2
    EntornoMontanha = 3
    Montanha = 4