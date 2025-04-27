import os
from typing import ClassVar,Any
import httpx
import json
from pydantic import Field

from .response import Response
from .types import OllamaModelType
from .request import Message, Tool,Request

from pydantic import ConfigDict, Field, PrivateAttr

from emp_agents.exceptions import InvalidModelException
from emp_agents.models import GenericTool, Provider, SystemMessage


class OllamaProvider(Provider[Response]):
    URL: ClassVar[str] = "http://localhost:11434/api/chat"
    # URL: ClassVar[str] = "http://localhost:11434/api/generate"

    api_key: str = Field(default_factory=lambda: os.environ["OLLAMA_API_KEY"])
    default_model: OllamaModelType = Field(default=OllamaModelType.gemma3_27b)

    @property
    def headers(self):
        return {
            "Content-Type": "application/json"
        }

    def _refine_for_oai_reasoning_models(
        self, result: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Awkwardly, OpenAI reasoning models do not accept system messages.
        They also accept some transformed parameters.
        """
        result["max_completion_tokens"] = result["max_tokens"]
        del result["max_tokens"]
        del result["tools"]
        for message in result["messages"]:
            if message["role"] == "system":
                message["role"] = "user"
        return result

    def _from_request(self, request: Request):
        exclude = ["system", "frequency_penalty", "presence_penalty", "num_responses", "n"]
        result = request.model_dump(exclude_none=True)

        if request.system:
            messages = [SystemMessage(content=request.system)] + request.messages
        else:
            messages = request.messages


        # Function to recursively set 'additionalProperties': False
        # def set_additional_properties_false(schema):
        #     if isinstance(schema, dict):
        #         if schema.get("type") == "object":
        #             schema["additionalProperties"] = False
        #         for key, value in schema.items():
        #             set_additional_properties_false(value)
        #     elif isinstance(schema, list):
        #         for item in schema:
        #             set_additional_properties_false(item)

        # if "response_format" in result:
        #     assert request.response_format is not None

        #     model_schema = request.response_format.model_json_schema()
        #     set_additional_properties_false(model_schema)
        #     del result["response_format"]
        #     result["response_format"] = {
        #         "type": "json_schema",
        #         "json_schema": {
        #             "name": request.response_format.__name__,
        #             "description": "response format",
        #             "strict": True,
        #             "schema": {
        #                 "type": "object",
        #                 "additionalProperties": False,
        #                 **model_schema,
        #             },
        #         },
        #     }


        # result["messages"] = [m.model_dump() for m in messages]
        result["messages"] = []
        for m in messages:
            m_dict = m.model_dump()
            # Fix any tool_calls in assistant messages
            if m_dict.get("role") == "assistant" and "tool_calls" in m_dict:
                if m_dict["tool_calls"] is not None:
                    for tool_call in m_dict["tool_calls"]:
                        function = tool_call.get("function")
                        if function and isinstance(function.get("arguments"), str):
                            try:
                                function["arguments"] = json.loads(function["arguments"])
                            except json.JSONDecodeError as e:
                                raise ValueError(f"Failed to decode tool_call arguments: {function['arguments']}") from e
            result["messages"].append(m_dict)


        result["tools"] = (
            [self.to_tool_call(t).model_dump(exclude_none=True) for t in request.tools]
            if request.tools
            else None
        )

        result["stream"] = False
        # result["format"] = "json"

        for field in exclude:
            if field in result:
                del result[field]

        is_reasoning_model = request.model in {
            OllamaModelType.openthinker_32b,
            OllamaModelType.deepseek_r1_32b,
        }
        return (
            self._refine_for_oai_reasoning_models(result)
            if is_reasoning_model
            else result
        )

    async def completion(self, request: Request) -> Response:
        # print("ttttttttttt")
        # print(request)#
        # print("aaaaaaaaaaaa")

        openai_request = self._from_request(request)
        # print(openai_request)
        # print("jjjjjjjjjjj")

        async with httpx.AsyncClient(headers=self.headers) as client:
            response = await client.post(self.URL, json=openai_request, timeout=None)
        if response.status_code >= 400:
            # print(response.text)
            raise ValueError(response.json())
        # print(response.text)
        data = response.json()
        for tool_call in data.get('message', {}).get('tool_calls', []):
            function_data = tool_call.get('function', {})
            if 'arguments' in function_data and isinstance(function_data['arguments'], dict):
                function_data['arguments'] = json.dumps(function_data['arguments'])

        # print(f"responseeee beforeeee::  {data}")
        # print(f"spacing########################################################################")
        first_json = Response(**data)
        # print(f"responseeee::  {first_json}")
        return first_json
        # return Response(**response.json())

    def to_tool_call(self, tool: GenericTool):
        from .tool import Function, Parameters, Property
        from .tool import Tool as Tool

        return Tool(
            type="function",
            function=Function(
                description=tool.description,
                name=tool.name,
                parameters=Parameters(
                    properties={
                        key: Property(**param.model_dump(exclude_none=True))
                        for key, param in tool.parameters.items()
                    },
                    required=tool.required,
                ),
            ),
            strict=True,
        )


__all__ = [
    "Classification",
    "Message",
    "OpenAIBase",
    "OllamaModelType",
    "Request",
    "Response",
    "Tool",
    "Function",
    "Property",
    "Parameters",
]
