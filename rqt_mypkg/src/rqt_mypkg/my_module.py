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
from .utils.utility import Utility
from qt_gui.plugin import Plugin
from python_qt_binding import loadUi
from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtCore import * 
from PyQt5.QtWidgets import *
from rospkg import RosPack
from .utils import utility
from argparse import ArgumentParser
from .topicDialog import TopicDialog

packageRoot = ""
def dropEvent(*event) :
    return
    # QString format = event.mimeData().formats().at(0)
    # QByteArray data = event->mimeData()->data(format);
    # QDataStream stream(&data, QIODevice::ReadOnly);

    # int r, c;
    # QStandardItem *sitem = new QStandardItem;
    # stream >> r >> c >> *sitem;

    # qDebug() << r << "-" << c << sitem->text();


def addIteminTree(topLevel, itemToInsert):
    item = QTreeWidgetItem()
    item.setText(0, itemToInsert)
    topLevel.addChild(item)

def addNode(nodeToInsert):
    print("HERE")
    print(nodeToInsert)
    print(type(nodeToInsert))
    # item = QTreeWidgetItem()
    # item.setText(0, nodeToInsert)
    # packageRoot.addChild(item)
    
def createModule(items, scene, graph):
    if(len(items) >0 ) :
        childrens = items[0].takeChildren()
        #Il controllo viene fatto dentro la creazione del nodo
        #Graph.createNode(graph, items[0].text(0), childrens)
        #Utility.createXmlFile(graph)

    topicdialog = TopicDialog()
    topicdialog.exec()
    topic = topicdialog.get_topic()
    #scene.addItem(Utility.createRect(topic)) 
    print("TOPIC INSERT ")
    print(topic)    
    painter = QPainter()
    rec = QRectF(0, 0, 100, 100)
    painter.drawRect(rec)
    rect_graph = QGraphicsRectItem(rec)
    rect_graph.setFlag(QGraphicsItem.ItemIsMovable, True)
    rect_graph.setPen(Qt.red)
    scene.addItem(rect_graph)
    # file = QFileInfo("../resource/modules.png")
    # appIcon = QFileIconProvider().icon(file).pixmap(50, QIcon.Normal, QIcon.On)
    # pixmap = QPixmap(appIcon)
    # pitem2 = QGraphicsPixmapItem(pixmap)
    
    # pitem2.setPos(0,0)   
    # scene.addItem(pitem2)
    # pitem2.setFlag(QGraphicsItem.ItemIsMovable, True)
    
    # image = QImage(QSize(500, 500),QImage.Format_RGB32)
    # rect = QRectF(500, 500, 500,500)
    # painter = QPainter(image)
    # painter.setBrush(QBrush(Qt.green))
    # painter.fillRect(rect, Qt.blue)
    # painter.fillRect(rect,Qt.red)
    # painter.setPen(QPen(Qt.red))
    # painter.setFont(QFont( "Courier", 100))
    # painter.drawText(rect,"prova")
    # gg =  QPixmap.fromImage(image)
    # painter.end()
    # scene.addPixmap(gg)

    
    


def createItem(text):
    item = QTreeWidgetItem()
    item.setText(0, text)
    return item
        
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
        scene =  QGraphicsScene()
        topMsgLevel = QTreeWidgetItem()
        topNodesLevel = QTreeWidgetItem()
        messages = ""
        rosGraph = Graph.createGraph("ROS graph")
        # Get path to UI file which should be in the "resource" folder of this package
        ui_file = os.path.join(rosPack.get_path('rqt_mypkg'), 'resource', 'MyPlugin.ui')
        # Extend the widget with all attributes and children from UI file
        loadUi(ui_file, self)
        # Give QObjects reasonable names
        self.setWindowTitle("Visual Tool")
        
        context.add_widget(self)
        
        workflowView = self.workflowView
        workflowView.setScene(scene)
        
        # rospack list-names
        packages = rosPack.list()
        packages.sort()
        packageTreeWidget = self.packageTree
        topNodesLevel.setText(0, "ROS Packages-Nodes")
        
        # nodes = rosnode.get_node_names()
        # print(nodes)
        msgTreeWidget = self.msgTree
        topMsgLevel.setText(0, "ROS Nodes-Messages")
        
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
        
        packageTreeWidget.itemDoubleClicked.connect(lambda: createModule(packageTreeWidget.selectedItems(), scene, rosGraph))
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