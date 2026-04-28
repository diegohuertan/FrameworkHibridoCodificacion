import logging
import time
from typing import List
from src.core.models import PropiedadListada, EtiquetaSemantica
from src.puertos.interfaces import IClasificadorRepository
from .factory import MADFactory

class MADRepository(IClasificadorRepository):
    def __init__(self):
        logging.info("Levantando Kernel MAD (Multi-Agent Debate)...")
        try:
            self.orquestador = MADFactory.crear_sistema_completo()
            logging.info("Motor MAD en Staging: Operativo y Multicloud.")
        except Exception as e:
            logging.error(f"BOOT ERROR en MAD: No se pudo ensamblar el motor: {e}")
            raise e

    def clasificar_lote(self, lote: List[PropiedadListada]) -> List[EtiquetaSemantica]:
        if not lote:
            return []
        
        resultados = []
        for propiedad in lote:
            # Ahora recibimos 4 variables, incluyendo el código limpio
            codigo_final, razonamiento, t_in, t_out = self.orquestador.ejecutar_flujo_completo(
                propiedad=propiedad.texto_crudo,
                concepto_padre=propiedad.concepto
            )
            
            etiqueta = EtiquetaSemantica(
                codigo=codigo_final,
                origen="MAD-MultiAgent",
                metricas={
                    "debate_completo": True,
                    "tokens_in": t_in,
                    "tokens_out": t_out,
                    "tokens_total": t_in + t_out
                },
                razonamiento=razonamiento
            )
            resultados.append(etiqueta)
            time.sleep(2)
            
        return resultados
    
    def _parsear_veredicto_a_dto(self, veredicto: str, t_in: int, t_out: int) -> EtiquetaSemantica:        
        lineas = veredicto.split('\n')
        codigo_final = "ERROR_PARSING"
        
        for linea in lineas:
            if "Gana" in linea or "Veredicto" in linea:
                codigo_final = linea.split(":")[-1].strip()
                break

        return EtiquetaSemantica(
            codigo=codigo_final,
            origen="MAD-MultiAgent",
            metricas={
                "debate_completo": True,
                "tokens_in": t_in,
                "tokens_out": t_out,
                "tokens_total": t_in + t_out
            },
            razonamiento=veredicto
        )