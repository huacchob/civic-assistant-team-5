"""Graph for the Program Agent workflow."""

from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph

from .nodes import fetch_government_programs
from .state import ProgramMatcherState


def build_program_graph() -> CompiledStateGraph[
    ProgramMatcherState, None, ProgramMatcherState, ProgramMatcherState
]:
    """Program Agent workflow graph."""
    graph: StateGraph[
        ProgramMatcherState, None, ProgramMatcherState, ProgramMatcherState
    ] = StateGraph(state_schema=ProgramMatcherState)

    # Add government programs node
    graph.add_node(node="government_programs", action=fetch_government_programs)

    # Entry + finish point
    graph.set_entry_point(key="government_programs")
    graph.set_finish_point(key="government_programs")

    # MUST compile or ainvoke won’t run
    return graph.compile()
