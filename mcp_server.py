from client import SloppyQuorumStore
import json

def handle_request(req):
    store = SloppyQuorumStore()
    action = req.get("action")
    if action == "put":
        k = req.get("key", "")
        v = req.get("val", "")
        nodes = req.get("nodes", ["n1", "n2"])
        ok = store.put(k, v, nodes)
        return {"status": "ok", "success": ok}
    return {"status": "error", "message": "Unknown action"}

if __name__ == "__main__":
    print(json.dumps(handle_request({"action": "put", "key": "k", "val": "v"})))
