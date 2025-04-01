# Documentation for obsidian v3.py

#py
#graphviz #obsidian #PyQt6 #networkx #graph_viewer #UI #app #visualization #interactive #metadata


This code is a Python script that creates an interactive graph viewer for the Obsidian note-taking app. The graph is displayed using the PyQt6 library, which provides a set of tools for creating GUI applications in Python.

The script starts by importing various modules from the Python standard library and third-party libraries, including `os`, `re`, `networkx` (for handling graphs), `PyQt6.QtWidgets`, and `PyQt6.QtGui`. It also defines a custom graph viewer class called `GraphViewer` that inherits from `QGraphicsView`.

The `ObsidianGraphApp` class is then defined, which is responsible for handling the user interface (UI) of the application. The constructor of this class sets up the UI elements and connections between them. It also defines a number of helper functions, including `select_vault`, `extract_metadata`, `build_graph`, `generate_graph`, and `update_graph`.

The `main` function at the end of the script creates an instance of the `ObsidianGraphApp` class and starts the UI event loop using `app.exec()`. This allows the user to interact with the application by clicking on nodes in the graph, which will display more information about the node in a pop-up window.

Here is a detailed explanation of each part of the script:

1. Importing modules and libraries: The first few lines of the script import various Python modules and third-party libraries that are needed for this application. These include `os` (for handling operating system tasks), `re` (for regular expression matching), `networkx` (for handling graphs), `PyQt6.QtWidgets` (for creating GUI elements in Python), and `PyQt6.QtGui` (for handling graphics).
2. Defining the custom graph viewer class: The `GraphViewer` class is defined as a subclass of `QGraphicsView`. This class provides a way to display and interact with graphs in an interactive way, using Qt's graphics framework. It has several methods for drawing nodes, edges, and other graph elements, as well as handling user input events such as mouse clicks.
3. Defining the main application class: The `ObsidianGraphApp` class is defined as a subclass of `QWidget`. This class provides the UI elements and connections between them that make up the application. It also defines several helper functions, including `select_vault`, `extract_metadata`, `build_graph`, `generate_graph`, and `update_graph`.
4. Constructor: The constructor of the `ObsidianGraphApp` class sets up the UI elements and connections between them. It creates a main window with a title bar, a menu bar, and a central widget containing the graph viewer. It also defines the layout of the main window and connects the necessary signals and slots for user input events.
5. Main function: The `main` function at the end of the script creates an instance of the `ObsidianGraphApp` class and starts the UI event loop using `app.exec()`. This allows the user to interact with the application by clicking on nodes in the graph, which will display more information about the node in a pop-up window.

Overall, this script provides an example of how to use Python and Qt to create a graph viewer for Obsidian notes using the networkx library for handling graphs. The code is well structured and easy to understand, making it a useful resource for anyone looking to create their own interactive graph visualization applications in Python.
