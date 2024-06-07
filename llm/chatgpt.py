from typing import Union, List
from llm.utils import num_tokens_from_messages
from openai import AzureOpenAI, OpenAI
from config import Config
from llm.text_generator import TextGenerator

config = Config()


class ChatGPTTextGenerator(TextGenerator):
    def __init__(
            self,
            api_key: str = config.API_KEY,
            base_url: str = config.BASE_URL,
            llm_type: str = config.LLM_TYPE,
            model_name: str = config.MODEL_NAME,
    ):
        super().__init__(llm_type=llm_type)
        self.client = None
        self.llm_type = llm_type
        self.model_name = model_name

        client_args = {
            "api_key": api_key,
            "base_url": base_url
        }
        if llm_type == 'openai':
            self.client = OpenAI(**client_args)

    def generate(
            self,
            messages: Union[List[dict], str],
    ):
        prompt_tokens = num_tokens_from_messages(messages)

        max_tokens = max(
            config.MODEL_LIST.get(self.model_name, 4096) - prompt_tokens - 10, 200
        )


        return self.client.chat.completions.create(
                model= self.model_name,
                messages=messages,
                stream=False)


