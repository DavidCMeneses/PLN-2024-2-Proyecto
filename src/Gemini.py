from google import genai
from google.genai import types

# Replace with your Gemini API key
print('\033[32mIniciando Modelo GEMINI...\033[0m')
api_key = ''
with open('./src/GeminiKey.txt') as file_key:
    api_key = file_key.readline()
file_key.close()

client = genai.Client(api_key=api_key)
print('\033[32mModelo GEMINI listo!\033[0m')

def GeminiModel(text: str)->str:
    response = client.models.generate_content(
        model="gemini-1.5-pro",
        config=types.GenerateContentConfig(
            system_instruction='Tu trabajo es corregir la redacción de una descripción sin cambiar ninguna de las palabras existentes. Puedes agregar conectores para darle sentido al texto.'),
        contents=[text]
    )
    return response.text