import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.pesoMin = 0
        self.cammino = []
        self.graph = None
        self.idmap = {}

    def get_cromosomi(self):
        return DAO.get_cromosomi()

    def buildGraph(self, cMin, cMax):
        self.graph = nx.DiGraph()
        allNodes = DAO.getAllNodes(cMin, cMax)
        for n in allNodes:
            self.idmap[n.GeneID] = n
        self.graph.add_nodes_from(allNodes)
        allArchi = DAO.getAllArchi(cMin, cMax)
        for g1,g2,p in allArchi:
            if self.idmap[g1].Chromosome < self.idmap[g2].Chromosome:
                self.graph.add_edge(self.idmap[g1], self.idmap[g2], weight = p)
            elif self.idmap[g2].Chromosome < self.idmap[g1].Chromosome:
                self.graph.add_edge(self.idmap[g2], self.idmap[g1], weight = p)
            else:
                self.graph.add_edge(self.idmap[g1], self.idmap[g2], weight=p)
                self.graph.add_edge(self.idmap[g2], self.idmap[g1], weight = p)


    def getGraphDetails(self):
        return self.graph.number_of_nodes(), self.graph.number_of_edges()

    def getNodiMaxConNum(self):
        nodiConNumArchiUscenti = []
        for n in self.graph.nodes():
            numUscenti = len(list(nx.neighbors(self.graph, n)))
            pesoUscenti = 0
            for v in nx.neighbors(self.graph, n):
                pesoUscenti += self.graph[n][v]['weight']
            nodiConNumArchiUscenti.append((n, numUscenti, pesoUscenti))

        nodiConNumArchiUscenti.sort(key=lambda x:x[1], reverse=True)
        return nodiConNumArchiUscenti[0:5]

    def getMaxCammino(self):
        for n in self.graph.nodes():
            self.ricorsione([n])
        return self.cammino, self.pesoMin

    def ricorsione(self, parziale):
        if len(parziale) > len(self.cammino):
            if self.calcolaPeso(parziale) < self.pesoMin:
                self.cammino = copy.deepcopy(parziale)
                self.pesoMin = self.calcolaPeso(parziale)
            else:
                for v in nx.neighbors(self.graph, parziale[-1]):
                    if self.condizione(parziale, parziale[-1], v):
                        parziale.append(v)
                        self.ricorsione(parziale)
                        parziale.pop()

    def calcolaPeso(self, parziale):
        pesoTot = 0
        for i in range(len(parziale)-1):
            nodo1 = parziale[i]
            nodo2 = parziale[i+1]
            pesoTot += self.graph[nodo1][nodo2]['weight']
        return pesoTot

    def condizione(self, parziale, n, v):
        if v in parziale:
            return False
        ultimo = parziale[-1]
        penultimo = parziale[len(parziale)-2]
        if self.graph[ultimo][v]['weight'] >= self.graph[penultimo][ultimo]['weight']:
            if ultimo.Essential == v.Essential:
                return False
            else:
                return True
        return False


