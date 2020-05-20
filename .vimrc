""""""""""""""""""""
"        _
" __   _(_)_ __ ___  _ __ ___
" \ \ / / | '_ ` _ \| '__/ __|
"  \ V /| | | | | | | | | (__
" (_)_/ |_|_| |_| |_|_|  \___|
"
"
" Vim configration file
" Author: Mitsuhiro Komuro
"
" Version: 2.3.4.b
" General configs: L24
" Key configs: L105
" Plugin maneger configs: L164
" Plugin configs: L236
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

""""""""""""""""""

""""""""""
"" Plugin maneger configs
""""""""""

" Install Plugin manager when running the vim at first time
if has('vim_starting')
    set rtp+=~/.vim/plugged/vim-plug
    if !isdirectory(expand('~/.vim/plugged/vim-plug'))
        echo 'install vim-plug...'
        call system('mkdir -p ~/.vim/plugged/vim-plug')
        call system('git clone https://github.com/junegunn/vim-plug.git ~/.vim/plugged/vim-plug/autoload')
    end
endif

" Plugins
call plug#begin('~/.vim/plugged')
    Plug 'junegunn/vim-plug',
        \ {'dir': '~/.vim/plugged/vim-plug/autoload'}

    " Colour schme
    Plug 'junegunn/seoul256.vim'
    " Color theme [Dracula]
    Plug 'dracula/vim'

    " Load when executeing the command
    " File tree for Vim
    Plug 'scrooloose/nerdtree', { 'on':  ['NERDTreeToggle'] }
    Plug 'jistr/vim-nerdtree-tabs'
    Plug 'Xuyuanp/nerdtree-git-plugin'
    Plug 'tiagofumo/vim-nerdtree-syntax-highlight'
    Plug 'ctrlpvim/ctrlp.vim'
    Plug 'scrooloose/nerdcommenter'
    Plug 'ryanoasis/vim-devicons'

    " Load when opening the specific file type
    Plug 'tpope/vim-fireplace', { 'for': ['clojure'] }

    " Snipets
    Plug 'SirVer/ultisnips' | Plug 'honza/vim-snippets'

    " Status bar for power-line like theme
    Plug 'vim-airline/vim-airline'
    Plug 'vim-airline/vim-airline-themes'

    " Help Japanease
    Plug 'vim-jp/vimdoc-ja'

    " Indent visualiser
    Plug 'Yggdroot/IndentLine'

    " Auto close
    Plug 'Townk/vim-autoclose'

    " Auto closing block such as function
    Plug 'tpope/vim-endwise'

    " Git plugin for vim
    Plug 'tpope/vim-fugitive'
    Plug 'airblade/vim-gitgutter'

    " Remove wihte space
    Plug 'bronson/vim-trailing-whitespace'

    " Python vertual enviroment on vim
    Plug 'plytophogy/vim-virtualenv'

    " Running linter
    Plug 'w0rp/ale'

    " Searching plugins
    Plug 'junegunn/fzf', { 'do': {-> fzf#install()} }
    Plug 'junegunn/fzf.vim'

    " Markdown Preview from vim
    Plug 'tyru/open-browser.vim'
    Plug 'kannokanno/previm'

    " Language Server Protocol
    Plug 'neoclide/coc.nvim', {'branch': 'release'}

    " vim window resizer
    Plug 'simeji/winresizer'

    " Shell for vim
    Plug 'kassio/neoterm'

call plug#end()

""""""""""""""""""

""""""""""
"" Plugin configs
""""""""""

" vim-airline
let g:airline_powerline_fonts = 1
let g:airline_theme='onedark'
set laststatus=2
let g:airline#extensions#tabline#enabled = 1
let g:airline#extensions#tabline#buffer_idx_mode = 1
let g:airline#extensions#tabline#formatter ='unique_tail_improved'
let g:airline#extensions#coc#enabled = 1
let airline#extensions#coc#error_symbol = 'E:'
let airline#extensions#coc#warning_symbol = 'W:'
let airline#extensions#coc#stl_format_err = '%E{[%e(#%fe)]}'
let airline#extensions#coc#stl_format_warn = '%W{[%w(#%fw)]}'
if !exists('g:airline_symbols')
    let g:airline_symbols = {}
endif
let g:airline_symbols.paste = 'ρ'
let g:airline_symbols.spell = 'Ꞩ'
let g:airline_symbols.notexists = '∄'
let g:airline_symbols.whitespace = 'Ξ'
let g:airline#extensions#virtualenv#enabled = 1
let g:airline#extensions#ale#enabled = 1
if !exists('g:airline_powerline_fonts')
    let g:airline#extensions#tabline#left_sep = ' '
    let g:airline#extensions#tabline#left_alt_sep = '|'
    let g:airline_left_sep          = '▶'
    let g:airline_left_alt_sep      = '»'
    let g:airline_right_sep         = '◀'
    let g:airline_right_alt_sep     = '«'
    let g:airline#extensions#branch#prefix     = '⤴' "➔, ➥, ⎇
    let g:airline#extensions#readonly#symbol   = '⊘'
    let g:airline#extensions#linecolumn#prefix = '¶'
    let g:airline#extensions#paste#symbol      = 'ρ'
    let g:airline_symbols.linenr    = '␊'
    let g:airline_symbols.crypt = '🔒'
    let g:airline_symbols.branch = '⭠'
    let g:airline_symbols.paste     = 'ρ'
    let g:airline_symbols.paste     = 'Þ'
    let g:airline_symbols.paste     = '∥'
    let g:airline_symbols.whitespace = 'Ξ'
else
    let g:airline#extensions#tabline#left_sep = ''
    let g:airline#extensions#tabline#left_alt_sep = ''
    let g:airline_left_sep = ''
    let g:airline_left_alt_sep = ''
    let g:airline_right_sep = ''
    let g:airline_right_alt_sep = ''
    let g:airline_symbols.branch = ''
    let g:airline_symbols.readonly = ''
    let g:airline_symbols.linenr = ''
endif

" Ale settings
let g:ale_sign_error = '⨉'
let g:ale_sign_warning = '⚠'
let g:ale_echo_msg_error_str = '⨉'
let g:ale_echo_msg_warning_str = '⚠'
let g:ale_echo_msg_format = '[%linter%] %s (%severity%)'
let g:ale_statusline_format = ['⨉ %d', '⚠ %d', '']
let g:ale_open_list = 1
let g:ale_javascript_prettier_use_local_config=1
let g:ale_sign_column_always = 1
let g:ale_lint_on_enter = 1
let g:ale_lint_on_save = 1
let g:ale_lint_on_text_changed = 'never'
let g:ale_set_loclist = 0
let g:ale_set_quickfix = 0
let g:ale_open_list = 0
let g:ale_keep_list_window_open = 0
let g:ale_linters = {
    \ 'python': ['flake8'],
    \ 'css': ['stylelint', 'prettier'],
    \ 'dockerfile': ['hadolint'],
    \ 'erb': ['erb'],
    \ 'html': ['HTMLHint'],
    \ 'haml': ['haml-lint'],
    \ 'javascript': ['eslint'],
    \ 'json': ['jq'],
    \ 'ruby': ['rubocop', 'solargraph'],
    \ 'typescript': ['eslint'],
    \ 'vim': ['vint'],
    \ 'yaml': ['yamllint'],
\}

"vim help language
set helplang=ja

" Colour theme with plugins
let g:rehash256 = 1
color dracula

" Markdown Preview
au BufRead,BufNewFile *.md set filetype=markdown
let g:previm_open_cmd = 'open -a Google\ Chrome'

" Indent visualiser
hi SpecialKey guifg=#333333
let g:indentLine_color_term = 239
let g:indentLine_char = '┆'

" NERDTREE icons
let g:NERDTreeIndicatorMapCustom = {
    \ "Modified"  : "✹",
    \ "Staged"    : "✚",
    \ "Untracked" : "✭",
    \ "Renamed"   : "➜",
    \ "Unmerged"  : "═",
    \ "Deleted"   : "✖",
    \ "Dirty"     : "✗",
    \ "Clean"     : "✔︎",
    \ "Unknown"   : "?"
    \ }
nnoremap <silent><C-T> :NERDTreeToggle<CR>
" nnoremap <silent><C-l> <plug>NERDTreeTabsToggle<CR>
vmap ++ <plug>NERDCommenterToggle
nmap ++ <plug>NERDCommenterToggle

" Auto pen settings For NERDTree
autocmd vimenter * NERDTree | wincmd p
autocmd StdinReadPre * let s:std_in=1
autocmd VimEnter * if argc() == 0 && !exists("s:std_in") | NERDTree | endif
autocmd VimEnter * if argc() == 1 && isdirectory(argv()[0]) && !exists("s:std_in") | exe 'NERDTree' argv()[0] | wincmd p | ene | endif

" sync open file with NERDTree
" Check if NERDTree is open or active
" function! IsNERDTreeOpen()
"       return exists("t:NERDTreeBufName") && (bufwinnr(t:NERDTreeBufName) != -1)
" endfunction

" Call NERDTreeFind iff NERDTree is active, current window contains a modifiable
" file, and we're not in vimdiff
" function! SyncTree()
"     if &modifiable && IsNERDTreeOpen() && strlen(expand('%')) > 0 && !&diff
"         NERDTreeFind
"         wincmd p
"     endif
" endfunction

" Highlight currently open buffer in NERDTree
" autocmd BufEnter * call SyncTree()

" ctrlp
let g:ctrlp_user_command = ['.git/', 'git --git-dir=%s/.git ls-files -oc --exclude-standard']

" git gutter configs
set signcolumn=yes
let g:gitgutter_async = 1
let g:gitgutter_sign_modified = 'rw'
highlight GitGutterAdd ctermfg=green
highlight GitGutterChange ctermfg=yellow
highlight GitGutterDelete ctermfg=red
highlight GitGutterChangeDelete ctermfg=yellow

" neoterm configs
function! NTermHolizontalSplit()
	let l:tmp = g:neoterm_default_mod
	let g:neoterm_default_mod = "aboveleft"
	Tnew
	let g:neoterm_default_mod = l:tmp
endfunction

function! NTermVerticalSplit()
	let l:tmp = g:neoterm_default_mod
	let g:neoterm_default_mod = "vertical"
	Tnew
	let g:neoterm_default_mod = l:tmp
endfunction

nnoremap <silent> <c-s><c-s> :Ttoggle<CR>
tnoremap <silent> <c-s><c-s> <C-\><C-n>:Ttoggle<CR>
tnoremap <silent> <C-w> <C-\><C-n><C-w>
nnoremap <c-s><c-h> :call NTermHolizontalSplit()<CR>
nnoremap <c-s><c-v> :call NTermVerticalSplit()<CR>

" fzf settings
nnoremap <C-g> :Rg<Space>
nnoremap <C-h> :History<CR>

let g:fzf_action = {
  \ 'ctrl-o': 'tab split'
  \ }

command! -bang -nargs=* Rg
  \ call fzf#vim#grep(
  \   'rg --column --line-number --hidden --ignore-case --no-heading --color=always '.shellescape(<q-args>), 1,
  \   <bang>0 ? fzf#vim#with_preview({'options': '--delimiter : --nth 4..'}, 'up:60%')
  \           : fzf#vim#with_preview({'options': '--delimiter : --nth 4..'}, 'right:50%:hidden', '?'),
  \   <bang>0)

" vim dev icons
let g:webdevicons_conceal_nerdtree_brackets = 1
let g:WebDevIconsNerdTreeBeforeGlyphPadding = ""
let g:WebDevIconsUnicodeDecorateFolderNodes = v:true
" after a re-source, fix syntax matching issues (concealing brackets):
if exists('g:loaded_webdevicons')
  call webdevicons#refresh()
endif
set guifont=RictyDiscordForPowerline\ Nerd\ Font:h14

" coc.nvim settings
highlight CocErrorSign ctermfg=15 ctermbg=196
highlight CocWarningSign ctermfg=0 ctermbg=172

" coc.nvim keymap
inoremap <silent><expr> <TAB>
      \ pumvisible() ? "\<C-n>" :
      \ <SID>check_back_space() ? "\<TAB>" :
      \ coc#refresh()
inoremap <expr><S-TAB> pumvisible() ? "\<C-p>" : "\<C-h>"

function! s:check_back_space() abort
    let col = col('.') - 1
    return !col || getline('.')[col - 1]  =~# '\s'
endfunction

nmap <silent> gd <Plug>(coc-definition)
nmap <silent> gy <Plug>(coc-type-definition)
nmap <silent> gi <Plug>(coc-implementation)
nmap <silent> gr <Plug>(coc-references)
nnoremap <silent> K :call <SID>show_documentation()<CR>
nmap <silent> <space>fmt <Plug>(coc-format)
nmap <F2> <Plug>(coc-rename)

set statusline^=%{coc#status()}%{get(b:,'coc_current_function','')}

function! s:show_documentation()
    if (index(['vim','help'], &filetype) >= 0)
        execute 'h '.expand('<cword>')
    else
        call CocAction('doHover')
    endif
endfunction

function FindCursorPopUp()
  let radius = get(a:000, 0, 2)
  let srow = screenrow()
  let scol = screencol()
  " it's necessary to test entire rect, as some popup might be quite small
  for r in range(srow - radius, srow + radius)
    for c in range(scol - radius, scol + radius)
      let winid = popup_locate(r, c)
      if winid != 0
        return winid
      endif
    endfor
  endfor
  return 0
endfunction

function ScrollPopUp(down)
  let winid = FindCursorPopUp()
  if winid == 0
    return 0
  endif

  let pp = popup_getpos(winid)
  call popup_setoptions( winid,
    \ {'firstline' : pp.firstline + ( a:down ? 1 : -1 ) } )
  return 1
endfunction

nnoremap <expr> <c-d> ScrollPopUp(1) ? '<esc>' : '<c-d>'
nnoremap <expr> <c-u> ScrollPopUp(0) ? '<esc>' : '<c-u>'
