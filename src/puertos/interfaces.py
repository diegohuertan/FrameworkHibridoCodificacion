from abc import ABC, abstractmethod
from typing import List
from src.core import PropiedadListada, EtiquetaSemantica

class IProcesarLoteService(ABC):
    """Puerto Inbound: Lo que tu script o API llama para iniciar el proceso."""
    @abstractmethod
    def ejecutar(self, lote: List[PropiedadListada]) -> List[EtiquetaSemantica]:
        pass

class IClasificadorRepository(ABC):
    """Puerto Outbound: El contrato que obliga a los motores a devolver el DTO."""
    @abstractmethod
    def clasificar_lote(self, lote: List[PropiedadListada]) -> List[EtiquetaSemantica]:
        pass

class IPoliticaAceptacion(ABC):
    """Puerto Policy: El contrato del Juez para validar las métricas dinámicas."""
    @abstractmethod
    def es_aceptable(self, etiqueta: EtiquetaSemantica) -> bool:
        pass