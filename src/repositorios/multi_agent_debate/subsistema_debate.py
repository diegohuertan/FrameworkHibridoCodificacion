import logging
from typing import Tuple
from .core.analista import Analista
from .core.critico import Critico

class SubSistemaDebate:
    def __init__(self, analista: Analista, critico: Critico, max_rondas: int = 3):
        self.analista = analista
        self.critico = critico
        self.max_rondas = max_rondas

    def ejecutar(self, propiedad: str, concepto_padre: str) -> Tuple[str, int, int]:
        historia_debate = ""
        propuesta_actual = ""
        t_in_total = 0
        t_out_total = 0
        
        for ronda in range(1, self.max_rondas + 1):
            historial_a_pasar = historia_debate if ronda > 1 else None
            propuesta_actual, a_in, a_out = self.analista.procesar(propiedad, concepto_padre, historial_a_pasar)
            t_in_total += a_in
            t_out_total += a_out
            
            if "ERROR_API" in propuesta_actual:
                return propuesta_actual, t_in_total, t_out_total
            
            critica, c_in, c_out = self.critico.evaluar(propiedad, concepto_padre, propuesta_actual)
            t_in_total += c_in
            t_out_total += c_out
            
            if "ERROR_API" in critica:
                return critica, t_in_total, t_out_total
            
            if "OK" in critica.upper() or critica.strip() == "":
                return propuesta_actual, t_in_total, t_out_total
            
            historia_debate += f"- Ronda {ronda}: Propuesta='{propuesta_actual}', Crítica='{critica}'\n"

        return propuesta_actual, t_in_total, t_out_total