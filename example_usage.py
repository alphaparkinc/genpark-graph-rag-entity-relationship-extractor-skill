from client import GraphRAGExtractor

text = "Alice works at AlphaCorp with Bob. Bob collaborates with Charlie on ProjectX."
extractor = GraphRAGExtractor()
triples = extractor.extract_triples(text)
subgraph = extractor.get_subgraph("Alice", depth=2)

print("Extracted Triples:", triples)
print("Alice Subgraph Nodes:", subgraph["nodes"])
print("Alice Subgraph Edges:", subgraph["edges"])
