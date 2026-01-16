"""Graph state definitions and data structures for the Deep Research agent."""

import operator
from typing import Annotated, List, Literal, Optional

from langchain_core.messages import MessageLikeRepresentation
from langgraph.graph import MessagesState
from pydantic import BaseModel, Field
from typing_extensions import TypedDict


###################
# Structured Outputs
###################
class ConductResearch(BaseModel):
    """Call this tool to conduct research on a specific topic."""
    research_topic: str = Field(
        description="The topic to research. Should be a single topic, and should be described in high detail (at least a paragraph).",
    )

class ResearchComplete(BaseModel):
    """Call this tool to indicate that the research is complete."""

class Summary(BaseModel):
    """Research summary with key findings."""
    
    summary: str
    key_excerpts: str

class ClarifyWithUser(BaseModel):
    """Model for user clarification requests."""
    
    need_clarification: bool = Field(
        description="Whether the user needs to be asked a clarifying question.",
    )
    question: str = Field(
        description="A question to ask the user to clarify the report scope",
    )
    verification: str = Field(
        description="Verify message that we will start research after the user has provided the necessary information.",
    )

class ResearchQuestion(BaseModel):
    """Research question and brief for guiding research."""
    
    research_brief: str = Field(
        description="A research question that will be used to guide the research.",
    )

class ReviewFeedback(BaseModel):
    """Feedback from the reviewer on the quality of research."""
    
    grade: Literal["pass", "fail"] = Field(
        description="Pass if the research is sufficient and covers the topic well. Fail otherwise."
    )
    feedback: str = Field(
        description="Specific feedback on what is missing or needs improvement."
    )
    suggested_queries: List[str] = Field(
        description="Suggested search queries to address the missing information.",
        default=[]
    )

class Section(BaseModel):
    """A section of the research report."""
    name: str = Field(description="Name of the section.")
    description: str = Field(description="Brief description of what this section should cover.")
    research: bool = Field(description="Whether research is needed for this section.", default=True)

class SectionOutput(BaseModel):
    """Output creation for a section."""
    name: str
    content: str
    sources: List[str] = []

class ResearchStep(BaseModel):
    """A step in the research plan."""
    id: int
    description: str

class Query(BaseModel):
    """A search query."""
    query: str
    aspect: str

class Feedback(BaseModel):
    """Feedback from review."""
    grade: Literal["pass", "fail"]
    notes: str 





###################
# State Definitions
###################

def override_reducer(current_value, new_value):
    """Reducer function that allows overriding values in state."""
    if isinstance(new_value, dict) and new_value.get("type") == "override":
        return new_value.get("value", new_value)
    else:
        return operator.add(current_value, new_value)
    
class AgentInputState(MessagesState):
    """InputState is only 'messages'."""

class AgentState(MessagesState):
    """Main agent state containing messages and research data."""
    
    supervisor_messages: Annotated[list[MessageLikeRepresentation], override_reducer]
    research_brief: Optional[str]
    raw_notes: Annotated[list[str], override_reducer] = []
    notes: Annotated[list[str], override_reducer] = []
    final_report: str

class SupervisorState(TypedDict):
    """State for the supervisor that manages research tasks."""
    
    supervisor_messages: Annotated[list[MessageLikeRepresentation], override_reducer]
    research_brief: str
    notes: Annotated[list[str], override_reducer] = []
    research_iterations: int = 0
    raw_notes: Annotated[list[str], override_reducer] = []

class ResearcherState(TypedDict):
    """State for individual researchers conducting research."""
    
    researcher_messages: Annotated[list[MessageLikeRepresentation], operator.add]
    tool_call_iterations: int = 0
    research_topic: str
    compressed_research: str
    raw_notes: Annotated[list[str], override_reducer] = []
    review_feedback: Optional[ReviewFeedback] = None
    review_iterations: int = 0

class ResearcherOutputState(BaseModel):
    """Output state from individual researchers."""
    
    compressed_research: str
    raw_notes: Annotated[list[str], override_reducer] = []

class DeepResearchState(AgentState):
    """Extended state for deep research."""
    sections: List[Section] = []
    completed_sections: List[SectionOutput] = []