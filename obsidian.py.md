# Documentation for obsidian.py

#py
##tags ##links ##graph ##markdown ##file ##node ##edge ##visualize ##extract


Here is a detailed Markdown documentation for the code:

### Importing Modules

The following modules are imported at the beginning of the code:

* `os`: Provides functions for interacting with the operating system, such as reading and writing files.
* `re`: A regular expression module that provides functions for matching patterns in strings.
* `networkx`: A Python library for creating and manipulating graphs.
* `pyvis.network`: A Python library for creating interactive HTML visualizations of graphs.

### Defining Variables

The following variables are defined at the beginning of the code:

* `VAULT_PATH`: The path to your Obsidian vault or Markdown directory. This is used in the `build_graph` function to scan all `.md` files in the vault.
* `file_path`: A variable that stores the file path for the current .md file being processed. This is used in the `extract_metadata` function to read the contents of the file.
* `tags`: A set that will store the #tags extracted from the Markdown file.
* `links`: A set that will store the wiki-style links extracted from the Markdown file.
* `graph`: An instance of a `nx.Graph` object that will be used to build and visualize the graph of relationships between Markdown files.
* `net`: An instance of a `pyvis.network.Network` object that will be used to create an interactive HTML visualization of the graph.

### Extracting Metadata

The `extract_metadata` function is defined as follows:
```python
def extract_metadata(file_path):
    """Extracts tags (#tag) and wiki-style links ([[Link]]) from a Markdown file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    tags = set(re.findall(r'#(\w+)', content))  # Extract #tags
    links = set(re.findall(r'\[\[([^\]]+)\]\]', content))  # Extract [[Links]]
    
    return tags, links
```
This function takes a file path as an argument and reads the contents of the Markdown file using the `open` function with encoding `'utf-8'`. It then uses regular expressions to extract all #tags and wiki-style links (represented by [[Links]]) from the contents. The extracted tags and links are returned as a tuple.

### Building the Graph

The `build_graph` function is defined as follows:
```python
def build_graph(vault_path):
    """Scans all .md files in a directory and builds a graph of their relationships."""
    graph = nx.Graph()
    files = {}
    
    # Scan all .md files
    for file in os.listdir(vault_path):
        if file.endswith(".md"):
            file_path = os.path.join(vault_path, file)
            tags, links = extract_metadata(file_path)
            
            # Add file node
            graph.add_node(file, label=file, color="lightblue")
            files[file] = {"tags": tags, "links": links}
            
            # Add tag relations
            for tag in tags:
                tag_node = f"#{tag}"
                graph.add_node(tag_node, label=tag, color="green")  # Tag nodes in green
                graph.add_edge(file, tag_node)  # Connect file to tag
    
    # Add file-to-file links
    for file, data in files.items():
        for link in data["links"]:
            if f"{link}.md" in files:  # Ensure the linked file exists
                graph.add_edge(file, f"{link}.md", color="gray")
    
    return graph
```
This function takes a vault path as an argument and creates a new `nx.Graph` object to build and store the relationships between Markdown files. It then scans all `.md` files in the vault directory using the `os.listdir` function, and for each file, it extracts its #tags and wiki-style links using the `extract_metadata` function. For each file, it adds a node to the graph with the file name as the label, and sets its color to "lightblue". It also adds nodes for each tag extracted from the file, and connects the file to those tags using edges.

After all files have been processed, it checks for file-to-file links (i.e., links that point to other Markdown files) and adds them to the graph if they exist. The final graph is returned.

### Visualizing the Graph

The `visualize_graph` function is defined as follows:
```python
def visualize_graph(graph):
    """Creates an interactive HTML visualization of the graph."""
    net = Network(notebook=False, cdn_resources="remote")
    net.from_nx(graph)
    
    # Save and open in browser
    net.write_html("graph.html")
```
This function takes a `graph` object as an argument and creates an instance of the `Network` class from the `pyvis.network` module using the `Notebook` parameter set to `False`. It then uses the `from_nx` method to create an HTML visualization of the graph using the `Network` instance, and saves the output as an HTML file named "graph.html". Finally, it opens the saved HTML file in a web browser using the `write_html` method.
