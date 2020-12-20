#!/usr/bin/env python3
from i3ipc import Connection
from anytree import Node, RenderTree
from termcolor import colored

i3 = Connection()
root = i3.get_tree()

watch = True
only_content = True
tree_nodes = {}
for container in root.descendants():
    try:
        parent_node = tree_nodes[container.parent.id]
    except KeyError:
        parent_node = None
        pass

    if only_content:
        if container.type == 'dockarea' or container.parent.type == 'dockarea':
            continue

        if container.name == 'content' and container.parent.type == 'output':
            continue

        if container.type == 'workspace':
            parent_node = tree_nodes[container.parent.parent.id]

    tree_nodes[container.id] = Node(container.name, parent=parent_node, con=container)

for root_node in (n for n in tree_nodes.values() if n.parent is None):
    for pre, fill, node in RenderTree(root_node):
        color = None
        on_color = None
        style = None
        name = node.name if node.name is not None else '{NONE}'
        if node.con.type == 'workspace':
            name = f'[{name}] {{{node.con.layout}}}'
            color = 'cyan'
        elif node.con.type == 'output':
            color = 'blue'
            attr = ('bold',)

        if node.con.parent is not None:
            if node.con.parent.focus[0] == node.con.id:
                on_color = 'on_grey'

        if node.con.focused:
            on_color = 'on_magenta'

        if node.name is None and node.con.window is None:
            name = f'{{{node.con.layout}}}'

        line = f'{pre}{colored(name, color, on_color, style)}'
        print(line)

