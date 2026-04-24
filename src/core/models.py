from dataclasses import dataclass, field
from typing import Optional, Dict

@dataclass(frozen=True)
class PropiedadListada:
    """
    Value Object (Inmutable). 
    Representa la entrada pura del sistema (ej. fila de un CPN).
    """
    concepto: str
    texto_crudo: str

@dataclass(frozen=True)
class EtiquetaSemantica:
    """
    Value Object (Inmutable). 
    Representa la salida estandarizada del sistema.
    """
    codigo: str
    origen: str
    metricas: Dict[str, float] = field(default_factory=dict)
    razonamiento: Optional[str] = None