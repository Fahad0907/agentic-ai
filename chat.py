from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated, Generator
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph.message import add_messages
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import MemorySaver


# chat bot config
llm = ChatOllama(
    model="qwen2.5-coder:7b",
    temperature=0
)

class ChatState(TypedDict):
    message: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState):
    response = llm.invoke(state['message'])
    return {
        'message': [response]
    }


check_pointer = MemorySaver()
graph = StateGraph(ChatState)

graph.add_node('chat_node', chat_node)

graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

workflow = graph.compile(checkpointer=check_pointer)

config = {'configurable' : {'thread_id' : '1'}}
def show_output(message)-> Generator[str, None, None]:
    for chunk, metadata in workflow.stream(
        {"message": [HumanMessage(content=message)]},
        config=config,
        stream_mode="messages"  # streams token by token
    ):
        if chunk.content:
            yield chunk.content