import os
import re
import networkx as nx
from pyvis.network import Network

# Path to your Obsidian vault or Markdown directory
VAULT_PATH = "C:/Users/luuk/Documents/Obsidian Vault/eigen projecten/python/functional/read gcode - AI Processed"

def extract_metadata(file_path):
    """Extracts tags (#tag) and wiki-style links ([[Link]]) from a Markdown file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    tags = set(re.findall(r'#(\w+)', content))  # Extract #tags
    links = set(re.findall(r'\[\[([^\]]+)\]\]', content))  # Extract [[Links]]

    return tags, links

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

def visualize_graph(graph):
    """Creates an interactive HTML visualization of the graph."""
    net = Network(notebook=False, cdn_resources="remote")
    net.from_nx(graph)

    # Save and open in browser
    net.write_html("graph.html")

if __name__ == "__main__":
    graph = build_graph(VAULT_PATH)
    visualize_graph(graph)
