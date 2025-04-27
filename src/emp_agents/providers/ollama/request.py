from typing import Annotated, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, PlainSerializer

from emp_agents.models.shared import Message
from emp_agents.models.shared.tools import GenericTool

from .tool import Tool
from .types import OllamaModelType


class Request(BaseModel):
    """
    https://github.com/ollama/ollama/blob/main/docs/api.md#generate-a-chat-completion
    """

    model_config = ConfigDict(populate_by_name=True)

    model: OllamaModelType
    max_tokens: Optional[int] = Field(default=None)
    temperature: Optional[float] = Field(default=None, ge=0, le=2.0)
    tool_choice: Literal["none", "required", "auto", None] = Field(default=None)
    tools: Annotated[
        Optional[list[GenericTool]],
        PlainSerializer(
            lambda tools_list: (
                # [tool.to_openai() for tool in tools_list]
                [tool for tool in tools_list]
                if tools_list is not None
                else None
            ),
            return_type=Optional[list[Tool]],
        ),
    ] = Field(default=None)

    system: str | None = None
    messages: list[Message] | None = None  # Anthropic Field

    # print("hereeeeeeeeeeeeeee")
    num_responses: Optional[int] = Field(
        default=None, serialization_alias="n"
    )  # openai
    top_p: Optional[int] = Field(default=None)  # openai

    def model_dump(self, *, exclude_none=True, by_alias=True, **kwargs):
        return super().model_dump(
            exclude_none=exclude_none, by_alias=by_alias, **kwargs
        )
