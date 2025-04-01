# Documentation for obsidian v2.py

#py
#Obsidian #Graph #Networkx #Pyvis #PyQt6 #UI #Search #Filter #Vault #Relationship


The provided code is a Python script that creates an interactive graph viewer for the Obsidian note-taking app using the PyQt6 library and the networkx library to perform graph operations. The script defines several classes, including `ObsidianGraphApp`, which represents the main window of the application.

Here's a detailed analysis of the code:

1. Imports: The script imports various libraries, including `os`, `re`, and `networkx` (for graph operations) as well as `pyvis` for creating interactive graphs and `PyQt6.QtWidgets` for building the user interface.
2. Class definition: The script defines a class named `ObsidianGraphApp` that inherits from `QMainWindow`. This class is responsible for creating the graph viewer UI and handling user input.
3. Initialization: In the initialization method, the constructor of the parent class is called to create a new instance of `QMainWindow`. The window title is set to "Obsidian Graph Viewer", and its geometry is set to 400x200 pixels.
4. Select vault button: A select vault button is created using `QPushButton` that opens a file dialog to select an Obsidian vault (folder) when clicked. The selected folder path is stored in the `vault_path` attribute of the class instance.
5. Search bar and generate graph button: Two more buttons are created, one for searching notes or tags using a search bar (`QLineEdit`) and another for generating an interactive HTML graph of the relationships between notes when clicked. The search bar is connected to the `update_graph` method, which filters the graph based on the user input and regenerates the HTML file with the filtered graph.
6. Graph generation: The `generate_graph` method creates a new instance of the `Network` class from the `pyvis` library and populates it with nodes and edges from the `Graph` object created by the `build_graph` method. The `build_graph` method recursively scans all .md files in the selected vault directory, extracts tags and wiki-style links using regular expressions, and builds a graph of the relationships between notes.
7. Update graph: This method is connected to the search bar's textChanged event, which filters the graph based on the user input and regenerates the HTML file with the filtered graph.
8. Main loop: The script enters the main loop using `app.exec()` and starts the event loop for the application, allowing it to process events and respond to user input.

Overall, this code creates a simple but powerful graph viewer that allows users to explore their Obsidian notes by searching for tags or filtering the graph based on specific criteria.
