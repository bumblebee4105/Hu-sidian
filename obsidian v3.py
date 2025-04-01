import sys
import os
import re
import networkx as nx
from pyvis.network import Network
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QVBoxLayout, QWidget, QLineEdit, QLabel
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl

class ObsidianGraphApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.vault_path = None  # Store selected vault path
        self.graph = nx.Graph()  # Graph object
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

        # WebView to show the HTML Graph
        self.web_view = QWebEngineView(self)

        # Add widgets to layout
        layout.addWidget(self.label)
        layout.addWidget(self.vault_btn)
        layout.addWidget(self.search_bar)
        layout.addWidget(self.graph_btn)
        layout.addWidget(self.web_view)  # Embed graph in GUI

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
                    self.graph.add_node(file, label=file, color="lightblue")
                    files[file] = {"tags": tags, "links": links}

                    # Add tag relations
                    for tag in tags:
                        tag_node = f"#{tag}"
                        self.graph.add_node(tag_node, label=tag, color="green")
                        self.graph.add_edge(file, tag_node)

        # Add file-to-file links
        for file, data in files.items():
            for link in data["links"]:
                linked_file = f"{link}.md"
                if linked_file in files:  # Ensure linked file exists
                    self.graph.add_edge(file, linked_file, color="gray")

    def generate_graph(self):
        """Creates and displays an interactive HTML graph inside the app."""
        self.build_graph()

        net = Network(notebook=False, cdn_resources="local")  # Use local JS
        net.from_nx(self.graph)

        graph_html = "graph.html"
        net.write_html(graph_html)

        # Load in PyQt WebEngineView
        self.web_view.setUrl(QUrl.fromLocalFile(os.path.abspath(graph_html)))

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

        net = Network(notebook=False, cdn_resources="local")  # Use local JS
        net.from_nx(filtered_graph)

        filtered_graph_html = "filtered_graph.html"
        net.write_html(filtered_graph_html)

        # Load in PyQt WebEngineView
        self.web_view.setUrl(QUrl.fromLocalFile(os.path.abspath(filtered_graph_html)))

if __name__ == "__main__":
    app = QApplication(sys.argv)  # ✅ Fix: Pass sys.argv to QApplication
    window = ObsidianGraphApp()
    window.show()
    sys.exit(app.exec())  # ✅ Fix: Properly handle app exit
