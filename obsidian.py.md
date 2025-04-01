# Documentation for obsidian.py

#py
#metadata #graph #pyvis #obsidian #relationships #visualization #nodes #edges #extract #build


This code defines a few functions for extracting metadata from Markdown files, building a graph of file relationships based on that metadata, and creating an interactive HTML visualization of the graph using the `pyvis` library. Here's a breakdown of each function:

1. `extract_metadata`: This function takes a path to a Markdown file as input and extracts two sets of data from it: tags (denoted by `#tags`) and wiki-style links (`[[Link]]`). It returns a tuple containing these two sets.
2. `build_graph`: This function scans all `.md` files in a given directory and builds a graph of their relationships based on the metadata extracted using `extract_metadata`. It creates nodes for each file, tags, and wiki-style links, and adds edges between them to represent the relationships. The resulting graph is returned as an instance of `nx.Graph`.
3. `visualize_graph`: This function takes a `nx.Graph` object as input and creates an interactive HTML visualization of it using the `pyvis` library. It displays the nodes and edges of the graph, and allows users to interact with them by hovering over them to display information or clicking on them to navigate to the linked files. The resulting visualization is saved in a file named "graph.html" and can be opened in a web browser.
4. `main`: This function is the entry point for the script. It calls `build_graph` with the path to the Obsidian vault or Markdown directory as an argument, builds the graph using that path, and then passes it to `visualize_graph` to create the interactive visualization.

Overall, this code allows users to extract metadata from Markdown files, build a graph of their relationships, and create an interactive visualization of that graph using the `pyvis` library. It can be useful for exploring the relationships between different files in an Obsidian vault or Markdown directory.
