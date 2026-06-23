import copy

from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._graph=nx.Graph()
        self._avvistamenti=[]
        self._idMapA={}
        self._bestPath = []
        self._bestScore = 0

    def getBestPath(self):
        self._bestPath=[]
        self._bestScore=0
        for start in self._graph.nodes:
            parziale=[start]
            self._ricorsione(parziale)
        return self._bestPath, self._bestScore
    def _ricorsione(self, parziale):
        if self._bestScore<self._getScore(parziale):
            self._bestPath=copy.deepcopy(parziale)
            self._bestScore=self._getScore(parziale)
        current=parziale[-1]
        for successor in self._graph.neighbors(current):
            mese=successor.datetime.month
            if successor not in parziale and self._getAvvistamentiPerMese(parziale).get(mese, 0)<3 and current.duration<successor.duration:
                parziale.append(successor)
                self._ricorsione(parziale)
                parziale.pop()


    def _getAvvistamentiPerMese(self, parziale):
        avvistamenti={}
        for n in parziale:
            mese=n.datetime.month
            if mese not in avvistamenti:
                avvistamenti[mese]=0
            avvistamenti[mese]+=1
        return avvistamenti
    def _getScore(self, parziale):
        score=100
        for i in range(0, len(parziale)-1):
            if parziale[i].datetime.month!=parziale[i+1].datetime.month:
                score+=100
            else:
                score+=300
        return score






    def buildGraph(self, year, state):
        self._graph.clear()
        self._avvistamenti=DAO.get_all_sightings(year, state)
        for a in self._avvistamenti:
            self._idMapA[a.id]=a
        self._graph.add_nodes_from(self._avvistamenti)
        for u in self._avvistamenti:
            for v in self._avvistamenti:
                if u.shape==v.shape and u.id!=v.id and u.distance_HV(v)<100:
                    self._graph.add_edge(u, v)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getAllYears(self):
        return DAO.get_all_years()
    def getAllStates(self, year):
        return DAO.get_all_states(year)

    def getInfoConnessa(self):
        components=list(nx.connected_components(self._graph))
        largest=max(components, key=len)
        return len(components), largest


