# Documentation for Hu-sidian v1.py

#py
#visualization #graph #networkx #pyqt #markdown #metadata #relationships #explorer #vault

The code provided is a Python script that implements an interactive graph visualization of an Obsidian vault using the NetworkX library. Here's a step-by-step guide on how the script works:

1. Importing necessary libraries: The script imports the necessary libraries for building and rendering the graph, including NetworkX (nx) and PyQt5 for creating the user interface.
2. Creating a class for the graph visualization: The `GraphViewer` class is created to manage the graph visualization. It has several methods that allow users to interact with the graph, such as adding nodes, edges, and updating layout settings.
3. Extracting metadata from Markdown files: The script scans all Markdown files in the vault folder and extracts tags and wiki-style links using regular expressions. This data is used to build the graph.
4. Building the graph: The script builds a graph with nodes representing files and edges representing relationships between them. Tags are represented as separate nodes, and wiki-style links are also represented as separate nodes.
5. Drawing the graph: Once the graph is built, it is drawn using PyQt5's graphics view widget. Users can interact with the graph by adding/removing nodes, edges, or updating layout settings.
6. Updating graph forces: The `update_forces` method updates the graph layout based on user input from the sliders.
7. Filtering the graph: The `update_graph` method filters the graph based on a search query provided by the user. It creates a new graph with only nodes and edges that match the search query, and renders it in the same graphics view widget.
8. Main function: The script's main function is responsible for creating an instance of the `GraphViewer` class, setting up the user interface, and running the event loop to handle user input.

Overall, this code provides a convenient way to visualize and explore the relationships between files in an Obsidian vault using the power of NetworkX and PyQt5.
