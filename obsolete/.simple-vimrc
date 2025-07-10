""""""""""""""""""""
"        _                 _                 _
"    ___(_)_ __ ___  _ __ | | ___     __   _(_)_ __ ___  _ __ ___
"   / __| | '_ ` _ \| '_ \| |/ _ \____\ \ / / | '_ ` _ \| '__/ __|
"  _\__ \ | | | | | | |_) | |  __/_____\ V /| | | | | | | | | (__
" (_)___/_|_| |_| |_| .__/|_|\___|      \_/ |_|_| |_| |_|_|  \___|
"                     |_|
"
"
" Vim configration file
" Author: Mitsuhiro Komuro
"
" Version: 2.3.5
" General configs: L24
" Key configs: L105
"
""""""""""""""""""

""""""""""
"" General configs
""""""""""

" Shell
set shell=/usr/local/bin/bash

" Text encoding
set encoding=utf-8
set fileencoding=utf-8
scriptencoding utf-8

" Specify the tag file
set tags=~/.tags

" Ruler
set ruler

" The number of lines used by commandline
set cmdheight=1

" Position of status line
set laststatus=2

" Display the filepath
set title

" File name completion using <Tab> key
set wildmenu

" Display the inputed command
set showcmd

" Ignore upper/lower case when search with lower case
set smartcase

" Display the highlight of search result
set hlsearch

" Replace tab input with multiple blank inputs
set expandtab

" Start the search when type the first character of search word
set incsearch

" Hide buffers when they are abandoned
set hidden

" Line feed code
set nolist

" Display the row number
set number
highlight LineNr ctermfg=yellow

" Highlight the corresponding brackets
set showmatch

" Cutoff the beap sound
set belloff=all

" Yank content copy to clipboard
set clipboard+=unnamed

" Indantation
set autoindent
set smartindent
set tabstop=4
set shiftwidth=4

" Don't stop a cursor at the end of row
set whichwrap=b,s,h,l,<,>,[,]

" Display the syntax highlight
syntax on

" History size
set history=5000

" Pasteing settings
if &term =~ "xterm"
    let &t_SI .= "\e[?2004h"
    let &t_EI .= "\e[?2004l"
    let &pastetoggle = "\e[201~"

    function XTermPasteBegin(ret)
        set paste
        return a:ret
    endfunction

    inoremap <special> <expr> <Esc>[200~ XTermPasteBegin("")
endif

""""""""""""""""""

""""""""""
"" Key configs
""""""""""

" Highlight off with double key input of <ESC>
nnoremap <Esc><Esc> :<C-u>set nohlsearch<Return>

" Highlighting before action [/], [?], [*], [#]
nnoremap / :<C-u>set hlsearch<Return>/
nnoremap ? :<C-u>set hlsearch<Return>?
nnoremap * :<C-u>set hlsearch<Return>*
nnoremap # :<C-u>set hlsearch<Return>#

" Backspace
set backspace=indent,eol,start
set backspace=2

" Display split
nnoremap sj <C-w>j
nnoremap sk <C-w>k
nnoremap sl <C-w>l
nnoremap sh <C-w>h
nnoremap ss :<C-u>sp<CR><C-w>j
nnoremap sv :<C-u>vs<CR><C-w>l

" Next buffer tab
nnoremap <silent> 9 :bprev<CR>

" Previous buffer tab
nnoremap <silent> 0 :bnext<CR>

" Delete current buffer tab
nnoremap bd :bd<CR>

