from dataclasses import dataclass
from typing import Optional

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
    confianza: float
    origen: str  # Ej: 'AC-PLT_kNN', 'MAD_GPT4', 'MAD_Claude3'
    razonamiento: Optional[str] = None  # Justificación del LLM si es necesario