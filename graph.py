from phases.phase_1 import phase_1_flow
from phases.phase_2 import phase_2_flow
from phases.phase_3 import phase_3_flow
from phases.phase_4 import phase_4_flow
from phases.phase_5 import phase_5_flow
from langgraph.graph import START, MessagesState, StateGraph, END




class State(MessagesState):

    summerized: str


# Create an instance of StateGraph
graph = StateGraph(State)


graph.add_node("phase_1_flow", phase_1_flow)
graph.add_node("phase_2_flow", phase_2_flow)
graph.add_node("phase_3_flow", phase_3_flow)
graph.add_node("phase_4_flow", phase_4_flow)
graph.add_node("phase_5_flow", phase_5_flow)


# Define sequential transitions from START to each node
graph.add_edge(START, "phase_1_flow")


graph.add_edge("phase_1_flow", "phase_2_flow")
graph.add_edge("phase_2_flow", "phase_3_flow")
graph.add_edge("phase_3_flow", "phase_4_flow")
graph.add_edge("phase_4_flow", "phase_5_flow")


graph.add_edge("phase_5_flow", END)

# Compile the graph flow
mystery = graph.compile()



# Function to process each event as it streams
def process_event_stream(event):
    results = []

    # Assuming `event` is already structured as a tuple
    _, phase_data = event  # Each event is a (phase_id, phase_data) tuple

    for agent, details in phase_data.items():
        if agent in ["Masami", "Susumu", "Kouhei", "Detective"]:
            # Normal processing for the 3 specified agents
            agent_name = agent
            response_content = details.get("messages")
            results.append((agent_name, response_content))
        elif "phase" in agent:
            # Extract the phase number from the agent name, e.g., "phase_1_flow"
            phase_number = agent.split("_")[1]  # Get the number part after "phase_"
            agent_name = "detective"
            response_content = f"end of phase {phase_number}"
            results.append((agent_name, response_content))
    
    return results


from queue import Queue

message_queue = Queue()


# Example usage assuming events are streaming in
# Replace this loop with the actual streaming mechanism you use
def runcov():
    for event in mystery.stream(
        {
            "messages": "start",
        },
        {"recursion_limit": 700},
        subgraphs=True,
    ):
        extracted_data = process_event_stream(event)
        for agent, response in extracted_data:
            message_dict = {
                "agent_name": agent,
                "content": response,
            }
            message_queue.put(message_dict)
            # print('hi')
            print(f"Agent: {agent}, Response: {response}")

if __name__ == "__main__":
    runcov()
