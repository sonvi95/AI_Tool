from openai import OpenAI

class ModuleApi():
    def __init__(self):
        self.key_api = "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"
        self.client = OpenAI(api_key=self.key_api)
        self.model = "gpt-4o-mini"

    def send_message(self,message):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": message}
                ]
            )
            return response
        except Exception as e:
            print(e)

    def send_image(self,image_link,message):
        try:
            response = self.client.responses.create(
                model=self.model,
                input=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "input_text", "text": message},
                            {
                                "type": "input_image",
                                "image_url": image_link
                            }
                        ]
                    }
                ]
            )
            return response
        except Exception as e:
            print(e)

MODULE_API = ModuleApi()