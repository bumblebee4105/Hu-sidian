# Documentation for obsidian v3.py

#py
#graph #obsidian #networkx #pyvis #qt #markdown #visualization #html #app #vault


This code defines a graph viewer for the Obsidian note-taking application using PyQt6 and NetworkX. The user can select an Obsidian vault folder, extract tags and wiki-style links from Markdown files, and generate an interactive HTML graph of the relationships between them.

Here's a detailed breakdown of each line of code:

1. `import sys`: This imports the system module, which provides functions for interacting with the operating system and managing processes.
2. `import os`: This imports the operating system module, which provides functions for interacting with the file system and other operating system-related tasks.
3. `import re`: This imports the regular expression module, which allows for pattern matching and searching within strings.
4. `import networkx as nx`: This imports the NetworkX library, which is a Python library for creating, modifying, and analyzing complex networks.
5. `from pyvis.network import Network`: This imports the Network class from the PyVis library, which provides functions for creating interactive visualizations of graph data.
6. `from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QVBoxLayout, QWidget, QLineEdit, QLabel`: This imports various Qt widgets from the PyQt6 library, which are used to create the user interface for the graph viewer.
7. `from PyQt6.QtWebEngineWidgets import QWebEngineView`: This imports the QWebEngineView class from the PyQt6 library, which is a widget that allows you to display web pages within your application.
8. `from PyQt6.QtCore import QUrl`: This imports the QUrl class from the PyQt6 library, which is used for working with URLs and other web-related tasks.
9. `class ObsidianGraphApp(QMainWindow)`: This defines a subclass of QMainWindow that represents the main window of the graph viewer application.
10. `__init__(self)`: This is the constructor method for the ObsidianGraphApp class, which initializes the widgets and sets up the user interface.
11. `self.setCentralWidget(QWidget())`: This sets the central widget of the main window to a new QWidget instance.
12. `self.setLayout(QVBoxLayout())`: This sets the layout manager for the central widget to a vertical box layout, which arranges the child widgets vertically.
13. `self.select_vault_button = QPushButton("Select Vault")`: This creates a new QPushButton instance and adds it to the vertical box layout. The button text is set to "Select Vault".
14. `self.select_vault_button.clicked.connect(self.select_vault)`: This connects the clicked signal of the select vault button to the select_vault method.
15. `self.graph = nx.Graph()`: This creates a new NetworkX graph instance, which will be used to store the data for the graph viewer.
16. `self.build_graph()`: This method is called when the user clicks the select vault button, and it builds the graph based on the selected vault folder.
17. `self.generate_graph()`: This method creates an interactive HTML graph of the relationships between the nodes in the graph using PyVis.
18. `self.update_graph()`: This method filters the graph based on search input from the user and updates the display to show only the filtered graph.
19. `if __name__ == "__main__"`: This line of code is used to guard the execution of the main function, which is used for testing purposes.
20. `app = QApplication(sys.argv)`: This creates a new instance of the QApplication class and passes it the command-line arguments.
21. `window = ObsidianGraphApp()`: This creates a new instance of the ObsidianGraphApp class and sets it as the main window for the application.
22. `window.show()`: This shows the main window for the application.
23. `sys.exit(app.exec())`: This method is used to properly handle the exit of the application, which ensures that all resources are released and the application exits cleanly.
