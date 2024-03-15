+++
title               = "Hitchhikers Guide to the Code"
description         = "I'd like open source projects to have a guide that points me to the highlights in the code"
date                = 2024-03-14
 updated            = 2024-03-16
taxonomies.category = ["Programming"]
taxonomies.tags     = []
+++

# Hitchhikers Guide to Code

In a software project, there are often large parts of the code, which are necessary for everything to
work, but not really exciting. And, there are a few central components where the essence of the
project happens, that are worth reading to understand the software.

I had the idea to give each project a file which gives readers a guided tour to these central pieces of
functionality.
And, being a fan of Douglas Adams' The Hitchhiker's Guide to the Galaxy,
I would of course call it `hitchhiker.md`

I suggest the following content:
*   version of the code that is documented in the file. This does not always have to be the
    newest version. The fundamental concepts don't change that often, and once you understood how the project works, it is easy
    to look for these components in the current code.
*   Link to the source at that version
*   A list of the central classes / functions. Each with:
    *   The component's name (including all namespaces / modules / ...)
    *   Where to find the component, preferably as link to the file and line
    *   One sentence what this component does
*   A link to important pieces of documentation

Just 20 lines would have helped me a lot in many projects. It might be best if they are written by
someone new to the project, because they know best what information would have helped them.

## Examples

*   [Bomber Hans2](https://github.com/wonkodv/bomberhans2/blob/main/hitchhiker.md)
*   [Req Trace](https://github.com/wonkodv/reqtrace/blob/master/hitchhiker.md)
