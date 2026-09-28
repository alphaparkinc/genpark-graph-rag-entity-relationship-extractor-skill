"""Graph RAG Entity & Relational Knowledge Subgraph Extractor.
100% Python Standard Library.
"""

import re
import collections

class GraphRAGExtractor:
    """GraphRAG knowledge graph extraction and neighborhood sub-graph retriever."""
    def __init__(self):
        self.entities = set()
        self.triples = []
        self.adj = collections.defaultdict(list)

    def extract_triples(self, text):
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
        for s in sentences:
            words = [w for w in re.findall(r'\b[A-Za-z0-9_-]+\b', s)]
            capitalized = [w for w in words if w[0].isupper() and len(w) > 1]
            for i in range(len(capitalized)):
                for j in range(i + 1, len(capitalized)):
                    h, t = capitalized[i], capitalized[j]
                    if h != t:
                        self.entities.add(h)
                        self.entities.add(t)
                        self.triples.append((h, "RELATED_TO", t))
                        self.adj[h].append(t)
                        self.adj[t].append(h)
        return self.triples

    def get_subgraph(self, entity, depth=1):
        visited = {entity}
        frontier = [entity]
        edges = []
        for _ in range(depth):
            next_frontier = []
            for u in frontier:
                for v in self.adj.get(u, []):
                    edges.append((u, v))
                    if v not in visited:
                        visited.add(v)
                        next_frontier.append(v)
            frontier = next_frontier
        return {"nodes": list(visited), "edges": edges}
