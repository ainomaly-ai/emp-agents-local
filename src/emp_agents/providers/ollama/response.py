import json
from enum import StrEnum
from typing import Optional

from pydantic import BaseModel

# from emp_agents.models.shared import AssistantMessage, ToolCall
from emp_agents.models import AssistantMessageOllama, Message, ResponseT, ToolCallOllama
from emp_agents.types import Role

from .types import OllamaModelType as ModelType


# class ResponseType(StrEnum):
    # text = "text"
    # tool_use = "tool_use"


# class Content(BaseModel):
#     id: str | None = None
#     type: ResponseType
#     text: str | None = None
#     input: dict[str, str] | None = None
#     name: str | None = None

#     @property
#     def function(self) -> ToolCall.Function:
#         assert self.name is not None
#         assert self.input is not None
#         return ToolCall.Function(name=self.name, arguments=json.dumps(self.input))

#     def to_message(self) -> AssistantMessage:
#         return AssistantMessage(content=self.text)



class Message(BaseModel):
    message: AssistantMessageOllama


# class Usage(BaseModel):
#     input_tokens: int
#     output_tokens: int


class Response(ResponseT):
    model: ModelType | str
    created_at : str
    response : Optional[str] = None
    message: AssistantMessageOllama
    # content: list[Content]
    done : Optional[bool] = None
    done_reason : Optional[str] = None
    total_duration:Optional[int] = None
    load_duration:Optional[int] = None
    prompt_eval_count:Optional[int] = None
    prompt_eval_duration:Optional[int] = None
    eval_count:Optional[int] = None
    eval_duration:Optional[int] = None


    @property
    def text(self):
        return self.response

    @property
    def tool_calls(self) -> list[ToolCallOllama] | None:
        # print("toolcalls respose")
        # print(self.message.tool_calls)
        return self.message.tool_calls

    @property
    def messages(self) -> list[Message]:
        if self.message.content is not '':
            print(f"{self.message.content}")
            return [self.message.content] 
        else:
        # if self.message:
            return [self.message]
        
    def __repr__(self):
        return f'<Response id="{self.id}">'

    def print(self):
        for choice in self.message:
            print(choice.content)
            print("-" * 15)

    __str__ = __repr__
