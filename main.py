import logging
import os
import sys

# Ajustar el path para que el kernel encuentre la raíz 'src'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Imports de Élite: Limpios, directos y soberanos
from src.core import PropiedadListada
from src.repositorios.ac_plt.repository import ACPLTRepository
from src.repositorios import PoliticaACPLT, PoliticaMaestra
from src.servicios.orquestador import OrquestadorClasificacionService

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_staging_test():
    logging.info("=== KERNEL BOOT SEQUENCE: MODE STAGING ===")
    
    # 1. Motor Primario (Carga el .pkl unificado)
    motor_primario = ACPLTRepository()
    
    # 2. El Juez (Política de confianza)
    mapa_leyes = {
        "AC-PLT": PoliticaACPLT(umbral_distancia=0.05) 
    }
    juez_supremo = PoliticaMaestra(mapa_leyes)
    
    # 3. Orquestador (El cerebro del Framework)
    orquestador = OrquestadorClasificacionService(
        motores=[motor_primario], 
        politica=juez_supremo
    )
    
    # 4. Payload de prueba
    lote = [
        PropiedadListada(concepto="granito", texto_crudo="seco"),
        PropiedadListada(concepto="cáscara", texto_crudo="proteger"), 
    ]
    


    # 5. Ejecución del Pipeline
    logging.info("Inyectando datos en el Pipeline Hexagonal...")
    resultados = orquestador.ejecutar(lote)
    
    # 6. Reporte de Telemetría
    print("\n" + "="*40)
    print("      RESULTADOS DE CLASIFICACIÓN")
    print("="*40)
    for i, etiqueta in enumerate(resultados):
        dist = etiqueta.metricas.get("distancia_knn", 0.0)
        print(f"[{i+1}] {etiqueta.codigo:<15} | Dist: {dist:.4f} | Origen: {etiqueta.origen}")
    print("="*40)

if __name__ == "__main__":
    run_staging_test()