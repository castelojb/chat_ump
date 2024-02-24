from typing import Optional

from openai.types.beta import Thread
from openai.types.beta.threads import ThreadMessage, Run

from src.common.open_ai_api import client, get_assistant


def get_new_thread() -> Thread:
    """Creating a thread, it will be associated to an assistant during the run step"""
    thread = client.beta.threads.create()
    return thread


def add_message_to_thread(thread_id: str, content: str) -> ThreadMessage:
    """Append a new message to the thread"""
    message = client.beta.threads.messages.create(
        thread_id=thread_id, role="user", content=content
    )
    return message


def get_assistant_response(thread_id: str, run: Optional[Run] = None) -> Optional[str]:
    """Given a thread, run the assistant for this thread and periodically checks for the response."""

    if run is None:
        assistant = get_assistant()

        chat_run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant.id,
        )
    else:

        chat_run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)

    if chat_run.status in ["queued", "in_progress"]:
        return get_assistant_response(thread_id, chat_run)

    elif chat_run.status != "completed":
        raise Exception("Could not finish the request")

    messages = client.beta.threads.messages.list(thread_id=thread_id)

    assistant_answer = [msg for msg in messages.data if msg.role == "assistant"]

    if len(assistant_answer) > 0:

        return assistant_answer[0].content[0].text.value

        # responses = []
        # for msg in assistant_answer:
        #     for content in msg.content:
        #         responses.append(content.text.value)
        #
        # return "\n".join(responses)

    raise Exception("Could not finish the request")
