#!/usr/bin/env python3
import sys
from i3ipc import Connection

output_left = 'DisplayPort-1'
output_center = 'DisplayPort-0'
output_right = 'HDMI-A-0'

i3 = Connection()
workspaces = i3.get_workspaces()

center_workspace = next(w for w in workspaces if w.output == output_center and w.visible)
if center_workspace.focused:
    sys.exit(1)

focused_workspace = next(w for w in workspaces if w.focused)
i3.command(f'move workspace to output {center_workspace.output}')
i3.command(f'workspace {center_workspace.name}')
i3.command(f'move workspace to output {focused_workspace.output}')
