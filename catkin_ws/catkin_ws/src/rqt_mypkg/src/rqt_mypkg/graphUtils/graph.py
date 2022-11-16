import graphviz
import networkx as nx
import matplotlib.pyplot  as plt
import io
from xml.sax.saxutils import escape
import string

class Graph:
    def createGraph(graphName):
        graph = nx.DiGraph(comment = graphName)
        graph.add_node('ROOT')
        return graph
    
    def createEdge(graph, node1, node2):
        graph.add_edge(node1, node2)

    def createTopicEdge(graph, node1, node2, edge):
        graph.add_edge(node1, node2, name=edge)
    
    def createNode(graph, nodeName, childList):
        graph.add_node(nodeName)
        Graph.createEdge(graph, 'ROOT', nodeName)
        if(childList!=None):
            if(len(childList) >0):
                for t in childList :
                    graph.add_node(t.text(0))
                    Graph.createEdge(graph, nodeName, t.text(0))
        print("OK STAMPO IL GRAFO")
        print(graph.nodes())
        print(graph.edges())

    def createXml(graph):
        G = nx.path_graph(4)
        nx.write_gexf(G, "/home/ylenia/Desktop/output.gexf")
        fh = io.BytesIO()
        nx.write_gexf(graph, fh)
        fh.seek(0)
        print(nx.read_gexf(fh))

    def createRoslaunchfile(dataXml):
        inner_template = string.Template('   <node name="${name}" pkg="${pkg}" type="${type}"/>')

        outer_template = string.Template("""<launch>
            ${document_list}
        </launch>
        """)

        data = dataXml

        inner_contents = [inner_template.substitute(name=name, pkg=pkg, type=typex) for (name, pkg, typex) in data]
        result = outer_template.substitute(document_list='\n'.join(inner_contents))
        roslaunchFile = open("/home/ylenia/Desktop/rosLaunch.xml", "wt")
        roslaunchFile.write(result)
        roslaunchFile.close()