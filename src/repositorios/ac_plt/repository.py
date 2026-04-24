import sys
import os
import joblib
import logging
from typing import List
from sentence_transformers import SentenceTransformer

from src.core.models import PropiedadListada, EtiquetaSemantica
from src.puertos.interfaces import IClasificadorRepository

# Conexión al legacy
DIRECTORIO_ACTUAL = os.path.dirname(os.path.abspath(__file__))
sys.path.append(DIRECTORIO_ACTUAL)

try:
    from functions.text_cleaning import TextCleaner
except ImportError as e:
    logging.error(f"KERNEL ERROR: No se pudo cargar el módulo de limpieza: {e}")


class ACPLTRepository(IClasificadorRepository):
    def __init__(self):
        path_binario = os.path.join(DIRECTORIO_ACTUAL, "acplt_core_unificado.pkl")
        if not os.path.exists(path_binario):
            raise FileNotFoundError(f"BOOT ERROR: No se encontró el binario en {path_binario}.")
        
        logging.info("Levantando Kernel AC-PLT...")
        datos = joblib.load(path_binario)
        self.knn = datos["modelo_knn"]
        
        # 2. Inicializar Modelos
        self.encoder = SentenceTransformer('intfloat/e5-base-v2')
        self.cleaner = TextCleaner(nlp="es_core_news_sm", language="spanish")
        logging.info("Motor AC-PLT en Staging: Operativo.")

    def clasificar_lote(self, lote: List[PropiedadListada]) -> List[EtiquetaSemantica]:
        """Orquesta el pipeline de clasificación sin tocar la lógica matemática."""
        if not lote: return []
        
        textos_limpios = self._sanitizar_textos(lote)
        vectores = self._vectorizar(textos_limpios)
        distancias, indices = self._ejecutar_inferencia(vectores)
        
        return self._empaquetar_dtos(distancias, indices)

    def _sanitizar_textos(self, lote: List[PropiedadListada]) -> List[str]:
        """Aplica la limpieza legacy de Spacy."""
        limpios = []
        for p in lote:
            tokens = self.cleaner.clean_text(str(p.texto_crudo))
            limpios.append(" ".join([t.text for t in tokens]))
        return limpios

    def _vectorizar(self, textos: List[str]):
        """Transforma texto plano a coordenadas E5."""
        return self.encoder.encode(textos, show_progress_bar=False)

    def _ejecutar_inferencia(self, vectores):
        """Busca el vecino más cercano en la memoria del kNN."""
        return self.knn.kneighbors(vectores)

    def _empaquetar_dtos(self, distancias, indices) -> List[EtiquetaSemantica]:
        """Traduce la salida matemática bruta a los Maletines del Framework."""
        resultados = []
        for i, (dist, idx) in enumerate(zip(distancias, indices)):
            codigo_asignado = self.knn.classes_[idx[0]]
            
            etiqueta = EtiquetaSemantica(
                codigo=codigo_asignado,
                metricas={"distancia_knn": float(dist[0])},
                origen="AC-PLT",
                razonamiento=f"Top-1 kNN. Distancia: {dist[0]:.4f}"
            )
            resultados.append(etiqueta)
        return resultados