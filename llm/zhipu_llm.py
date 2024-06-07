from typing import Union, List
from llm.utils import num_tokens_from_messages
from openai import AzureOpenAI, OpenAI
from config import Config
from llm.text_generator import TextGenerator
from zhipuai import ZhipuAI

config = Config()


class ZhiPuTextGenerator(TextGenerator):
    def __init__(
            self,
            base_url: str = config.BASE_URL,
            llm_type: str = config.LLM_TYPE,
            model_name: str = config.MODEL_NAME,
    ):
        super().__init__(llm_type=llm_type)
        self.client = None
        self.llm_type = llm_type
        self.model_name = model_name
        self.client = ZhipuAI(api_key=config.ZHIPU_API_KEY)

    def generate(
            self,
            messages: Union[List[dict], str],
    ):
        prompt_tokens = num_tokens_from_messages(messages)

        max_tokens = max(
            config.MODEL_LIST.get(self.model_name, 4096) - prompt_tokens - 10, 200
        )
        oai_config = {
            "model": "glm-4",
            # "max_tokens": max_tokens,
            # "top_p": 1.0,
            # "frequency_penalty": 0.0,
            # "presence_penalty": 0.0,
            # "n": 1,
            "messages": messages,
            "temperature": 0.01
        }

        oai_response = self.client.chat.completions.create(**oai_config)
        return oai_response
