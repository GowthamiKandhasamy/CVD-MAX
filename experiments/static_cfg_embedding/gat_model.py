import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GATConv, GCNConv, global_mean_pool

class GATEncoder(nn.Module):
    def __init__(self, in_dim, hidden_dim, out_dim, heads=4):
        super().__init__()

        self.use_gcn_fallback = True  # safety for tiny graphs

        # GAT layers
        self.gat1 = GATConv(in_dim, hidden_dim, heads=heads, concat=True)
        self.gat2 = GATConv(hidden_dim * heads, hidden_dim, heads=1, concat=True)

        # GCN fallback layers
        self.gcn1 = GCNConv(in_dim, hidden_dim)
        self.gcn2 = GCNConv(hidden_dim, hidden_dim)

        self.lin = nn.Linear(hidden_dim, out_dim)

    def forward(self, data):
        x, edge_index, batch = data.x, data.edge_index, data.batch

        #  If graph is too small or too sparse → use GCN (stable)
        if self.use_gcn_fallback and edge_index.size(1) < x.size(0):
            # GCN path (stable for tiny graphs)
            x = self.gcn1(x, edge_index)
            x = F.relu(x)
            x = self.gcn2(x, edge_index)
            x = F.relu(x)
        else:
            # GAT path (attention)
            x = self.gat1(x, edge_index)
            x = F.leaky_relu(x)
            x = self.gat2(x, edge_index)
            x = F.leaky_relu(x)

        # Pool nodes → graph embedding
        x = global_mean_pool(x, batch)

        z = self.lin(x)
        return z
