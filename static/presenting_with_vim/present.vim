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
