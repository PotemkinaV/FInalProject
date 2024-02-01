from openai import OpenAI


class GPT:
    def __init__(self, api_key, model="gpt-3.5-turbo"):
        self.model = model
        self.client = OpenAI(api_key=api_key)
        self.prompt = "Суммаризируй следующий документ, рассказав самое важное о нем в три предложения:"

    @staticmethod
    def process_stream(stream):
        collected_chunks = []
        collected_messages = []
        for chunk in stream:
            collected_chunks.append(chunk)
            chunk_message = chunk.choices[0].delta.content
            collected_messages.append(chunk_message)
        collected_messages = [m for m in collected_messages if m is not None]
        full_reply_content = ''.join([m for m in collected_messages])
        return full_reply_content

    def summarize(self, text):
        new_message = {"role": "user", "content": self.prompt + text[:2048]}
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                new_message
            ]
        )
        return response.choices[0].message.content
