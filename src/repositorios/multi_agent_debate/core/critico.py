from typing import Callable, Tuple
from .agent_base import AgenteBase

class Critico(AgenteBase):
    def __init__(self, motor_llm: Callable, api_key: str, modelo: str, system_prompt: str, temperatura: float = 0.0):
        super().__init__(motor_llm, api_key, modelo, temperatura)
        self.system_prompt = system_prompt

    def evaluar(self, propiedad: str, concepto_padre: str, codigo_propuesto: str) -> Tuple[str, int, int]:
        user_prompt = f"CONCEPTO PADRE: [{concepto_padre.upper()}]\n"
        user_prompt += f"FRASE ORIGINAL DEL PARTICIPANTE: '{propiedad}'\n"
        user_prompt += f"CÓDIGO PROPUESTO POR ANALISTA: '{codigo_propuesto}'\n\n"
        user_prompt += "INSTRUCCIÓN: Aplica tu pipeline de auditoría. Responde ÚNICAMENTE 'OK' si es perfecto, o 'RECHAZADO: [motivo]' si falla en cualquier criterio."
            
        return self.invocar_llm(system_prompt=self.system_prompt, user_prompt=user_prompt)