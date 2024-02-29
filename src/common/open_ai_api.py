from typing import Optional

from openai import OpenAI
from openai.types.beta import Assistant

from src.common.utils import get_env

client = OpenAI(api_key=get_env("OPENAI_KEY"))

assistant: Optional[Assistant] = None


def get_assistant() -> Assistant:
    global assistant
    if assistant is None:
        assistant = client.beta.assistants.retrieve(get_env("OPENAI_ASSISTANT_ID"))
        return assistant
    else:
        return assistant
