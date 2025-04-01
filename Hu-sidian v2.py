import os
import re
import networkx as nx
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QPushButton, 
    QVBoxLayout, QWidget, QLineEdit, QLabel, QGraphicsScene, 
    QGraphicsView, QGraphicsEllipseItem, QGraphicsTextItem, 
    QGraphicsLineItem, QSlider, QToolTip
)
from PyQt6.QtGui import QBrush, QPen, QPainter, QColor
from PyQt6.QtCore import Qt, QTimer
import math
import random

DISTANCE_MULTIPLIER = 10

def obsidian_dark_theme():
    return """
        QWidget {
            background-color: #1e1e1e;
            color: #dcdcdc;
            font-family: 'Inter', 'Source Sans Pro', sans-serif;
        }
        QPushButton {
            background-color: #282828;
            border-radius: 5px;
            padding: 8px;
        }
        QPushButton:hover {
            background-color: #3c3c3c;
        }
        QLabel {
            color: #ffffff;
        }
        QLineEdit {
            background-color: #282828;
            border: 1px solid #555;
            padding: 5px;
            border-radius: 5px;
        }
        QGraphicsView {
            border: none;
        }
    """

class InteractiveNode(QGraphicsEllipseItem):
    def __init__(self, name, graph_viewer, x, y):
        super().__init__(-5, -5, 10, 10)
        self.name = name
        self.graph_viewer = graph_viewer
        self.setBrush(QBrush(QColor("#8e44ad")))
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsEllipseItem.GraphicsItemFlag.ItemIsMovable)

        self.edges = []
        self.velocity = [random.uniform(-1, 1), random.uniform(-1, 1)]
        self.dragging = False
        self.setPos(x, y)

        # 🌟 Create the text label
        self.label = QGraphicsTextItem(name)
        self.label.setDefaultTextColor(QColor("#dcdcdc"))
        self.label.setZValue(2)  # Keep text above nodes
        graph_viewer.scene.addItem(self.label)
        self.update_label_position()

    def update_label_position(self):
        """Position label slightly offset from the node."""
        self.label.setPos(self.x() + 12, self.y() - 8)

    def setX(self, x):
        super().setX(x)
        self.update_label_position()

    def setY(self, y):
        super().setY(y)
        self.update_label_position()

class GraphViewer(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.graph = nx.Graph()
        self.nodes = {}
        self.edges = {}

        # Default force layout parameters
        self.center_force = 0.01
        self.link_force = 0.5
        self.repel_force = 1.2
        self.tag_link_distance = 100  # Tags stay close
        self.md_link_distance = 300
        self.structure_link_distance = 700  # Structure nodes stay apart
        self.link_distance = 750.0
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_physics)
        self.timer.start(30)

        # Enable zoom & pan
        self.scale_factor = 1.0
        self.setRenderHints(QPainter.RenderHint.Antialiasing)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setBackgroundBrush(QBrush(QColor("#1e1e1e")))

    def wheelEvent(self, event):
        """Handle zooming using the mouse wheel."""
        zoom_in_factor = 1.25
        zoom_out_factor = 0.8

        if event.angleDelta().y() > 0:
            self.scale(zoom_in_factor, zoom_in_factor)
        else:
            self.scale(zoom_out_factor, zoom_out_factor)

    def is_tag_node(self, node_name):
        """Identify tag nodes."""
        return node_name.startswith("#")
    
    def is_md_node(self, node_name):
        """Identify tag nodes."""
        return node_name.endswith(".md")

    def get_link_distance(self, node1, node2):
        """Return preferred link distance based on node type."""
        if self.is_tag_node(node1) or self.is_tag_node(node2):
            return self.tag_link_distance
        if self.is_md_node(node1) or self.is_md_node(node2):
            return self.md_link_distance
        return self.structure_link_distance

    def draw_graph(self):
        self.scene.clear()
        self.nodes.clear()
        self.edges.clear()

        pos = nx.spring_layout(self.graph, k=self.link_distance / 1000, scale=500)

        for node, (x, y) in pos.items():
            node_item = InteractiveNode(node, self, x * DISTANCE_MULTIPLIER, y * DISTANCE_MULTIPLIER)
            self.scene.addItem(node_item)
            self.nodes[node] = node_item

        for edge in self.graph.edges:
            node1, node2 = self.nodes[edge[0]], self.nodes[edge[1]]
            line = QGraphicsLineItem()
            line.setPen(QPen(Qt.GlobalColor.gray, 1))
            self.scene.addItem(line)
            self.edges[(edge[0], edge[1])] = line
            node1.edges.append(line)
            node2.edges.append(line)

    def update_physics(self):
        k = 50
        strength = 0.005
        repel_strength = 1000

        for node in self.nodes.values():
            if node.dragging:
                continue

            fx, fy = 0, 0

            for neighbor in self.graph.neighbors(node.name):
                if neighbor in self.nodes:
                    other = self.nodes[neighbor]
                    dx, dy = other.x() - node.x(), other.y() - node.y()
                    distance = math.sqrt(dx**2 + dy**2) or 0.1
                    preferred_distance = self.get_link_distance(node.name, neighbor)  # 🔥 Dynamic distance
                    
                    force = (distance - preferred_distance) * strength
                    fx += dx / distance * force
                    fy += dy / distance * force

            for other in self.nodes.values():
                if other is node:
                    continue
                dx, dy = other.x() - node.x(), other.y() - node.y()
                distance = math.sqrt(dx**2 + dy**2) or 0.1
                if distance < k:
                    force = repel_strength / (distance**2)
                    fx -= dx / distance * force
                    fy -= dy / distance * force

            node.velocity[0] = (node.velocity[0] + fx) * 0.9
            node.velocity[1] = (node.velocity[1] + fy) * 0.9
            node.setX(node.x() + node.velocity[0])
            node.setY(node.y() + node.velocity[1])

            # Update edges
            for edge in node.edges:
                other_node = self.get_other_edge_node(edge, node)
                if other_node:
                    edge.setLine(node.x(), node.y(), other_node.x(), other_node.y())

    def get_other_edge_node(self, edge, node):
        for edge_nodes, line in self.edges.items():
            if edge_nodes[0] == node.name:
                return self.nodes[edge_nodes[1]]
            elif edge_nodes[1] == node.name:
                return self.nodes[edge_nodes[0]]
        return None


class ObsidianGraphApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.vault_path = None
        self.graph_viewer = GraphViewer()
        self.graph = self.graph_viewer.graph
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Obsidian Graph Viewer")
        self.setGeometry(100, 100, 1000, 700)
        layout = QVBoxLayout()

        # UI Components
        self.label = QLabel("Select your Obsidian vault:")
        self.vault_btn = QPushButton("Choose Vault")
        self.vault_btn.clicked.connect(self.select_vault)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search for notes or tags...")
        self.search_bar.textChanged.connect(self.generate_graph)

        self.graph_btn = QPushButton("Generate Graph")
        self.graph_btn.clicked.connect(self.generate_graph)

        # Add components to layout
        layout.addWidget(self.label)
        layout.addWidget(self.vault_btn)
        layout.addWidget(self.search_bar)
        layout.addWidget(self.graph_btn)

        layout.addWidget(self.graph_viewer)

        # Set main container
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.setStyleSheet(obsidian_dark_theme())

    def select_vault(self):
        """Opens file dialog to select an Obsidian vault (folder)."""
        folder = QFileDialog.getExistingDirectory(self, "Select Vault Folder")
        if folder:
            self.vault_path = folder
            self.label.setText(f"Vault: {os.path.basename(folder)}")

    def extract_metadata(self, file_path):
        """Extracts tags and wiki-style links from Markdown files."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        tags = set(re.findall(r'#(\w+)', content))
        links = set(re.findall(r'\[\[([^\]]+)\]\]', content))
        return tags, links

    def build_graph(self):
        """Scans .md files and builds a graph with relationships."""
        self.graph.clear()
        files = {}

        if not self.vault_path:
            return

        # Scan .md files
        for root, _, filenames in os.walk(self.vault_path):
            for file in filenames:
                if file.endswith(".md"):
                    file_path = os.path.join(root, file)
                    tags, links = self.extract_metadata(file_path)

                    # Store node with filepath
                    self.graph.add_node(file, label=file)
                    files[file] = {"tags": tags, "links": links}

                    # Add tag relations
                    for tag in tags:
                        tag_node = f"#{tag}"
                        print(tag_node)
                        print(file)
                        self.graph.add_edge(tag, file)
                        self.graph.add_edge(tag_node, file)

        # Add file-to-file links
        for file, data in files.items():
            for link in data["links"]:
                linked_file = f"{link}.md"
                if linked_file in files:
                    self.graph.add_edge(file, linked_file)

    def generate_graph(self):
        self.build_graph()
        self.graph_viewer.draw_graph()

    # def generate_graph(self):
    #     self.graph.clear()
    
    #     # 🏗 Structure nodes
    #     self.graph.add_edge("A", "B")
    #     self.graph.add_edge("B", "C")
    #     self.graph.add_edge("C", "D")
    
    #     # 🔖 Tag nodes (stay close)
    #     self.graph.add_edge("#tag_urgent", "A")
    #     self.graph.add_edge("#tag_todo", "B")
    #     self.graph.add_edge("#tag_review", "C")
    
    #     self.graph_viewer.draw_graph()

if __name__ == "__main__":
    app = QApplication([])
    window = ObsidianGraphApp()
    window.show()
    app.exec()
