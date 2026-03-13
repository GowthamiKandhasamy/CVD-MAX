import pickle
import torch
import os
import sys
import networkx as nx
from simple_gnn import SimpleGraphEncoder

print("Starting run_embedding_simple.py...")

if len(sys.argv) < 2:
    print("Usage: python run_embedding_simple.py <cfg.pkl>")
    exit(1)

cfg_file = sys.argv[1]

with open(cfg_file, "rb") as f:
    G = pickle.load(f)

print("Loaded CFG")

# Build node list
nodes = list(G.nodes())
node_to_idx = {n: i for i, n in enumerate(nodes)}

# Build X
X = []
for n in nodes:
    feat = G.nodes[n].get("x", [])
    if feat is None or len(feat) == 0:
        raise ValueError(f"Node {n} has no features")
    X.append(feat)

X = torch.tensor(X, dtype=torch.float)

N = X.size(0)

# Build adjacency matrix with self-loops
A = torch.zeros((N, N), dtype=torch.float)

for u, v in G.edges():
    if u in node_to_idx and v in node_to_idx:
        i = node_to_idx[u]
        j = node_to_idx[v]
        A[i, j] = 1.0

# Add self-loops
for i in range(N):
    A[i, i] = 1.0

print("Built adjacency matrix:", A.shape)

model = SimpleGraphEncoder(in_dim=X.size(1), hidden_dim=64, out_dim=128)
print("Model created")

model.eval()
with torch.no_grad():
    emb = model(X, A)
    print("Embedding shape:", emb.shape)
    print("Embedding (first 10 values):", emb[:10])

# Save
out_name = os.path.splitext(cfg_file)[0] + "_embedding.pt"
torch.save(emb, out_name)
print("Saved embedding to:", os.path.abspath(out_name))
