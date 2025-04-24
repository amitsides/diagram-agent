from rdflib import Graph, RDFS, OWL
from rdflib.namespace import RDF
import re

# Load an ontology
def load_ontology(file_path: str) -> Graph:
    g = Graph()
    g.parse(file_path, format='xml')  # OWL/RDF format
    return g

# Clean and label URIs
def extract_label(uri):
    if isinstance(uri, str):
        return re.split(r'[#/]', uri)[-1]
    else:
        return uri.split("#")[-1]

# Convert ontology classes and relationships into natural language
def generate_llm_facts(graph: Graph, max_facts=20):
    facts = []
    for subj, pred, obj in graph:
        subj_label = extract_label(subj)
        pred_label = extract_label(pred)
        obj_label = extract_label(obj)

        if pred == RDFS.subClassOf:
            fact = f"A {subj_label} is a kind of {obj_label}."
        elif pred == RDF.type and obj == OWL.Class:
            fact = f"{subj_label} is a concept in this domain."
        elif pred == RDF.type and obj == OWL.ObjectProperty:
            fact = f"{subj_label} is a type of relationship between two entities."
        else:
            fact = f"{subj_label} {pred_label} {obj_label}."

        if fact not in facts:
            facts.append(fact)
        if len(facts) >= max_facts:
            break
    return facts

# Example usage
if __name__ == "__main__":
    ontology_path = "your_ontology.owl"  # Replace with your OWL file
    graph = load_ontology(ontology_path)
    facts = generate_llm_facts(graph)
    print("\n".join(facts))
