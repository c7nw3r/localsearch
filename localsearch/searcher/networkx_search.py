from typing import List, Optional

from localsearch import ScoredDocument
from localsearch.__spi__ import Writer, Reader, Documents, Traverser


class NetworkxSearch(Traverser, Reader, Writer):

    def __init__(self, path: Optional[str]):
        import networkx as nx
        if path is not None:
            self.graph = nx.read_graphml(path)
        else:
            self.graph = nx.Graph()

    def read(self, text: str, n: Optional[int] = None) -> List[ScoredDocument]:
        # TODO: implement
        pass

    def append(self, documents: Documents):
        nodes = [(e.id, e.fields) for e in documents]
        self.graph.add_nodes_from(nodes)

    def remove(self, idx: int):
        pass

    def add_node(self, node_id: str, fields: dict):
        self.graph.add_nodes_from([(node_id, fields)])

    def add_edge(self, source_id: str, target_id: str, edge_type: str):
        edge = {"source_id": source_id, "target_id": target_id, "type": edge_type}
        self.graph.add_edges_from([source_id, target_id, edge])

    def get_edges(self, node_id: str):
        edges = self.graph.edges(node_id, data=True)
        return [edge[2] for edge in edges]

    def search_by_type(self, node_type: str):
        nodes = self.graph.nodes(data=True)
        nodes = filter(lambda x: x[1]["type"] == node_type, nodes)
        return list(map(lambda x: x[1], nodes))

    def search_by_id(self, node_id: str):
        nodes = self.graph.nodes(data=True)
        nodes = filter(lambda x: x[0] == node_id, nodes)
        return list(map(lambda x: x[1], nodes))[0]

    def _save(self):
        import networkx as nx
        nx.write_graphml(self.graph, "./graph.ml")
