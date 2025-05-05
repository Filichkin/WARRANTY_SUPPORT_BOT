from pydantic import BaseModel
from typing import Literal


class AskResponse(BaseModel):
    response: str


class AskWithAIResponse(BaseModel):
    response: str
    provider: Literal['deepseek', 'mistral'] = 'mistral'
