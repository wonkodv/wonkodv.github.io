+++
title               = "Presenting in VIM"
description         = "If your presentation is code heavy, leverage syntax highlighting and writing comfort by staying in the editor"
date                = "2021-09-16"
taxonomies.category = ["Programming"]
taxonomies.tags     = ["Vim"]
extra.image         = "presenting_with_vim/presenting_with_vim.png"
+++

# Presenting in VIM

If you have to present something that contains mostly code and no graphics, you can stay in vim.
The benefit is that you can write your presentation like code. Also, often when
talking about code it is useful to show some real code, and that is easiest when
you are already in the right tool.

{{ image(path="presenting_with_vim.png", alt="Screenshot of a presentation using vim", title="Screenshot using neovim in terminator") }}


Write your "Slides" in Markdown, starting with a new Headline in line 50, 100,
150, ...

Some configuration is necessary to:

1. hide every visual distraction
1. Add a margin
1. increase your font size
1. enable smooth navigation.

Points one and two are simply some settings. Which exactly depends on you normal setup and plugins.
Enabling `cursorline` helps in online meetings if you would normally point at
things with your finger.

The font is either controlled by your terminal (`CTRL+SCROLL_WHEEL` in termnator)
or by a setting `set guifont=Consolas:18` in GVim/`neovim-qt`.
It should be large enough that bad projectors or vidoe codecs over low bandwith
online meetings still produce something readable.

Smooth navigation is achieved by a mapping that snaps lines 50, 100, 150, ... to the top of the screen.
I currently have the following `present.vim` which I source when necessary:


```vim
nnoremap <buffer> <F3> <CMD>exe 'normal '.(line(".")/50*50).'Gzt'<CR><C-L>
nmap <buffer> <F2> 50k<F3>
nmap <buffer> <F4> 50j<F3>
nnoremap <buffer> <F5> yi<:! firefox <C-R>"<CR><space>

highlight! EndOfBuffer ctermbg=bg ctermfg=bg guibg=bg guifg=bg

setlocal scrolloff=1
setlocal guifont=Consolas:h18
setlocal nonumber
setlocal cmdheight=1
setlocal statusline=
setlocal showtabline=0
setlocal signcolumn=yes:3
setlocal noshowmode
setlocal laststatus=0
setlocal noshowcmd
setlocal nocursorcolumn
setlocal nolist
setlocal colorcolumn=
setlocal noruler
```
I navigate through the "slides" using F2 for previous, F4 for next and F3 to
realign the slide to the top of the screen.
F5 marks a URL inside `<>` and opens it in `firefox`, so you can show a picture.

You can play around using [present.vim](/presenting_with_vim/present.vim) and [presentation.md](/presenting_with_vim/presentation.md)
