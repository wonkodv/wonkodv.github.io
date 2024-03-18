+++
title               = "Modern Terminal"
description         = "I found a new Terminal Emulator and love it"
date                = 2022-04-20
taxonomies.category = ["Unix"]
taxonomies.tags     = ["bash"]
+++

# A Modern Terminal

Some years ago I saw a talk by Gary Bernhardt.
The tile was "A Whole new World" and he showed this great new ecosystem of terminal emulator and editor that drew class diagrams onto the terminal.
Turns out he just photoshopped those screenshots and none of this worked.

When I stumbled upon [Kitty](https://sw.kovidgoyal.net/kitty/), it seemed this whole new world was finally coming.

Some of the features:
*   Actually good font settings
*   Graphics on the terminal, by sending escape codes that contain the filename or the image data (bmp or png base64-encoded)
*   Hyperlinks and configurable handlers (ever clicked on a filename that `ls` printed?)
*   Integration with the shell so the terminal can associate commands with their output
    *   Shortcut to scroll to previous prompts (Ctrl+Shift+Z)
    *   Shortcut to open last output in a pager (Ctrl+Shift+H)
    *   or click to open any output in a pager (Ctrl+Shift+Mouse3)

I'm so happy.
