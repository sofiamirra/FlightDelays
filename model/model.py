import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._airports = DAO.getAllAirports()
        # Dizionario che collega all'id l'oggetto Aeroporto
        self._idMapAirports = {}
        for a in self._airports:
            self._idMapAirports[a.ID] = a


    def buildGraph(self, nMin):
        self._graph.clear()
        nodes = DAO.getAllNodes(nMin, self._idMapAirports)
        self._graph.add_nodes_from(nodes)
        self._addEdges()

    def _addEdges(self):
        allTratte = DAO.getAllEdges(self._idMapAirports)

        # Queste tratte hanno due problemi: i) archi diretti e inversi (necessario sommarli)
        # ii) ho archi fra aeroporti che avevo filtrato
        for t in allTratte:
            # Se i nodi sono già stati inseriti nel grafo
            if t.aeroportoP in self._graph and t.aeroportoA in self._graph:
                # Se l'arco era già stato aggiunto nel grafo, incremento il peso
                if self._graph.has_edge(t.aeroportoP, t.aeroportoA):
                    self._graph[t.aeroportoP][t.aeroportoA]['weight'] += t.peso
                # Altrimenti, lo aggiungo direttamente
                self._graph.add_edge(t.aeroportoP, t.aeroportoA, weight=t.peso)

    def getGraphDetails(self):
        # Restituiamo una tupla con il numero di nodi e il numero di archi
        return len(self._graph.nodes), len(self._graph.edges)

    def getAllNodes(self):
        nodes = list(self._graph.nodes)
        nodes.sort(key=lambda x: x.IATA_CODE)
        return nodes
