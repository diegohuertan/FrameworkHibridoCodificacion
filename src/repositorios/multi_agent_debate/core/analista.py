from typing import Callable, Tuple
from .agent_base import AgenteBase

class Analista(AgenteBase):
    def __init__(self, motor_llm: Callable, api_key: str, modelo: str, system_prompt: str, temperatura: float = 0.1):
        super().__init__(motor_llm, api_key, modelo, temperatura)
        self.system_prompt = system_prompt

    def procesar(self, propiedad: str, concepto_padre: str, historia_debate: str = None) -> Tuple[str, int, int]:
        """Arma el payload (User Prompt) y dispara el LLM."""
        
        user_prompt = f"CONCEPTO PADRE: [{concepto_padre.upper()}]\nFRASE ORIGINAL: '{propiedad}'\n"
        
        if historia_debate:
            user_prompt += f"\nDEBATE PREVIO:\n{historia_debate}\n\nNUEVA INSTRUCCIÓN: Tu propuesta anterior fue rechazada. Genera un nuevo código solucionando las críticas (1 a 3 palabras máximo)."
        else:
            user_prompt += "\nINSTRUCCIÓN: Genera el código CPN inicial siguiendo tu pipeline (1 a 3 palabras máximo)."
            
        texto, t_in, t_out = self.invocar_llm(system_prompt=self.system_prompt, user_prompt=user_prompt)
        
        return texto, t_in, t_out