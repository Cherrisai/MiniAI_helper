import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


client = Groq(api_key=os.getenv('GROQ_API_KEY'))


def ask(
    prompt,
    system      = "You are a helpful assistant.",
    model       = "llama-3.3-70b-versatile",
    max_tokens  = 500,
    temperature = 0.7
):
    response = client.chat.completions.create(
        model    = model,
        messages = [
            {"role": "system", "content": system},
            {"role": "user",   "content": prompt}
        ],
        max_tokens  = max_tokens,
        temperature = temperature
    )
    return response.choices[0].message.content.strip()
