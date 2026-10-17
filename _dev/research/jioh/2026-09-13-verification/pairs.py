import json
B="/Users/jiohin/Desktop/future-of-sw/LLM_driven_shceduling/dataset/build/coreset-single/"
def ev(f): return json.load(open(B+f+".workload.json"))
for a,b in [("c2-p1a","c2-p1b"),("c2-p2a","c2-p2b"),("c2-p3a","c2-p3b")]:
    A,Bb=ev(a),ev(b)
    ea={ (e["op"],e.get("id",e.get("target")),e["t"],json.dumps(e,sort_keys=True)) for e in A["events"]}
    eb={ (e["op"],e.get("id",e.get("target")),e["t"],json.dumps(e,sort_keys=True)) for e in Bb["events"]}
    da=sorted({(x[0],x[1]) for x in ea-eb}); db=sorted({(x[0],x[1]) for x in eb-ea})
    print(a,b,"only-in-a:",da,"only-in-b:",db)
    print("  gt a:",[(g["t_start"],g["mode"],g["attributes"]) for g in A["ground_truth"]])
    print("  gt b:",[(g["t_start"],g["mode"],g["attributes"]) for g in Bb["ground_truth"]])
