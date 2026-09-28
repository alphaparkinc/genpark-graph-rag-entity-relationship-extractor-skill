import sys
import json
from client import GraphRAGExtractor

extractor = GraphRAGExtractor()

def handle_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-graph-rag-entity-relationship-extractor-skill", "version": "1.0.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "extract_and_query_graph_rag",
                        "description": "Extract entity triples from corpus and query subgraphs",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "corpus_text": {"type": "string", "description": "Text document to index"},
                                "query_entity": {"type": "string", "description": "Seed entity for neighborhood graph"},
                                "depth": {"type": "integer", "default": 2}
                            },
                            "required": ["corpus_text"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        
        if tool_name == "extract_and_query_graph_rag":
            text = args.get("corpus_text", "")
            entity = args.get("query_entity", "")
            depth = args.get("depth", 2)
            triples = extractor.extract_triples(text)
            subgraph = extractor.get_subgraph(entity, depth) if entity else None
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps({"triples_count": len(triples), "triples": triples, "subgraph": subgraph})}]
                }
            }
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
