# Documentation for Hu-sidian v2.py

#py
##graph ##node ##tag #link #search #theme #structure #vault #relation #rebuild


This is a complete and functional implementation of the Obsidian Graph Viewer. It includes a few key features to make it easy to use and understand:

1. Structure nodes: These are the basic building blocks of the graph, representing individual notes or files in your vault. Each structure node has a unique label that corresponds to the filepath of the underlying Markdown file.
2. Tag nodes: These represent tags used in your notes, such as "#tag_urgent" or "#tag_todo". These tags are connected to their corresponding structures through an edge.
3. File-to-file links: These represent relationships between individual files in your vault. For example, if you have two notes, "A.md" and "B.md", and you want to show that they refer to each other, you can add an edge between them.
4. Search bar: This allows you to search for specific notes or tags in the graph. When you enter a query in the search bar, only nodes and edges corresponding to your search query will be displayed in the viewer.
5. Generate Graph button: This will rebuild the entire graph based on your current vault structure. The new graph will include all of the structure nodes, tag nodes, and file-to-file links that you have defined in your Markdown files.
6. Dark theme: This sets the style of the viewer to a dark theme. You can modify this by changing the value of `obsidian_dark_theme` in the source code.

I hope this helps! Let me know if you have any questions or need further assistance.
