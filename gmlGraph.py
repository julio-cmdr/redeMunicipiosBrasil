import igraph
from igraph import Graph
import pandas as pd
import json

class gmlGraph():

    def __init__(self):

        """
        self.ufs = {}
        with open('dados/estados.json','r') as fd:
            
            for tupla in json.load(fd):
                self.ufs[tupla["id"]] = tupla["sigla"]

        df = pd.read_csv('dados/novo_municipios.csv')
        df['nome'] = [ nome.upper() for nome in df['nome']]

        # Adicionando ao dataset um coluna de estados.
        siglas = []
        for row in df.itertuples():
            siglas.append(self.ufs[row.codigo_uf])

        df['estado'] = siglas
        df.to_csv('dados/novo_municipios.csv', index=False)
        """

        df = pd.read_csv('dados/novo_municipios.csv')

        self.estados = {}
        
        cont = 0
        # Para cada cidade.
        for row in df.itertuples():
            # Se o código dos estados ainda não existe no dicionário.
            if row.estado not in self.estados:
                self.estados[row.estado] = {}
            # Se a cidade ainda não existe no dicionário do estado.
            if row.nome not in self.estados[row.estado]:
                self.estados[row.estado][row.nome] = [row.codigo_ibge, \
                    row.latitude, \
                    row.longitude, \
                    row.capital]
            # Verificando se existe cidades duplicadas.
            else:
                print("Duplicate: ", row.nome)
        
        df = pd.read_csv('municipiosVizinhos.csv')
        
        cidades = []
        # Identificando o conjunto total de cidades.
        for row in df.itertuples():
            cidades.append(row.A+'--'+row.EstadoA)
            cidades.append(row.B+'--'+row.EstadoB)
        
        cidades = list(set(cidades))
        cidades.sort()
        # Atribuindo as cidades IDs únicos.
        cont = 0
        d_cids = {}
        for c in cidades:
            cidade, estado = c.split('--')
            if estado in self.estados:
                if cidade in self.estados[estado]:
                    # Atribuindo o ID de ordem léxica e o do IBGE.
                    d_cids[c] = [cont, self.estados[estado][cidade][0]]
                    cont += 1
        
        arestas = []
        # Construindo as arestas do grafo.
        for row in df.itertuples():
            # Se ambas as cidades existirem.
            if row.EstadoA in self.estados and \
                row.A in self.estados[row.EstadoA] and \
                row.EstadoB in self.estados and \
                row.B in self.estados[row.EstadoB]:
                arestas.append([
                    d_cids[row.A+'--'+row.EstadoA][0],
                    d_cids[row.B+'--'+row.EstadoB][0],
                ])
        
        g = Graph()
        g.add_vertices(len(cidades))
        g.add_edges(arestas)
        for i in range(len(cidades)):
            if cidades[i] in d_cids:
                #g.vs[i]["id"] = d_cids[cidades[i]][1]
                g.vs[i]["name"] = d_cids[cidades[i]][1]
                g.vs[i]["label"] = cidades[i].split('--')[0]
        
        layout = g.layout_kamada_kawai()
        igraph.plot(g,"dados/rede.pdf", layout=layout, bbox = (9000, 9000))
        g.save("dados/rede.gml", format="gml")

if __name__=='__main__':

    g = gmlGraph()
