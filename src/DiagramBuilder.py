from typing import Dict, List, Optional, Union
import json


class DiagramBuilder:
    """A utility class to build diagrams programmatically from data structures."""
    
    def __init__(self):
        self.indent_level = 0
        self.code_lines = []
    
    def _indent(self) -> str:
        """Return the current indentation string."""
        return "    " * self.indent_level
    
    def _add_line(self, line: str):
        """Add a line of code with proper indentation."""
        self.code_lines.append(f"{self._indent()}{line}")
    
    def _start_block(self, line: str):
        """Start a new code block with the given line."""
        self._add_line(line)
        self.indent_level += 1
    
    def _end_block(self):
        """End the current code block."""
        self.indent_level -= 1
    
    def _add_node(self, node_type: str, node_id: str, parameters: Optional[List[str]] = None):
        """Add a node definition."""
        params = f'"{node_id}"'
        if parameters:
            params = f'"{node_id}", {", ".join(parameters)}'
        self._add_line(f"{node_type}({params})")
    
    def _add_nodes_group(self, nodes_list: List[Dict[str, str]]):
        """Add a group of nodes in a list notation."""
        if not nodes_list:
            return ""
            
        nodes_code = "["
        for i, node in enumerate(nodes_list):
            nodes_code += f'{node["type"]}("{node["id"]}")'
            if i < len(nodes_list) - 1:
                nodes_code += ",\n" + self._indent() + " "
        nodes_code += "]"
        return nodes_code
    
    def _process_connections(self, source, target, edge_type):
        """Process connections between nodes based on edge type."""
        if isinstance(source, list) and isinstance(target, list):
            # Many-to-many connection
            sources = self._add_nodes_group(source)
            targets = self._add_nodes_group(target)
            self._add_line(f"{sources} {edge_type} {targets}")
        elif isinstance(source, list):
            # Many-to-one connection
            sources = self._add_nodes_group(source)
            self._add_line(f"{sources} {edge_type} {target['type']}(\"{target['id']}\")")
        elif isinstance(target, list):
            # One-to-many connection
            targets = self._add_nodes_group(target)
            self._add_line(f"{source['type']}(\"{source['id']}\") {edge_type} {targets}")
        else:
            # One-to-one connection
            self._add_line(f"{source['type']}(\"{source['id']}\") {edge_type} {target['type']}(\"{target['id']}\")")
    
    def build_from_json(self, diagram_data: Dict) -> str:
        """Build diagram code from a JSON structure."""
        # Start with diagram definition
        diagram_name = diagram_data.get("diagram_name", "Network Diagram")
        show_param = str(diagram_data.get("show", False)).lower()
        
        self._start_block(f'with Diagram("{diagram_name}", show={show_param}):')
        
        # Create a dictionary of nodes by ID for easy lookup
        nodes_dict = {node["id"]: node for node in diagram_data.get("nodes", [])}
        
        # Create standalone nodes first
        standalone_nodes = []
        for node in diagram_data.get("nodes", []):
            is_in_edge = False
            for edge in diagram_data.get("edges", []):
                if edge["source_id"] == node["id"] or edge["target_id"] == node["id"]:
                    is_in_edge = True
                    break
                    
            if not is_in_edge and node.get("cluster") is None:
                standalone_nodes.append(node)
                self._add_line(f'{node["type"]}("{node["id"]}")')
        
        # Process clusters
        clusters = {}
        for node in diagram_data.get("nodes", []):
            if node.get("cluster"):
                cluster_name = node["cluster"]
                if cluster_name not in clusters:
                    clusters[cluster_name] = []
                clusters[cluster_name].append(node)
        
        # Create clusters and their nodes
        for cluster_name, cluster_nodes in clusters.items():
            self._start_block(f'with Cluster("{cluster_name}"):')
            
            for node in cluster_nodes:
                if "subcluster" not in node:
                    self._add_line(f'{node["type"]}("{node["id"]}")')
            
            # Handle subclusters
            subclusters = {}
            for node in cluster_nodes:
                if node.get("subcluster"):
                    subcluster_name = node["subcluster"]
                    if subcluster_name not in subclusters:
                        subclusters[subcluster_name] = []
                    subclusters[subcluster_name].append(node)
            
            for subcluster_name, subcluster_nodes in subclusters.items():
                self._start_block(f'with Cluster("{subcluster_name}"):')
                for node in subcluster_nodes:
                    self._add_line(f'{node["type"]}("{node["id"]}")')
                self._end_block()
            
            self._end_block()
        
        # Process edges after all nodes and clusters are defined
        for edge in diagram_data.get("edges", []):
            source_node = nodes_dict.get(edge["source_id"])
            target_node = nodes_dict.get(edge["target_id"])
            
            if source_node and target_node:
                self._process_connections(source_node, target_node, edge["type"])
        
        return "\n".join(self.code_lines)


def json_to_diagram_code(json_data: Union[str, Dict]) -> str:
    """Convert JSON data to diagram code."""
    if isinstance(json_data, str):
        diagram_data = json.loads(json_data)
    else:
        diagram_data = json_data
        
    builder = DiagramBuilder()
    return builder.build_from_json(diagram_data)


# Example usage
if __name__ == "__main__":
    # Create the JSON structure for the example
    example_data = {
        "diagram_name": "Message Collecting",
        "show": False,
        "nodes": [
            {"id": "pubsub", "type": "PubSub"},
            {"id": "core1", "type": "IotCore", "cluster": "Source of Data"},
            {"id": "core2", "type": "IotCore", "cluster": "Source of Data"},
            {"id": "core3", "type": "IotCore", "cluster": "Source of Data"},
            {"id": "flow", "type": "Dataflow", "cluster": "Targets", "subcluster": "Data Flow"},
            {"id": "bq", "type": "BigQuery", "cluster": "Targets", "subcluster": "Data Lake"},
            {"id": "storage", "type": "GCS", "cluster": "Targets", "subcluster": "Data Lake"},
            {"id": "engine", "type": "AppEngine", "cluster": "Targets", "subcluster": "Processing"},
            {"id": "bigtable", "type": "BigTable", "cluster": "Targets", "subcluster": "Processing"},
            {"id": "func", "type": "Functions", "cluster": "Targets", "subcluster": "Serverless"},
            {"id": "appengine", "type": "AppEngine", "cluster": "Targets", "subcluster": "Serverless"}
        ],
        "edges": [
            {"source_id": "core1", "target_id": "pubsub", "type": ">>"},
            {"source_id": "core2", "target_id": "pubsub", "type": ">>"},
            {"source_id": "core3", "target_id": "pubsub", "type": ">>"},
            {"source_id": "flow", "target_id": "bq", "type": ">>"},
            {"source_id": "flow", "target_id": "storage", "type": ">>"},
            {"source_id": "flow", "target_id": "engine", "type": ">>"},
            {"source_id": "engine", "target_id": "bigtable", "type": ">>"},
            {"source_id": "flow", "target_id": "func", "type": ">>"},
            {"source_id": "func", "target_id": "appengine", "type": ">>"},
            {"source_id": "pubsub", "target_id": "flow", "type": ">>"}
        ]
    }
    
    # Generate diagram code
    diagram_code = json_to_diagram_code(example_data)
    print(diagram_code)