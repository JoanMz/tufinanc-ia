import anthropic
client = anthropic.Anthropic()

messages = client.messages.create(
    model="claude-3-5-haiku-20241022",
    max_tokens=1000,
    temperature=1,
    system="You are a world-class poet. Respond only with short poems.",
    messages=[
        {
            "role": "user",
            "content": [{"type":"text",
                         "text":"What is the capital of France?"}]
        }
    ]
)
print(messages.content)