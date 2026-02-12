import torch
import sys
import os

if len(sys.argv) < 2:
    print("Usage: python view_embedding.py <embedding.pt>")
    exit(1)

emb_file = sys.argv[1]

print("Loading:", emb_file)
emb = torch.load(emb_file, map_location="cpu")

print("Type:", type(emb))
print("Shape:", emb.shape)

# Print full vector (careful: it's long)
print("\nFull embedding:\n", emb)

# Or just first 10 values
print("\nFirst 10 values:\n", emb[0, :10])

# Some quick sanity checks
print("\nMin value:", emb.min().item())
print("Max value:", emb.max().item())
print("Mean value:", emb.mean().item())
