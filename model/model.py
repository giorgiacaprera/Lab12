import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        """Definire le strutture dati utili"""
        # TODO
        self.G = nx.Graph()
        self.id_map = {}

    def build_weighted_graph(self, year: int):
        """
        Costruisce il grafo pesato dei rifugi considerando solo le connessioni con campo `anno` <= year passato
        come argomento.
        Il peso del grafo è dato dal prodotto "distanza * fattore_difficolta"
        """
        # TODO
        self.G.clear()
        rifugi = DAO.get_all_rifugi_grafo(year)
        connessioni = DAO.get_connessioni_pesate(year)

        for r in rifugi:
            self.G.add_node(r['id'], nome=r['nome'])
            self.id_map[r['nome']] = r['nome']

        fattori = {'facile': 1.0, 'media': 1.5, 'difficile': 2.0}

        for c in connessioni:
            u, v = c['id_rifugio1'], c['id_rifugio2']
            if u in self.G and v in self.G:
                peso = c['distanza']*fattori.get(c['difficolta'].lower(), 1.0)
                self.G.add_edge(u,v, weight=peso)

    def get_edges_weight_min_max(self):
        """
        Restituisce min e max peso degli archi nel grafo
        :return: il peso minimo degli archi nel grafo
        :return: il peso massimo degli archi nel grafo
        """
        # TODO
        if not self.G.edges: return 0, 0
        weights = [d['weight'] for u, v, d in self.G.edges(data=True)]
        return min(weights), max(weights)

    def count_edges_by_threshold(self, soglia):
        """
        Conta il numero di archi con peso < soglia e > soglia
        :param soglia: soglia da considerare nel conteggio degli archi
        :return minori: archi con peso < soglia
        :return maggiori: archi con peso > soglia
        """
        # TODO
        minori = sum(1 for u, v, d in self.G.edges(data=True) if d['weight'] < soglia)
        maggiori = sum(1 for u, v, d in self.G.edges(data=True) if d['weight'] > soglia)
        return minori, maggiori

"""Implementare la parte di ricerca del cammino minimo"""
    # TODO
    def get_cammino_minimo(self, soglia):
        sub_g = nx.Graph()
        sub_g.add_nodes_from(self.G.nodes(data=True))
        for u, v, d in self.G.edges(data=True):
            if d['weight'] > soglia:
                sub_g.add_edge(u, v, weight=d['weight'])

        best_path = []
        min_total_weight = float('inf')

        nodes = list(sub_g.nodes())
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                try:
                    path = nx.shortest_path(sub_g, source=nodes[i], target=nodes[j], weight='weight')
                    if len(path) >= 3:
                        w = nx.path_weight(sub_g, path, weight='weight')
                        if w < min_total_weight:
                            min_total_weight = w
                            best_path = path
                except nx.NetworkXNoPath:
                    continue
        return [(self.id_map[node], node) for node in best_path], min_total_weight
