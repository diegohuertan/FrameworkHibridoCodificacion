import os
from pathlib import Path
from dotenv import load_dotenv

# Localización dinámica basada en la posición de este archivo
# Ajusta el número en parents[] si cambias el archivo de lugar
try:
    ROOT_DIR = Path(__file__).resolve().parents[4] 
    ENV_PATH = ROOT_DIR / ".env"
except IndexError:
    # Fallback por si ejecutas desde un entorno con menos profundidad
    ENV_PATH = Path(".env").resolve()

# Carga forzada
load_dotenv(dotenv_path=ENV_PATH)

class MADSettings:
    """Centraliza todas las variables de entorno para el motor MAD."""
    
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GPT_API_KEY: str = os.getenv("GPT_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    MAX_RONDAS_DEBATE: int = int(os.getenv("MAX_RONDAS_DEBATE", "2"))
    UMBRAL_CONFIANZA_JUEZ: float = float(os.getenv("UMBRAL_CONFIANZA_JUEZ", "0.85"))

    @classmethod
    def validar_keys_minimas(cls):
        """Verifica que al menos tengamos Groq para poder operar el kernel."""
        if not cls.GROQ_API_KEY:
            # Imprimimos la ruta absoluta para debuggear en el terminal
            print(f"DEBUG: Buscando .env en -> {ENV_PATH}")
            raise ValueError(f"KERNEL PANIC: No se encontró GROQ_API_KEY en el .env (Ruta: {ENV_PATH})")

# Instancia global
settings = MADSettings()
settings.validar_keys_minimas()