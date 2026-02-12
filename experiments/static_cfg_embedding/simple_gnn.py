import torch
import torch.nn as nn
import torch.nn.functional as F

class SimpleGraphEncoder(nn.Module):
    def __init__(self, in_dim, hidden_dim, out_dim):
        super().__init__()
        self.lin1 = nn.Linear(in_dim, hidden_dim)
        self.lin2 = nn.Linear(hidden_dim, hidden_dim)
        self.lin_out = nn.Linear(hidden_dim, out_dim)

    def forward(self, X, A):
        # Message passing 1
        H = torch.matmul(A, X)
        H = self.lin1(H)
        H = F.relu(H)

        # Message passing 2
        H = torch.matmul(A, H)
        H = self.lin2(H)
        H = F.relu(H)

        # Global mean pooling
        g = H.mean(dim=0)

        # Project to embedding
        emb = self.lin_out(g)
        return emb
