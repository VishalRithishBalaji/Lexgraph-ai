import json
import re
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
from pydantic import BaseModel, Field


class Relationship(BaseModel):
    source: str
    target: str
    type: str


class KnowledgeGraph(BaseModel):
    entities: list[str] = Field(default_factory=list)
    relationships: list[Relationship] = Field(default_factory=list)


def extract_json(text: str) -> dict:
    text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    fence_match = re.search(
        r"```(?:json)?\s*(\{.*?\})\s*```",
        text,
        re.DOTALL,
    )
    if fence_match:
        return json.loads(fence_match.group(1))

    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end > start:
        return json.loads(text[start : end + 1])

    raise ValueError("No valid JSON object found in knowledge graph output.")


def normalize_graph_data(data: dict) -> dict:
    if "entities" in data:
        return {
            "entities": data.get("entities", []),
            "relationships": data.get("relationships", []),
        }

    entities: list[str] = []
    for values in data.values():
        if isinstance(values, list):
            for value in values:
                if isinstance(value, str) and value not in entities:
                    entities.append(value)

    return {"entities": entities, "relationships": []}


def load_graph_data(
    json_file: str | Path = "reports/knowledge_graph.json",
) -> dict:
    text = Path(json_file).read_text(encoding="utf-8")
    return normalize_graph_data(extract_json(text))


def save_graph_data(
    data: dict | KnowledgeGraph,
    json_file: str | Path = "reports/knowledge_graph.json",
) -> None:
    if isinstance(data, KnowledgeGraph):
        payload = data.model_dump()
    else:
        payload = normalize_graph_data(data)

    path = Path(json_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2),
        encoding="utf-8",
    )


def generate_graph(
    json_file: str | Path = "reports/knowledge_graph.json",
    output_file: str | Path = "reports/knowledge_graph.png",
) -> None:
    data = load_graph_data(json_file)

    graph = nx.Graph()

    for entity in data.get("entities", []):
        graph.add_node(entity)

    for rel in data.get("relationships", []):
        graph.add_edge(
            rel["source"],
            rel["target"],
            label=rel["type"],
        )

    plt.figure(figsize=(10, 8))

    pos = nx.spring_layout(graph, seed=42)

    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_size=2500,
    )

    labels = nx.get_edge_attributes(graph, "label")

    nx.draw_networkx_edge_labels(
        graph,
        pos,
        edge_labels=labels,
    )

    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()
