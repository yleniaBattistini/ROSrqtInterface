from curses import A_COLOR
import os
from platform import node
from sys import stdout
from pkg_resources import WorkingSet
import rosgraph
import rospy
import rospkg
import rostopic
import rosnode
import rosmsg
import subprocess
from .graphUtils.graph import Graph
#from .utils.utility import Utility
from qt_gui.plugin import Plugin
from python_qt_binding import loadUi
from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtCore import * 
from PyQt5.QtWidgets import *
from rospkg import RosPack
#from .utils import utility
from argparse import ArgumentParser
from .topicDialog import TopicDialog
from pyqtgraph.flowchart import Flowchart, Node
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui as qg
import pyqtgraph.flowchart.library as fclib


packageRoot = ""
customNodeArray = ['actionlib', 'turtlesim', 'turtle_teleop_key', 'rosbag', 'rqt_image_view']
nodesList= []
ROSg = Graph.createGraph("ROS graph")
dataxml = []


def addIteminTree(topLevel, itemToInsert):
    item = QTreeWidgetItem()
    item.setText(0, itemToInsert)
    topLevel.addChild(item)

def createNgxNode(name, childrens):
    Graph.createNode(ROSg, name, childrens)
    
def createModule(items, graph):
    #Set custom node name
    customNodeName = items[0].text(0)
    parent = items[0].parent().text(0)
    #print(customNodeName.parent())
    if customNodeName in customNodeArray:
        node = graph.createNode(customNodeName, pos= (0,0))
        if(len(items) >0) :
            childrens = items[0].takeChildren()
            #It's possible create node with childrens

def addXmlItem(nodeName, parent):
    if parent != "ROS Packages-Nodes":
        dataxml.append((nodeName, parent, nodeName))
    else : 
        dataxml.append((nodeName, nodeName, nodeName))

def printTerminalConnections(graph):
    connections = graph.listConnections()
    for c in connections:
        print(c)
        for i in range(len(c)-1):
            node1 = c[i].node().name()
            node2 = c[i+1].node().name()
            tmp = str(node1)
            tmp2 = str(node2)
            if(node1!="Input" or node2!="Output"):
                edge1= tmp.replace("<Terminal " + node1,"").replace(".", "").replace(">", "")
                edge2= tmp.replace("<Terminal " + node2,"").replace(".", "").replace(">", "")
                Graph.createTopicEdge(ROSg, node1, node2, edge1 + " " + edge2)
    
    Graph.createXml(ROSg)
    Graph.createRoslaunchfile(dataxml)
  
def createItem(text):
    item = QTreeWidgetItem()
    item.setText(0, text)
    return item

def set_rosGraph(rosg):
    ROSg = rosg
        
class MyPlugin(Plugin):

    def __init__(self, context):
        super(MyPlugin, self).__init__(context)
        # Give QObjects reasonable names
        self.setObjectName('MyPlugin')
        rosPack= RosPack()
        # Process standalone plugin command-line arguments
        parser = ArgumentParser()
        # Add argument(s) to the parser.
        parser.add_argument("-q", "--quiet", action="store_true",
                      dest="quiet",
                      help="Put plugin in silent mode")
        args, unknowns = parser.parse_known_args(context.argv())
        if not args.quiet:
            print("arguments: ", args)
            print("unknowns: ", unknowns)

        # Create QWidget
        self = QWidget()
        #scene =  QGraphicsScene()
        topMsgLevel = QTreeWidgetItem()
        topNodesLevel = QTreeWidgetItem()
        messages = ""
        #rosGraph = Graph.createGraph("ROS graph")
        #set_rosGraph(rosGraph)
        # Get path to UI file which should be in the "resource" folder of this package
        ui_file = os.path.join(rosPack.get_path('rqt_mypkg'), 'resource', 'MyPlugin.ui')
        # Extend the widget with all attributes and children from UI file
        loadUi(ui_file, self)
        # Give QObjects reasonable names
        self.setWindowTitle("Visual Tool HRI")
        
        context.add_widget(self)
        
        workflowView = self.widgetFlow
        self.layout = qg.QGridLayout()

        workflowView.setLayout(self.layout)
        fc = Flowchart(terminals ={
            'dataIn': {'io': 'in'},#in
            'dataOut': {'io': 'out'}#out
        })

        library = fclib.LIBRARY.copy()
        library.addNodeType(ActionLib, [('Custom_node',)])
        library.addNodeType(TurtleSim, [('Custom_node',)])
        library.addNodeType(TeleopTurtle, [('Custom_node',)])
        library.addNodeType(RosBag, [('Custom_node',)])
        library.addNodeType(RqtImageView, [('Custom_node',)])
        fc.setLibrary(library)
        self.layout.addWidget(fc.widget())

        # rospack list-names
        packages = rosPack.list()
        packages.sort()
        packageTreeWidget = self.packageTree
        topNodesLevel.setText(0, "ROS Packages-Nodes")
        
        # nodes = rosnode.get_node_names()
        # print(nodes)
        msgTreeWidget = self.msgTree
        topMsgLevel.setText(0, "ROS Nodes-Messages")

        runBtn = self.runBtn
        runBtn.clicked.connect(lambda:printTerminalConnections(fc))
        
        for p in packages:
            packageNodesItem = createItem(p)
            packageMsgItem = createItem(p)
            topNodesLevel.addChild(packageNodesItem)
            topMsgLevel.addChild(packageMsgItem)
            
            s = subprocess.check_output(['./rospack-list-executables.bash', p])
            nodes = list(s.decode("utf-8").split('\n'))
            nodes.remove('')
            
            for n in nodes:
                addIteminTree(packageNodesItem, n)
                
            messages = rosmsg.list_msgs(p)
            for m in messages:
                addIteminTree(packageMsgItem, "[PUB]" + m)
           
        # for n in nodes:
        #     #Adding ros nodes in tree (set root.)
        #     nodeItem = QTreeWidgetItem()
        #     nodeItem.setText(0, n)
        #     topNodeLevel.addChild(nodeItem)
        #     #Obtain ros noeds for each package
        #     nodesDescription = rosnode.get_node_info_description(n).split('\n')
        #     indexServ = nodesDescription.index('Services: ')
        #     print(nodesDescription)
        #     if 'Publications: ' in nodesDescription :
        #         indexPub = nodesDescription.index('Publications: ')
        #         if 'Subscriptions: ' in nodesDescription : 
        #             indexSub = nodesDescription.index('Subscriptions: ')
        #             for tPub in range(indexPub + 1, indexSub -1 , 1):
        #                 addIteminTree(nodeItem, "[PUB]" + nodesDescription[tPub])
        #             for tSub in range(indexSub + 1, indexServ -1, 1):
        #                 addIteminTree(nodeItem, "[SUB]" + nodesDescription[tSub])
            
        packageTreeWidget.addTopLevelItem(topNodesLevel)
        msgTreeWidget.addTopLevelItem(topMsgLevel)
        
        packageTreeWidget.itemDoubleClicked.connect(lambda: createModule(packageTreeWidget.selectedItems(), fc))
        #nodesTreeWidget.itemDoubleClicked.connect(lambda: createModule(nodesTreeWidget.selectedItems(), scene, rosGraph))
        
        
  
    def shutdown_plugin(self):
        # TODO unregister all publishers here
        pass

    def save_settings(self, plugin_settings, instance_settings):
        # TODO save intrinsic configuration, usually using:
        # instance_settings.set_value(k, v)
        pass

    def restore_settings(self, plugin_settings, instance_settings):
        # TODO restore intrinsic configuration, usually using:
        # v = instance_settings.value(k)
        pass

class ActionLib(Node):
    nodeName = 'actionlib'
        
    def __init__(self, name):
        self.view = None
        parent = self.nodeName
        #dialog
        topicdialog = TopicDialog()
        topicdialog.exec()
        #Get input topic
        inputCustomNode = topicdialog.get_topicInput()
        #Get output topic
        outputCustomNode = topicdialog.get_topicOutput()
        Node.__init__(self, name, terminals={inputCustomNode: {'io': 'in'}, outputCustomNode: {'io': 'out'}})
        Graph.createNode(ROSg, name, None)
        addXmlItem(self.nodeName, parent)

    def setView(self, view):  ## setView must be called by the program
        self.view = view


class TurtleSim(Node):
    nodeName = 'turtlesim'
        
    def __init__(self, name):
        self.view = None
        parent = self.nodeName
        #dialog
        topicdialog = TopicDialog()
        topicdialog.exec()
        #Get input topic
        inputCustomNode = topicdialog.get_topicInput()
        #Get output topic
        outputCustomNode = topicdialog.get_topicOutput()
        Node.__init__(self, name, terminals={inputCustomNode: {'io': 'in'}, outputCustomNode: {'io': 'out'}})   
        Graph.createNode(ROSg, name, None)
        addXmlItem(self.nodeName, parent)
            
    def setView(self, view):  ## setView must be called by the program
        self.view = view
            
    def process(self, data, display=True):
        print("connetto")
         ## if process is called with display=False, then the flowchart is being operated
          ## in batch processing mode, so we should skip displaying to improve performance.


class TeleopTurtle(Node):
    nodeName = 'turtle_teleop_key'
        
    def __init__(self, name):
        self.view = None
        parent = "turtlesim"
        #dialog
        topicdialog = TopicDialog()
        topicdialog.exec()
        #Get input topic
        inputCustomNode = topicdialog.get_topicInput()
        #Get output topic
        outputCustomNode = topicdialog.get_topicOutput()
        Node.__init__(self, name, terminals={inputCustomNode: {'io': 'in'}, outputCustomNode: {'io': 'out'}})    
        Graph.createNode(ROSg, name, None)
        addXmlItem(self.nodeName, parent)

    def setView(self, view):  ## setView must be called by the program
        self.view = view


class RosBag(Node):
    nodeName = 'rosbag'
        
    def __init__(self, name):
        self.view = None    
        parent = self.nodeName
        #dialog
        topicdialog = TopicDialog()
        topicdialog.exec()
        #Get input topic
        inputCustomNode = topicdialog.get_topicInput()
        #Get output topic
        outputCustomNode = topicdialog.get_topicOutput()
        Node.__init__(self, name, terminals={inputCustomNode: {'io': 'in'}, outputCustomNode: {'io': 'out'}})    
        Graph.createNode(ROSg, name, None)
        addXmlItem(self.nodeName, parent)

    def setView(self, view):  ## setView must be called by the program
        self.view = view


class RqtImageView(Node):
    nodeName = 'rqt_image_view'
        
    def __init__(self, name):
        self.view = None
        parent = self.nodeName
        #dialog
        topicdialog = TopicDialog()
        topicdialog.exec()
        #Get input topic
        inputCustomNode = topicdialog.get_topicInput()
        #Get output topic
        outputCustomNode = topicdialog.get_topicOutput()
        Node.__init__(self, name, terminals={inputCustomNode: {'io': 'in'}, outputCustomNode: {'io': 'out'}})    
        Graph.createNode(ROSg, name, None)
        addXmlItem(self.nodeName, parent)
        

    def setView(self, view):  ## setView must be called by the program
        self.view = view

        