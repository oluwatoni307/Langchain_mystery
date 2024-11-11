from langchain_core.prompts import PromptTemplate
from langgraph.graph import START, MessagesState, StateGraph
from phases.Kouhei import return_prompt as Kouhei_prompt
from phases.masami import return_prompt as masami_prompt
from phases.susumu import return_prompt as susumu_prompt
from phases.prompt import *
from phases.config import *
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START,END
from typing import Optional









class State(MessagesState):
    pass


def kouhei(state: State):
    Kouhei_phase = Kouhei_prompt(phase_5_prompt)

    prompt = PromptTemplate.from_template("{Kouhei_phase} this is the previous conversation: {history}")
    agent = prompt|llm|StrOutputParser()
    response = agent.invoke({"Kouhei_phase":Kouhei_phase,"history":state["messages"] })
    return {"messages": response}

def masami(state: State):
    masami_phase = masami_prompt(phase_5_prompt)

    prompt = PromptTemplate.from_template("{masami_phase} this is the previous conversation: {history}")
    agent = prompt|llm|StrOutputParser()
    response = agent.invoke({"masami_phase":masami_phase,"history":state["messages"] })
    return {"messages": response}

def susumu(state: State):
    susumu_phase = susumu_prompt(phase_5_prompt)

    prompt = PromptTemplate.from_template("{susumu_phase} this is the previous conversation: {history}")
    agent = prompt|llm|StrOutputParser()
    response = agent.invoke({"susumu_phase":susumu_phase,"history":state["messages"] })
    return {"messages": response}


def start(state: State):

    message = " We are now in phase 5. Time to vote"

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
phase_5_flow = graph.compile()