import logging
from .subsistema_debate import SubSistemaDebate
from .core.juez import Juez
from typing import Tuple


class OrquestadorMAD:
    """
    El General en el campo de batalla. 
    Coordina la ejecución paralela de las dos familias y el dictamen final del Juez.
    """
    def __init__(self, subsistema_a: SubSistemaDebate, subsistema_b: SubSistemaDebate, juez: Juez):
        # Inyección de dependencias pura: el Orquestador no instancia nada, recibe todo armado.
        self.subsistema_a = subsistema_a
        self.subsistema_b = subsistema_b
        self.juez = juez
    def ejecutar_flujo_completo(self, propiedad: str, concepto_padre: str) -> Tuple[str, str, int, int]:
        t_in_final = 0
        t_out_final = 0

        propuesta_a, a_in, a_out = self.subsistema_a.ejecutar(propiedad, concepto_padre)
        t_in_final += a_in
        t_out_final += a_out
        
        if "ERROR_API" in propuesta_a:
            return "ERROR_API", f"Falla Familia 1: {propuesta_a}", t_in_final, t_out_final

        propuesta_b, b_in, b_out = self.subsistema_b.ejecutar(propiedad, concepto_padre)
        t_in_final += b_in
        t_out_final += b_out
        
        if "ERROR_API" in propuesta_b:
            return "ERROR_API", f"Falla Familia 2: {propuesta_b}", t_in_final, t_out_final

        veredicto, j_in, j_out = self.juez.dictaminar(
            propiedad=propiedad, 
            concepto_padre=concepto_padre, 
            propuesta_a=propuesta_a, 
            propuesta_b=propuesta_b
        )
        t_in_final += j_in
        t_out_final += j_out

        # EL HACK: Extraemos el código real aquí mismo
        codigo_final = "ERROR_PARSING_JUEZ"
        if "Familia A" in veredicto:
            codigo_final = propuesta_a
        elif "Familia B" in veredicto:
            codigo_final = propuesta_b

        return codigo_final, veredicto, t_in_final, t_out_final