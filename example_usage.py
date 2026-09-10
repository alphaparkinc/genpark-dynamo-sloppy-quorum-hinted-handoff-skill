from client import SloppyQuorumStore

def main():
    print("=== Testing Sloppy Quorum with Hinted Handoff ===")
    store = SloppyQuorumStore(n=3, r=2, w=2)
    
    # Normal quorum write
    ok = store.put("user_name", "Alice", ["node_1", "node_2", "node_3"])
    assert ok
    
    # Read quorum
    val = store.get("user_name", ["node_1", "node_2"])
    print(f"Quorum read: user_name = {val}")
    assert val == "Alice"
    
    # Hinted handoff during partition of node_3
    store.record_hint("node_3", "email", "alice@example.com")
    recovered = store.handoff_hints("node_3")
    print(f"Handoff hints delivered to node_3: {recovered}")
    assert recovered == 1
    assert store.nodes["node_3"]["email"] == "alice@example.com"
    print("=== Dynamo Quorum Verification Complete ===")

if __name__ == "__main__":
    main()
