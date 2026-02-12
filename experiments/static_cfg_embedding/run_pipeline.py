import pickle
import sys
import os
import networkx as nx

def has_port_nodes(G):
    for n in G.nodes():
        if isinstance(n, str) and ":" in n:
            return True
    return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python run_pipeline.py <cfg.pkl>")
        exit(1)

    cfg_file = sys.argv[1]

    with open(cfg_file, "rb") as f:
        G = pickle.load(f)

    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    port_nodes = has_port_nodes(G)

    print("CFG:", cfg_file)
    print("Nodes:", num_nodes, "Edges:", num_edges, "Port nodes:", port_nodes)

    # Decision logic
    if num_nodes < 4 or num_edges <=2:
        print("→ Using SIMPLE encoder (fallback)")
        os.system(f"python run_embedding_simple.py {cfg_file}")
    else:
        print("→ Using GAT/GCN encoder")
        os.system(f"python run_embedding.py {cfg_file}")

if __name__ == "__main__":
    main()
