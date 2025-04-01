# Documentation for obsidian v2.py

#py
##tags ##graph ##PyVis ##QT ##Obsidian ##graphviewer ##metadata ##networkx ##interactive


This code is a Python script that creates an interactive graph viewer for the Obsidian note-taking app using PyVis and QT. The viewer allows users to select a vault directory, search for notes or tags, and view the relationships between them in a graph.

Here's a detailed explanation of each part of the code:

1. Importing necessary libraries:
The first few lines import the necessary libraries for the program, including PyVis, QT6, and other Python packages. These libraries are used to create an interactive graph viewer and handle user input.
2. Defining the `ObsidianGraphApp` class:
This is the main class of the script, which inherits from QMainWindow and contains all the necessary methods for creating and managing the graph viewer. The `__init__()` method is the constructor of the class, which initializes the attributes of the class and sets up the user interface.
3. Initializing the UI:
The `initUI()` method is used to set up the user interface of the graph viewer. It creates a new QWidget object and adds several widgets to it, including a label for selecting the vault directory, a button for choosing the vault directory, a search bar for searching notes or tags, and a button for generating the graph.
4. Selecting the vault directory:
The `select_vault()` method is used to open a file dialog box that allows users to select an Obsidian vault (folder) on their computer. The selected vault path is then stored in the `self.vault_path` attribute.
5. Extracting metadata from Markdown files:
The `extract_metadata()` method is used to extract tags and wiki-style links from a Markdown file. It uses regular expressions to find all occurrences of #tags and [[Links]] in the file, and then returns them as a tuple.
6. Building the graph:
The `build_graph()` method is used to recursively scan all .md files in a directory and build a graph of their relationships. It uses the `nx` package to create an empty graph object and add nodes and edges for each file, tag, and link found in the Markdown files.
7. Generating the graph:
The `generate_graph()` method is used to create an interactive HTML graph of the built graph using PyVis. It uses the `Network` class from PyVis to create a new instance of the Network object and add all nodes and edges from the built graph. The `write_html()` method is then called on this instance to save the generated graph as an HTML file, which can be opened in a web browser.
8. Updating the graph:
The `update_graph()` method is used to filter the graph based on search input entered by the user. It creates a new filtered graph object and adds only the nodes that match the search query. The edges between these nodes are then added to the filtered graph as well.
9. Running the script:
Finally, the script is run using `app.exec()`, which starts the event loop of the QT application and allows it to handle user input.
