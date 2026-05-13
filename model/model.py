import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._graph = nx.Graph() # inizializzazione grafo
        # Carichiamo tutti gli Aeroporti per mapparli nel dizionario
        self._airports = DAO.getAllAirports()
        self._idMapAirports = {}
        for a in self._airports:
            self._idMapAirports[a.ID] = a

    def buildGraph(self, nMin):
        """Metodo per la creazione del grafico"""
        self._graph.clear() # reset per analisi multiple
        # 1. Aggiunge i Nodi (filtrati dal DAO)
        nodes = DAO.getAllNodes(nMin, self._idMapAirports)
        self._graph.add_nodes_from(nodes)
        # 2. Aggiunge gli Archi
        self._addEdges()

    def _addEdges(self):
        """Recupera le rotte e popola gli archi del grafo"""
        allTratte = DAO.getAllEdges(self._idMapAirports)
        # Le tratte hanno due problemi:
        # i) il grafo è "non orientato", perciò bisogna sommare tutte le tratte
        # (Milano --> Roma = Roma --> Milano)
        # ii) gli archi devono essere compresi tra gli aeroporti filtrati

        for t in allTratte:
            # Mi assicuro che l'aeroporto di partenza e destinazione siano tra quelli
            # con almeno N compagnie di volo (ovvero nodi del grafo)
            if t.aeroportoP in self._graph and t.aeroportoA in self._graph:
                # Se l'arco (Milano --> Roma o Roma --> Milano) è già stato aggiunto
                if self._graph.has_edge(t.aeroportoP, t.aeroportoA):
                    # incrementa il peso dell'arco in questione
                    self._graph[t.aeroportoP][t.aeroportoA]['weight'] += t.peso
                # Altrimenti, creo l'arco nuovo e gli assegno il peso
                self._graph.add_edge(t.aeroportoP, t.aeroportoA, weight=t.peso)

    def getGraphDetails(self):
        """Restituisce le tuple per la View"""
        # Restituiamo una tupla con il numero totale di nodi e archi
        return len(self._graph.nodes), len(self._graph.edges)

    def getAllNodes(self):
        """Restituisce i nodi del grafo ordinati per IATA_CODE (per il menù a tendina)"""
        nodes = list(self._graph.nodes)
        nodes.sort(key=lambda x: x.IATA_CODE)
        return nodes
