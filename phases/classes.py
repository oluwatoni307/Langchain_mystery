from pydantic import BaseModel, Field
from typing import Optional
from typing import TypedDict
from langgraph.graph import  MessagesState




class decision(BaseModel):
    Terminate: bool = Field(description="whether to terminate or not    ")
    message: Optional[str] = Field(
        description="text to state cues or steer conversation. Note that this is optional. and it should be when it is necessary "
    )








class ai_response(BaseModel):
    next_agent: str = Field(description='this is the next agent to run')
    is_correct: bool = Field(description='is this response correct or not based on the clues')
    review:str = Field(description=' ')





class State(MessagesState):
    next_agent: str
    Terminate: bool
    summerized: str
    count: int
    last_agent: str
