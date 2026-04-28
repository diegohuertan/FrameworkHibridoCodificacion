import openai
import google.generativeai as genai
from groq import Groq
from typing import Tuple


def invocar_groq(api_key: str, modelo: str, system_prompt: str, user_prompt: str, temperatura: float) -> Tuple[str, int, int]:
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt}, 
            {"role": "user", "content": user_prompt}
        ],
        model=modelo, 
        temperature=temperatura
    )
    texto = response.choices[0].message.content.strip()
    tokens_input = response.usage.prompt_tokens
    tokens_output = response.usage.completion_tokens
    return texto, tokens_input, tokens_output

def invocar_openai(api_key: str, modelo: str, system_prompt: str, user_prompt: str, temperatura: float) -> str:
    client = openai.OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
        model=modelo, temperature=temperatura
    )
    return response.choices[0].message.content.strip()

def invocar_gemini(api_key: str, modelo: str, system_prompt: str, user_prompt: str, temperatura: float) -> str:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name=modelo,
        system_instruction=system_prompt
    )
    response = model.generate_content(
        user_prompt,
        generation_config=genai.types.GenerationConfig(temperature=temperatura)
    )
    return response.text.strip()