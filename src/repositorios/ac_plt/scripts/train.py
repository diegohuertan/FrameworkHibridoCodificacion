import pandas as pd
import joblib
import os
import sys
from sentence_transformers import SentenceTransformer
from sklearn.neighbors import KNeighborsClassifier

# =====================================================================
# EL CABLEADO TÁCTICO
# =====================================================================
DIRECTORIO_ACTUAL = os.path.dirname(os.path.abspath(__file__))
DIRECTORIO_PADRE = os.path.dirname(DIRECTORIO_ACTUAL)
sys.path.append(DIRECTORIO_PADRE)

try:
    from functions.text_cleaning import TextCleaner  # <-- IMPORTAMOS LA CLASE
except ImportError as e:
    print(f"\n[!] KERNEL PANIC: No pude importar la clase 'TextCleaner'.")
    print(f"[!] Error exacto: {e}\n")
    sys.exit(1)

def forjar_motor_unificado():
    print("=== INICIANDO FORJA DE MOTOR UNIFICADO (CPN120 + CPN27) ===")
    
    ruta_cpn120 = os.path.join(DIRECTORIO_PADRE,"functions", "data", "CPN120_normalize.csv")
    ruta_cpn27 = os.path.join(DIRECTORIO_PADRE,"functions", "data", "CPN27_normalize.csv")

    if not os.path.exists(ruta_cpn120):
        print(f"Error: No encuentro el CSV en {ruta_cpn120}")
        sys.exit(1)

    df_120 = pd.read_csv(ruta_cpn120)
    df_27 = pd.read_csv(ruta_cpn27)
    df_master = pd.concat([df_120, df_27], ignore_index=True)
    df_master = df_master.dropna().reset_index(drop=True)
    print(f"Datos fusionados: {len(df_master)} propiedades.")

    print("Inicializando TextCleaner legacy (Spacy)...")
    # Inicializamos la clase como lo pedía el archivo main.yaml original
    cleaner = TextCleaner(nlp="es_core_news_sm", language="spanish")

    print("Limpiando textos...")
    # Usamos el método de la clase
    textos_limpios = []
    for texto in df_master.iloc[:, 1].tolist():
        # La caja negra devuelve una lista de tokens, los volvemos a unir en un string
        tokens = cleaner.clean_text(str(texto))
        textos_limpios.append(" ".join([t.text for t in tokens]))        
    etiquetas = df_master.iloc[:, 2].tolist()

    print("Levantando Kernel E5 de HuggingFace...")
    model = SentenceTransformer('intfloat/e5-base-v2')
    X_train = model.encode(textos_limpios, show_progress_bar=True)

    print("Alineando neuronas del kNN...")
    knn = KNeighborsClassifier(n_neighbors=1, metric='cosine')
    knn.fit(X_train, etiquetas)

    ruta_binario = os.path.join(DIRECTORIO_PADRE, "acplt_core_unificado.pkl")
    joblib.dump({"modelo_knn": knn}, ruta_binario)
    
    print(f"✅ ¡FORJA COMPLETADA! Binario maestro guardado en: {ruta_binario}")

if __name__ == "__main__":
    forjar_motor_unificado()