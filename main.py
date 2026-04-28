import logging
import os
import sys

# 1. Alineación de Path (Soberanía de directorios)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Imports de Dominio
from src.core.models import PropiedadListada
# Importamos el nuevo Repositorio (ajusta el path si es necesario)
from src.repositorios.multi_agent_debate.repository import MADRepository

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_production_test():
    logging.info("=== KERNEL BOOT SEQUENCE: MODE REPOSITORY-MAD ===")
    
    # 1. Instanciar el Repositorio MAD (Aquí la Factory hace su magia internamente)
    try:
        repo_mad = MADRepository()
    except Exception:
        logging.error("Falla crítica en el despliegue del repositorio.")
        return

    # 2. Carga de Payload (Simulando lo que vendría del CPN)

    lote_prueba = [
    # 1. Abstracto de alta ambigüedad (Gold Standard: PERDÓN)
    PropiedadListada(
        concepto="Compasión", 
        texto_crudo="por lo que se le perdona la vida a alguien en las peliculas"
    ),
    # 2. Abstracto descriptivo (Gold Standard: FIJACIÓN)
    PropiedadListada(
        concepto="Obsesión", 
        texto_crudo="fijación mantenida en el tiempo con un objeto o persona"
    ),
    # 3. Asociación de Acción (Gold Standard: PROTECCIÓN)
    PropiedadListada(
        concepto="Cáscara", 
        texto_crudo="proteger"
    ),
    # 4. Mapeo Organizacional (Gold Standard: EMPRESA)
    PropiedadListada(
        concepto="Entidad", 
        texto_crudo="asociación de personas que se dedican a hacer algo"
    ),
    # 5. Atributo directo (Gold Standard: LENTITUD)
    PropiedadListada(
        concepto="Caracol", 
        texto_crudo="lento"
    )
]

    # 3. Ejecución a través de la Interfaz (Clasificar Lote)
    logging.info(f"Inyectando lote de {len(lote_prueba)} propiedades al motor MAD...")
    
    try:
        etiquetas = repo_mad.clasificar_lote(lote_prueba)
        
        # 4. Reporte de Telemetría Final
        print("\n" + "═"*60)
        print("      RESULTADOS FINALES DEL REPOSITORIO MAD")
        print("═"*60)
        
        for i, etiqueta in enumerate(etiquetas):
            print(f"Propiedad [{i+1}]: {lote_prueba[i].texto_crudo}")
            print(f"Código CPN: {etiqueta.codigo}")
            print(f"Origen:     {etiqueta.origen}")
            print(f"Métricas:   {etiqueta.metricas}")
            print("-" * 40)
            # Descomentar si quieres ver todo el "choclo" de la pelea
            # print(f"Razonamiento:\n{etiqueta.razonamiento}\n")
        
        print("═"*60)

    except Exception as e:
        logging.error(f"Error durante la clasificación por lote: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_production_test()