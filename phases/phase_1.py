from langchain_core.prompts import PromptTemplate
from langgraph.graph import START, MessagesState, StateGraph, END
from phases.Kouhei import return_prompt as Kouhei_prompt
from phases.masami import return_prompt as masami_prompt
from phases.susumu import return_prompt as susumu_prompt
from phases.prompt import *
from phases.config import llm, summary
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import ChatMessage,ChatMessageChunk
from typing import Annotated, TypedDict, Union, cast
from pydantic import BaseModel
from langgraph.graph import  MessagesState



class State(MessagesState):
    summerized: str

class Chatconversation(BaseModel):
    agent: str
    response: str

def kouhei(state: State):
    print("phase 1")
    Kouhei_phase = Kouhei_prompt(phase_1_prompt)

    prompt = PromptTemplate.from_template(
        "{Kouhei_phase} this is the previous conversation: {history}"
    )
    agent = prompt | llm | StrOutputParser()
    responses = agent.invoke(
        {"Kouhei_phase": Kouhei_phase, "history": state["messages"]}
    )
   
    
    return {"messages":  responses}


def masami(state: State):
    masami_phase = masami_prompt(phase_1_prompt)

    prompt = PromptTemplate.from_template(
        "{masami_phase} this is the previous conversation: {history}"
    )
    agent = prompt | llm | StrOutputParser()
    response = agent.invoke(
        {"masami_phase": masami_phase, "history": state["messages"]}
    )
    return {"messages":  response}

def susumu(state: State):
    susumu_phase = susumu_prompt(phase_1_prompt)

    prompt = PromptTemplate.from_template(
        "{susumu_phase} this is the previous conversation: {history}"
    )
    agent = prompt | llm | StrOutputParser()
    response = agent.invoke(
        {"susumu_phase": susumu_phase, "history": state["messages"]}
    )

    return {"messages":  response}


def start(state: State):

    message = "We are in Phase 1. quick introduction"

    return {"messages":message}


# Create an instance of StateGraph
graph = StateGraph(State)

# Define states and transitions
graph.add_node("Detective", start)


# Define nodes in a single flow sequence
graph.add_node("Kouhei", kouhei)
graph.add_node("Masami", masami)
graph.add_node("Susumu", susumu)

# Define sequential transitions from START to each node

graph.add_edge(START, "Detective")
graph.add_edge("Detective", "Kouhei")
graph.add_edge("Kouhei", "Masami")
graph.add_edge("Masami", "Susumu")
graph.add_edge("Susumu", END)


# Compile the graph flow
phase_1_flow = graph.compile()
