import torch
from torch_geometric.data import Data
import networkx as nx

def nx_to_pyg(G: nx.MultiDiGraph):
    # Map node ids to indices
    nodes = list(G.nodes())
    node_to_idx = {n: i for i, n in enumerate(nodes)}

    # Build node feature matrix
    X = []
    for n in nodes:
        feat = G.nodes[n].get("x", None)
        if feat is None or len(feat) == 0:
            raise ValueError(f"Node {n} has no feature vector!")
        X.append(feat)

    x = torch.tensor(X, dtype=torch.float)

    # Build edge index
    edges = []
    for u, v in G.edges():
        edges.append([node_to_idx[u], node_to_idx[v]])

    if len(edges) == 0:
        edge_index = torch.empty((2, 0), dtype=torch.long)
    else:
        edge_index = torch.tensor(edges, dtype=torch.long).t().contiguous()

    data = Data(x=x, edge_index=edge_index)

    return data
