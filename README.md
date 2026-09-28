# genpark-graph-rag-entity-relationship-extractor-skill

Agent Skill implementing **GraphRAG Entity-Relationship Extraction & Subgraph Neighborhood Retrieval** in 100% pure Python standard library.

## Architectural Flow
```mermaid
flowchart TD
    Doc["Corpus Text Document"] --> SentSplit["Sentence Tokenizer"]
    SentSplit --> EntDetect["Entity Identifier & Capitalized Tokens"]
    EntDetect --> Cooccur["Co-occurrence Pair Matrix"]
    Cooccur --> Triples["(Head, Relation, Tail) Triples"]
    Triples --> Adjacency["Graph Adjacency Index"]
    Seed["Query Seed Entity"] --> BFS["Bounded Neighborhood BFS (depth=k)"]
    Adjacency & Seed --> BFS
    BFS --> SubGraph["Target Subgraph Context"]
```
