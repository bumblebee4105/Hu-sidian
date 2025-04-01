import os
import re
import networkx as nx
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QPushButton, 
    QVBoxLayout, QWidget, QLineEdit, QLabel, QGraphicsScene, QGraphicsView,
    QGraphicsEllipseItem, QGraphicsTextItem, QGraphicsLineItem
)
from PyQt6.QtGui import QBrush, QPen
from PyQt6.QtCore import Qt

class GraphViewer(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.graph = nx.Graph()
        self.nodes = {}

    def draw_graph(self):
        """Draws the network graph in the PyQt UI."""
        self.scene.clear()
        pos = nx.spring_layout(self.graph)  # Compute node positions

        # Draw edges
        for edge in self.graph.edges:
            p1 = pos[edge[0]]
            p2 = pos[edge[1]]
            line = QGraphicsLineItem(p1[0] * 500, p1[1] * 500, p2[0] * 500, p2[1] * 500)
            line.setPen(QPen(Qt.GlobalColor.gray, 1))
            self.scene.addItem(line)

        # Draw nodes
        for node, (x, y) in pos.items():
            ellipse = QGraphicsEllipseItem(x * 500 - 5, y * 500 - 5, 10, 10)
            ellipse.setBrush(QBrush(Qt.GlobalColor.blue))
            text = QGraphicsTextItem(node)
            text.setPos(x * 500 + 8, y * 500)

            self.scene.addItem(ellipse)
            self.scene.addItem(text)
            self.nodes[node] = ellipse

class ObsidianGraphApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.vault_path = None  # Store selected vault path
        self.graph_viewer = GraphViewer()  # Custom graph viewer
        self.graph = self.graph_viewer.graph  # Access graph structure
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Obsidian Graph Viewer")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        # Label
        self.label = QLabel("Select your Obsidian vault:", self)

        # Select Vault Button
        self.vault_btn = QPushButton("Choose Vault", self)
        self.vault_btn.clicked.connect(self.select_vault)

        # Search Bar
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search for notes or tags...")
        self.search_bar.textChanged.connect(self.update_graph)

        # Generate Graph Button
        self.graph_btn = QPushButton("Generate Graph", self)
        self.graph_btn.clicked.connect(self.generate_graph)

        # Add widgets to layout
        layout.addWidget(self.label)
        layout.addWidget(self.vault_btn)
        layout.addWidget(self.search_bar)
        layout.addWidget(self.graph_btn)
        layout.addWidget(self.graph_viewer)  # Add the native graph viewer

        # Set central widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def select_vault(self):
        """Opens file dialog to select an Obsidian vault (folder)."""
        folder = QFileDialog.getExistingDirectory(self, "Select Vault Folder")
        if folder:
            self.vault_path = folder
            self.label.setText(f"Vault: {os.path.basename(folder)}")

    def extract_metadata(self, file_path):
        """Extracts tags (#tag) and wiki-style links ([[Link]]) from a Markdown file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        tags = set(re.findall(r'#(\w+)', content))  # Extract #tags
        links = set(re.findall(r'\[\[([^\]]+)\]\]', content))  # Extract [[Links]]

        return tags, links

    def build_graph(self):
        """Recursively scans .md files in a directory and builds a graph of their relationships."""
        self.graph.clear()
        files = {}

        if not self.vault_path:
            return

        # Scan recursively for .md files
        for root, _, filenames in os.walk(self.vault_path):
            for file in filenames:
                if file.endswith(".md"):
                    file_path = os.path.join(root, file)
                    tags, links = self.extract_metadata(file_path)

                    # Add file node
                    self.graph.add_node(file, label=file)
                    files[file] = {"tags": tags, "links": links}

                    # Add tag relations
                    for tag in tags:
                        tag_node = f"#{tag}"
                        self.graph.add_node(tag_node, label=tag)
                        self.graph.add_edge(file, tag_node)

        # Add file-to-file links
        for file, data in files.items():
            for link in data["links"]:
                linked_file = f"{link}.md"
                if linked_file in files:  # Ensure linked file exists
                    self.graph.add_edge(file, linked_file)

    def generate_graph(self):
        """Creates and renders the interactive graph inside PyQt."""
        self.build_graph()
        self.graph_viewer.draw_graph()  # Render inside PyQt

    def update_graph(self):
        """Filters the graph based on search input."""
        query = self.search_bar.text().strip().lower()
        if not query:
            self.generate_graph()
            return

        filtered_graph = nx.Graph()
        for node in self.graph.nodes:
            if query in node.lower():
                filtered_graph.add_node(node, **self.graph.nodes[node])
                for neighbor in self.graph.neighbors(node):
                    filtered_graph.add_node(neighbor, **self.graph.nodes[neighbor])
                    filtered_graph.add_edge(node, neighbor, **self.graph[node][neighbor])

        self.graph_viewer.graph = filtered_graph
        self.graph_viewer.draw_graph()

if __name__ == "__main__":
    app = QApplication([])
    window = ObsidianGraphApp()
    window.show()
    app.exec()
