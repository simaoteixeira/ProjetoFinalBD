from enum import Enum

from projeto.utils import forDjango


@forDjango
class MOVEMENTTYPES(Enum):
    IN = 'Entrada'
    OUT = 'Saída'

class PRODUCTIONORDERSTATUS(Enum):
    WAITING_PROD = "WAITING_PROD"
    IN_PROD = "IN_PROD"
    COMPLETED = "COMPLETED"
    CANCELED = "CANCELED"