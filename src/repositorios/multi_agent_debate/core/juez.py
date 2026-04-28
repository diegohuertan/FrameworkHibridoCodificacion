import random
from typing import Callable, Tuple
from .agent_base import AgenteBase

class Juez(AgenteBase):
    def __init__(self, motor_llm: Callable, api_key: str, modelo: str, system_prompt: str, temperatura: float = 0.0):
        super().__init__(motor_llm, api_key, modelo, temperatura)
        self.system_prompt = system_prompt

    def dictaminar(self, propiedad: str, concepto_padre: str, propuesta_a: str, propuesta_b: str) -> Tuple[str, int, int]:
        opciones = [
            {"id": "A", "codigo": propuesta_a},
            {"id": "B", "codigo": propuesta_b}
        ]
        random.shuffle(opciones)
        
        opcion_1 = opciones[0]
        opcion_2 = opciones[1]
        
        user_prompt = f"CONCEPTO PADRE: [{concepto_padre.upper()}]\n"
        user_prompt += f"FRASE CRUDA DEL PARTICIPANTE: '{propiedad}'\n\n"
        user_prompt += f"OPCIÓN 1: '{opcion_1['codigo']}'\n"
        user_prompt += f"OPCIÓN 2: '{opcion_2['codigo']}'\n\n"
        user_prompt += "INSTRUCCIÓN: Evalúa objetivamente y entrega los puntajes y el veredicto estrictamente en el formato de 4 líneas solicitado."
        
        respuesta_cruda, t_in, t_out = self.invocar_llm(system_prompt=self.system_prompt, user_prompt=user_prompt)
        
        if "ERROR_API" in respuesta_cruda:
            return respuesta_cruda, t_in, t_out
            
        respuesta_procesada = respuesta_cruda.replace("Opción 1", f"Opción 1 (Familia {opcion_1['id']})")
        respuesta_procesada = respuesta_procesada.replace("Opción 2", f"Opción 2 (Familia {opcion_2['id']})")
        
        return respuesta_procesada, t_in, t_out