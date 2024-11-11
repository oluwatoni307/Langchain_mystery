from langchain_core.messages import SystemMessage
from langgraph.graph import START, MessagesState, StateGraph
from phases.Kouhei import return_prompt as Kouhei_prompt
from phases.masami import return_prompt as masami_prompt
from phases.susumu import return_prompt as susumu_prompt
from phases.prompt import *
from phases.config import *
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, START, END
from langchain_core.prompts import ChatPromptTemplate
from phases.classes import *


def verifier(agents: list, last_conversation, agent_response):
    """_summary_

    Args:
        agents (list): _description_
        last_conversation (_type_): _description_
        agent_response (_type_): _description_

    Returns:
        _type_: _description_
    """
    prompt = ChatPromptTemplate(
        [
            SystemMessage(content=moderator_2),
            ("user", "last_conversation: {last_conversation}"),
            ("user", "agent_response: {agent_response}"),
            ("user", "agents: {agents}"),
        ]
    )
    new_llm = llm.with_structured_output(ai_response)
    agent = prompt | new_llm
    llm_response: ai_response = agent.invoke(
        {
            "last_conversation": last_conversation,
            "agent_response": agent_response,
            "agents": agents,
        }
    )
    return llm_response


def agent_blueprint(system_prompt, history, last_messages, next_agent: list):
    prompt = ChatPromptTemplate(
        [
            SystemMessage(content=system_prompt),
            ("user", " summary of older_messages: {history}, "),
            ("user", "Recent Messages: {last_messages}, "),
        ]
    )
    agent = prompt | llm | StrOutputParser()

    llm_response = agent.invoke({"history": history, "last_messages": last_messages})
    last_response = last_messages[-1]
    checked: ai_response = verifier(next_agent, last_response, llm_response)
    if not checked.is_correct:

        prompt = ChatPromptTemplate(
            [
                SystemMessage(content=system_prompt),
             ("system", f"Please provide an updated response addressing these points: {checked.review}"),
                ("user", "{llm_response}"),
            ]
        )
        agent = prompt | llm | StrOutputParser()

        llm_response = agent.invoke({"llm_response": llm_response})
    return {
        "messages": llm_response,
        "next_agent": checked.next_agent,
    }


def kouhei(state: State):
    Kouhei_phase = Kouhei_prompt(phase_4_prompt)
    history = state["summerized"]
    last_messages = state["messages"]
    next_agent = ["Susumu", "Masami"]

    response = agent_blueprint(Kouhei_phase, history, last_messages, next_agent)
    return response


def susumu(state: State):
    Kouhei_phase = susumu_prompt(phase_4_prompt)
    history = state["summerized"]
    last_messages = state["messages"]
    next_agent = ["Kouhei", "Masami"]

    response = agent_blueprint(Kouhei_phase, history, last_messages, next_agent)
    return response


def masami(state: State):
    Kouhei_phase = masami_prompt(phase_4_prompt)
    history = state["summerized"]
    last_messages = state["messages"]
    next_agent = ["Susumu", "Kouhei"]

    response = agent_blueprint(Kouhei_phase, history, last_messages, next_agent)
    return response


def summerize(state: State):
    prompt = ChatPromptTemplate(
        [
            ("system", Summerize_prompt),
            ("user", " previous conversations: {history}"),
        ]
    )

    last_messages = state["messages"][-2:]
    previous_messages = state["messages"][:-2]
    agent = prompt | llm | StrOutputParser()
    summary = agent.invoke({"history": previous_messages})
    full_summary = state["summerized"] + "\n" + summary
    # Assuming 'state' is your current message state
    state["messages"] = []

    return {
        "messages": last_messages,
        "summerized": full_summary,
    }


def selector(state: State):
    if len(state["messages"]) > 6:
        return "summerize"

    if state["next_agent"] == "DONE":
        return END
    else:
        return state["next_agent"]


def start(state: State):
    count = 0
    last_agent = ""
    next_agent = "Kouhei"
    messages = "We are now in phase 4. we are looking into the theories. Kouhei let us hear your thoughts"


    return {
        "count": count,
        "last_agent": last_agent,
        "next_agent": next_agent,
        "messages": messages,
    }


# Create an instance of StateGraph
graph = StateGraph(State)

# Define states and transitions
graph.add_node("Detective", start)
graph.add_node("summerize", summerize)

graph.add_node("Kouhei", kouhei)
graph.add_node("Masami", masami)
graph.add_node("Susumu", susumu)

# Define transitions based on responses

graph.add_edge(START, "Detective")
graph.add_conditional_edges("Detective", selector)
graph.add_conditional_edges("summerize", selector)

graph.add_conditional_edges("Kouhei", selector)
graph.add_conditional_edges("Masami", selector)
graph.add_conditional_edges("Susumu", selector)

phase_4_flow = graph.compile()
