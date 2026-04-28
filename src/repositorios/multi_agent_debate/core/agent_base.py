import logging
from typing import Callable, Tuple
import time

class AgenteBase:
    def __init__(self, motor_llm: Callable, api_key: str, modelo: str, temperatura: float = 0.0):
        self.motor_llm = motor_llm  
        self.api_key = api_key
        self.modelo = modelo
        self.temperatura = temperatura

    def invocar_llm(self, system_prompt: str, user_prompt: str) -> Tuple[str, int, int]:
        try:
            time.sleep(3.5)
            respuesta, t_in, t_out = self.motor_llm(
                api_key=self.api_key,
                modelo=self.modelo,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperatura=self.temperatura
            )
            return respuesta, t_in, t_out
            
        except Exception as e:
            error_msg = f"ERROR_API: {str(e)}" 
            logging.error(f"ERROR_KERNEL_MAD: Falla en el motor base. Detalle: {str(e)}")
            return error_msg, 0, 0