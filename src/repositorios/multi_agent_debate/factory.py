from pathlib import Path
from .config.mad_settings import settings
from .core.llm_wrappers import invocar_groq  
from .core.analista import Analista
from .core.critico import Critico
from .core.juez import Juez
from .subsistema_debate import SubSistemaDebate # Importamos el Ring
from .orquestador_mad import OrquestadorMAD

class MADFactory:
    @staticmethod
    def _cargar_prompt(nombre_archivo: str) -> str:
        ruta = Path(__file__).parent / "prompts" / nombre_archivo
        with open(ruta, "r", encoding="utf-8") as f:
            return f.read()

    @classmethod
    def crear_sistema_completo(cls) -> OrquestadorMAD:
        # 1. Carga de munición (Prompts MD)
        p_analista = cls._cargar_prompt("analista.md")
        p_critico = cls._cargar_prompt("critico.md")
        p_juez = cls._cargar_prompt("juez.md")

        # 2. Ensamblaje Familia 1 (Llama 3.3 70b)
        a1 = Analista(invocar_groq, settings.GROQ_API_KEY, "llama-3.3-70b-versatile", p_analista)
        c1 = Critico(invocar_groq, settings.GROQ_API_KEY, "llama-3.3-70b-versatile", p_critico)
        sub_a = SubSistemaDebate(analista=a1, critico=c1, max_rondas=settings.MAX_RONDAS_DEBATE)

        # 3. Ensamblaje Familia 2 (Llama 3 8b)
        a2 = Analista(invocar_groq, settings.GROQ_API_KEY, "llama-3.3-70b-versatile", p_analista)
        c2 = Critico(invocar_groq, settings.GROQ_API_KEY, "llama-3.3-70b-versatile", p_critico)
        sub_b = SubSistemaDebate(analista=a2, critico=c2, max_rondas=settings.MAX_RONDAS_DEBATE)

        # 4. El Juez
        juez = Juez(invocar_groq, settings.GROQ_API_KEY, "llama-3.3-70b-versatile", p_juez)

        # 5. Entrega al Orquestador: Inyectamos los Subsistemas ya armados
        return OrquestadorMAD(
            subsistema_a=sub_a,
            subsistema_b=sub_b,
            juez=juez
        )