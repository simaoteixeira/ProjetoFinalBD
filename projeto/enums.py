from enum import Enum

from projeto.utils import forDjango


@forDjango
class MOVEMENTTYPES(Enum):
    IN = 'Entrada'
    OUT = 'Saída'