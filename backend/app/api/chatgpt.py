import openai

openai.api_key = "your_openai_api_key"

def chat_with_gpt(prompt):
    response = openai.Chat.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
)
    return response.choices[0].message['content']
