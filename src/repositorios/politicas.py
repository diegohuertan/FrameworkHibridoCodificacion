import logging
from typing import Dict
from src.core import EtiquetaSemantica
from src.puertos import IPoliticaAceptacion

class PoliticaACPLT(IPoliticaAceptacion):
    """Especialista kNN: Aprueba si la distancia Euclidiana/Coseno es MENOR al umbral."""
    def __init__(self, umbral_distancia: float = 0.15):
        self.umbral_distancia = umbral_distancia

    def es_aceptable(self, etiqueta: EtiquetaSemantica) -> bool:
        distancia = etiqueta.metricas.get("distancia_knn", 1.0)
        es_valido = distancia < self.umbral_distancia
        
        if not es_valido:
            logging.debug(f"AC-PLT Rechazado: Distancia {distancia:.4f} > Umbral {self.umbral_distancia}")
            
        return es_valido

class PoliticaMAD(IPoliticaAceptacion):
    """Especialista Agentes: Aprueba si la relevancia Ragas es MAYOR al umbral."""
    def __init__(self, umbral_relevancia: float = 0.80):
        self.umbral_relevancia = umbral_relevancia

    def es_aceptable(self, etiqueta: EtiquetaSemantica) -> bool:
        relevancia = etiqueta.metricas.get("ragas_relevance", 0.0)
        es_valido = relevancia >= self.umbral_relevancia
        
        if not es_valido:
            logging.debug(f"MAD Rechazado: Relevancia {relevancia:.4f} < Umbral {self.umbral_relevancia}")
            
        return es_valido

class PoliticaMaestra(IPoliticaAceptacion):
    """El Router: Delega la validación según el origen de la etiqueta."""
    def __init__(self, mapa_politicas: Dict[str, IPoliticaAceptacion]):
        self.mapa_politicas = mapa_politicas

    def es_aceptable(self, etiqueta: EtiquetaSemantica) -> bool:
        juez_especialista = self.mapa_politicas.get(etiqueta.origen)
        
        if not juez_especialista:
            logging.error(f"Falla de Sistema: No hay política definida para el motor '{etiqueta.origen}'")
            return False
            
        return juez_especialista.es_aceptable(etiqueta)