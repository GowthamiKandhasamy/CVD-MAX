import pickle
import torch
import os
import sys
from nxtopyg import nx_to_pyg
from gat_model import GATEncoder

print("Starting run_embedding.py...")

if len(sys.argv) < 2:
    print("Usage: python run_embedding.py <cfg.pkl>")
    exit(1)

cfg_file = sys.argv[1]

with open(cfg_file, "rb") as f:
    G = pickle.load(f)

print("Loaded CFG")

data = nx_to_pyg(G)
print("Converted to PyG Data:", data)

# Add batch vector (single graph)
data.batch = torch.zeros(data.num_nodes, dtype=torch.long)

model = GATEncoder(in_dim=data.x.shape[1], hidden_dim=64, out_dim=128)
print("Model created")

model.eval()
with torch.no_grad():
    print("Running model forward pass...")
    emb = model(data)
    print("Embedding shape:", emb.shape)
    print("Embedding (first 10 values):", emb[0, :10])

# Save
out_name = os.path.splitext(cfg_file)[0] + "_embedding.pt"
torch.save(emb, out_name)
print("Saved embedding to:", os.path.abspath(out_name))
