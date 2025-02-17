from ollama import chat
from ollama import ChatResponse

# Run 'ollama run llama3.2' on a terminal

def LLNModel(text: str)->str:
    response: ChatResponse = chat(model='llama3.2', messages=[
    {
        'role': 'user',
        'content': f'{text}\nQuiero que me des la descripción que te acabo de dar mejor redactada pero sin que se alargue. Edítala lo mínimo posible intentando conectar las diferentes oraciones, no agreges nada extra. Tu respuesta debe ser únicamente la descripción, no digas nada extra.',
    },
    ])
    return response.message.content