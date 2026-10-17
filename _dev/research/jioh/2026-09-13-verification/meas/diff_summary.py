import json, sys
a = json.load(open(sys.argv[1])); b = json.load(open(sys.argv[2]))
same = diff = 0
def walk(x, y, path):
    global same, diff
    if isinstance(x, dict) and isinstance(y, dict):
        for k in sorted(set(x) | set(y)):
            if k not in x: print("ONLY-STORED", path + "/" + k); diff += 1; continue
            if k not in y: print("ONLY-REPRO ", path + "/" + k); diff += 1; continue
            walk(x[k], y[k], path + "/" + k)
    elif isinstance(x, list) and isinstance(y, list):
        if len(x) != len(y): print("LEN", path, len(x), len(y)); diff += 1
        for i, (p, q) in enumerate(zip(x, y)): walk(p, q, f"{path}[{i}]")
    else:
        if x == y: same += 1
        else: print("DIFF", path, "repro=", x, "stored=", y); diff += 1
walk(a, b, "")
print("leaf-equal", same, "diffs", diff)
