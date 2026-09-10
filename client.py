class SloppyQuorumStore:
    """
    Amazon Dynamo Sloppy Quorum and Hinted Handoff Engine.
    Achieves configurable R/W quorums and stores temporary hints when primary nodes are partitioned.
    """
    def __init__(self, n=3, r=2, w=2):
        self.n = n
        self.r = r
        self.w = w
        self.nodes = {}
        self.hints = [] # (intended_node, key, val)

    def put(self, key, value, active_nodes):
        success = 0
        for nid in active_nodes[:self.w]:
            if nid not in self.nodes:
                self.nodes[nid] = {}
            self.nodes[nid][key] = value
            success += 1
        return success >= self.w

    def get(self, key, active_nodes):
        for nid in active_nodes[:self.r]:
            if nid in self.nodes and key in self.nodes[nid]:
                return self.nodes[nid][key]
        return None

    def record_hint(self, intended_node, key, value):
        self.hints.append((intended_node, key, value))

    def handoff_hints(self, target_node):
        handed = 0
        rem = []
        for item in self.hints:
            intended, k, v = item
            if intended == target_node:
                if target_node not in self.nodes:
                    self.nodes[target_node] = {}
                self.nodes[target_node][k] = v
                handed += 1
            else:
                rem.append(item)
        self.hints = rem
        return handed
