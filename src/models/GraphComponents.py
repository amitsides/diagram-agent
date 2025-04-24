from enum import Enum
from typing import Optional, Any, List
from pydantic import BaseModel, Field


class EdgeType(str, Enum):
    FORWARD = ">>"           # Represents a forward relationship (>>)
    BACKWARD = "<<"          # Represents a backward relationship (<<)
    BIDIRECTIONAL = "-"      # Represents a bidirectional relationship (-)


class Node(BaseModel):
    """Represents a node in the graph"""
    id: str                  # Unique identifier for the node
    type: str                # Type of node (e.g., "ELB", "EC2", "RDS", "S3")
    label: Optional[str] = None  # Human-readable label
    properties: dict = Field(default_factory=dict)  # Additional properties


class Edge(BaseModel):
    """Represents an edge between two nodes"""
    source_id: str           # ID of the source node
    target_id: str           # ID of the target node
    type: EdgeType           # Type of relationship
    properties: dict = Field(default_factory=dict)  # Additional properties


class Graph(BaseModel):
    """Represents a complete graph structure"""
    nodes: List[Node] = Field(default_factory=list)
    edges: List[Edge] = Field(default_factory=list)

