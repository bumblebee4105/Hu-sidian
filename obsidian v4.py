import os
import re
import networkx as nx
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QPushButton, 
    QVBoxLayout, QWidget, QLineEdit, QLabel, QGraphicsScene, 
    QGraphicsView, QGraphicsEllipseItem, QGraphicsTextItem, 
    QGraphicsLineItem, QSlider, QToolTip
)
from PyQt6.QtGui import QBrush, QPen, QPainter
from PyQt6.QtCore import Qt

class InteractiveNode(QGraphicsEllipseItem):
    """Custom node class to handle interactions like hover and click."""
    
    def __init__(self, name, graph_viewer, x, y):
        super().__init__(x - 5, y - 5, 10, 10)
        self.name = name
        self.graph_viewer = graph_viewer
        self.setBrush(QBrush(Qt.GlobalColor.blue))
        self.setAcceptHoverEvents(True)
        self.edges = []  # Store edges connected to this node

    def hoverEnterEvent(self, event):
        """Highlight node and its edges on hover."""
        self.setBrush(QBrush(Qt.GlobalColor.red))  # Change node color
        for edge in self.edges:
            edge.setPen(QPen(Qt.GlobalColor.red, 2))  # Highlight edges
        QToolTip.showText(event.screenPos(), self.name)

    def hoverLeaveEvent(self, event):
        """Restore node and edge colors when hover ends."""
        self.setBrush(QBrush(Qt.GlobalColor.blue))  # Restore node color
        for edge in self.edges:
            edge.setPen(QPen(Qt.GlobalColor.gray, 1))

class GraphViewer(QGraphicsView):
    """Graph Viewer with interactive nodes and force-directed layout."""
    
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.graph = nx.Graph()
        self.nodes = {}
        self.edges = {}

        # Default force layout parameters
        self.center_force = 0.1
        self.link_force = 0.5
        self.link_distance = 300
        self.repel_force = 1.0

        # Enable zoom & pan
        self.scale_factor = 1.0
        self.setRenderHints(QPainter.RenderHint.Antialiasing)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)

    def wheelEvent(self, event):
        """Handle zooming using the mouse wheel."""
        zoom_in_factor = 1.25
        zoom_out_factor = 0.8

        if event.angleDelta().y() > 0:
            self.scale(zoom_in_factor, zoom_in_factor)
        else:
            self.scale(zoom_out_factor, zoom_out_factor)

    def update_forces(self, center, link, distance, repel):
        """Update force layout settings and redraw the graph."""
        self.center_force = center / 100.0
        self.link_force = link / 100.0
        self.link_distance = distance / 10.0
        self.repel_force = repel / 100.0
        self.draw_graph()

    def draw_graph(self):
        """Draws the network graph with force-directed layout."""
        self.scene.clear()
        self.nodes.clear()
        self.edges.clear()

        # Apply force-directed layout
        pos = nx.spring_layout(
            self.graph,
            center=(0, 0),
            k=self.link_distance / 1000,
            scale=500,
            iterations=int(self.repel_force * 10)
        )

        # Draw edges
        edge_items = {}
        for edge in self.graph.edges:
            p1 = pos[edge[0]]
            p2 = pos[edge[1]]
            line = QGraphicsLineItem(p1[0] * 10, p1[1] * 10, p2[0] * 10, p2[1] * 10)
            line.setPen(QPen(Qt.GlobalColor.gray, 1))
            self.scene.addItem(line)
            edge_items[edge] = line

        # Draw nodes
        for node, (x, y) in pos.items():
            node_item = InteractiveNode(node, self, x * 10, y * 10)
            text = QGraphicsTextItem(node)
            text.setPos(x * 10 + 8, y * 10)

            self.scene.addItem(node_item)
            self.scene.addItem(text)
            self.nodes[node] = node_item

        # Link nodes to their edges for highlighting
        for edge, line in edge_items.items():
            self.nodes[edge[0]].edges.append(line)
            self.nodes[edge[1]].edges.append(line)

    def get_file_path(self, node_name):
        """Retrieve the file path for a node (if it's a file)."""
        return self.nodes.get(node_name, None)

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

        # Force Control Sliders
        self.center_slider = self.create_slider(0, 100, 10, "Center Force")
        self.link_slider = self.create_slider(0, 100, 50, "Link Force")
        self.distance_slider = self.create_slider(1, 50, 30, "Link Distance")
        self.repel_slider = self.create_slider(0, 100, 10, "Repel Force")

        # Connect slider updates
        for slider in [self.center_slider, self.link_slider, self.distance_slider, self.repel_slider]:
            slider["slider"].valueChanged.connect(self.update_forces)

        # Add components to layout
        layout.addWidget(self.label)
        layout.addWidget(self.vault_btn)
        layout.addWidget(self.search_bar)
        layout.addWidget(self.graph_btn)

        # Add sliders
        for slider in [self.center_slider, self.link_slider, self.distance_slider, self.repel_slider]:
            layout.addWidget(slider["label"])
            layout.addWidget(slider["slider"])

        layout.addWidget(self.graph_viewer)

        # Set main container
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def create_slider(self, min_val, max_val, default, label_text):
        """Helper function to create a slider with a label."""
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setMinimum(min_val)
        slider.setMaximum(max_val)
        slider.setValue(default)
        
        label = QLabel(f"{label_text}: {default}")
        slider.valueChanged.connect(lambda value: label.setText(f"{label_text}: {value}"))
        
        return {"slider": slider, "label": label}

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
                        self.graph.add_node(tag_node, label=tag)
                        self.graph.add_edge(file, tag_node)

        # Add file-to-file links
        for file, data in files.items():
            for link in data["links"]:
                linked_file = f"{link}.md"
                if linked_file in files:
                    self.graph.add_edge(file, linked_file)

    def generate_graph(self):
        """Creates and renders the interactive graph."""
        self.build_graph()
        self.graph_viewer.draw_graph()

    def update_forces(self):
        """Updates the graph layout when sliders are changed."""
        self.graph_viewer.update_forces(
            self.center_slider["slider"].value(),
            self.link_slider["slider"].value(),
            self.distance_slider["slider"].value(),
            self.repel_slider["slider"].value()
        )

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
                    filtered_graph.add_edge(node, neighbor)

        self.graph_viewer.graph = filtered_graph
        self.graph_viewer.draw_graph()

    # def update_forces(self):
    #     """Updates the graph layout when sliders are changed."""
    #     self.graph_viewer.update_forces(
    #         self.center_slider["slider"].value(),
    #         self.link_slider["slider"].value(),
    #         self.distance_slider["slider"].value(),
    #         self.repel_slider["slider"].value()
    #     )

if __name__ == "__main__":
    app = QApplication([])
    window = ObsidianGraphApp()
    window.show()
    app.exec()
