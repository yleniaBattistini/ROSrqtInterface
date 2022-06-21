import graphviz
import networkx as nx
import matplotlib.pyplot  as plt
import io

class Graph:
    def createGraph(graphName):
        graph = nx.DiGraph(comment = graphName)
        graph.add_node('ROOT')
        return graph
    
    def createEdge(graph, node1, node2):
        graph.add_edge(node1, node2)
    
    def createNode(graph, nodeName, topicsList):
        graph.add_node(nodeName)
        Graph.createEdge(graph, 'ROOT', nodeName)
        if(len(topicsList)>0):
            for t in topicsList :
                graph.add_node(t.text(0))
                Graph.createEdge(graph, nodeName, t.text(0))
        print("OK STAMPO IL GRAFO")
        print(graph.nodes())
        print(graph.edges())
        G = nx.path_graph(4)
        nx.write_gexf(G, "/home/ylenia/Desktop/tryRqt/test.gexf")
        fh = io.BytesIO()
        nx.write_gexf(graph, fh)
        fh.seek(0)
        print(nx.read_gexf(fh))
   
    
# class Graph:
#     def createGraph(graphName):
#         graph = graphviz.Digraph(comment = graphName)
#         graph.node('ROOT', 'Root')
#         return graph

#     def createNode(graph, nodeName, topicsList):
#         graph.node(nodeName, nodeName)
#         graph.edge('ROOT', nodeName)
#         if(len(topicsList)>0):
#             for t in topicsList :
#                 graph.node(t.text(0), t.text(0))
#                 graph.edge(nodeName, t.text(0)) 
#         print(graph)         

#     def createEdge(graph, topic1, topic2):
#         graph.edge(topic1, topic2)