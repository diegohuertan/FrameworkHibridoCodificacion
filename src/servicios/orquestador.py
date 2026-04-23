import logging
from typing import List
from src.core import PropiedadListada, EtiquetaSemantica
from src.puertos import IProcesarLoteService, IClasificadorRepository, IPoliticaAceptacion

# Logs para el orquestador
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class OrquestadorClasificacionService(IProcesarLoteService):
    def __init__(self, 
                 motores: List[IClasificadorRepository], 
                 politica: IPoliticaAceptacion):
        if not motores:
            raise ValueError("KERNEL PANIC: No puedes iniciar el servicio sin motores de clasificación.")
        
        self.motores = motores
        self.politica = politica

    def ejecutar(self, lote: List[PropiedadListada]) -> List[EtiquetaSemantica]:
        if not lote:
            logging.warning("Lote vacío recibido. Abortando misión.")
            return []

        logging.info(f"Iniciando Pipeline con {len(self.motores)} motores. Lote inicial: {len(lote)} unidades.")
        
        etiquetas_finales = []
        lote_actual = lote 

        for indice, motor in enumerate(self.motores):
            if not lote_actual:
                logging.info("Pipeline completado prematuramente: Lote totalmente clasificado.")
                break

            logging.info(f"Ejecutando Motor {indice + 1}: {type(motor).__name__}")
            
            resultados_motor = motor.clasificar_lote(lote_actual)
            
            lote_siguiente = []
            es_ultimo_motor = (indice == len(self.motores) - 1)

            for propiedad, etiqueta in zip(lote_actual, resultados_motor):
                
                if self.politica.es_aceptable(etiqueta) or es_ultimo_motor:
                    etiquetas_finales.append(etiqueta)
                else:
                    lote_siguiente.append(propiedad)

            logging.info(f"Motor {indice + 1} resolvió {len(lote_actual) - len(lote_siguiente)} propiedades.")
            lote_actual = lote_siguiente

        logging.info(f"Procesamiento finalizado. Etiquetas generadas: {len(etiquetas_finales)}")
        return etiquetas_finales