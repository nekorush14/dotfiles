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
" General configs: L17
" Key configs: L105
" Plugin maneger configs: L124
" Plugin configs: L224
"
""""""""""""""""""

""""""""""
"" General configs
""""""""""

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

    " Load when executeing the command
    Plug 'scrooloose/nerdtree', { 'on':  ['NERDTreeToggle'] }

    " Load when opening the specific file type
    Plug 'tpope/vim-fireplace', { 'for': ['clojure'] }

    " Snipets
    Plug 'SirVer/ultisnips' | Plug 'honza/vim-snippets'

    " Status bar
    " Plug 'itchyny/lightline.vim'

    " Status bar for power-line like theme
    Plug 'vim-airline/vim-airline'

    " vim-airline theme
    Plug 'vim-airline/vim-airline-themes'

    " File tree
    Plug 'scrooloose/nerdtree'

    " Onedoark Colour scheam
    Plug 'joshdick/onedark.vim'

    " Ruby autocompleat
    Plug 'osyo-manga/vim-monster'

    " Ruby autocompleat2
    Plug 'tpope/vim-endwise'

    " Normal autocompleat
    Plug 'Shougo/neocomplcache.vim'

    " Help Japanease
    Plug 'vim-jp/vimdoc-ja'

    " Indent visualiser
    Plug 'Yggdroot/IndentLine'

    " Python Autocompleat
    Plug 'davidhalter/jedi-vim'

    " Markdown previewer
    Plug 'kannokanno/previm'

    " NERDTREE change icons
    Plug 'Xuyuanp/nerdtree-git-plugin'

    " Auto close
    Plug 'Townk/vim-autoclose'

    " Git plugin for vim
    Plug 'tpope/vim-fugitive'

    " Color theme [Molokai]
    Plug 'tomasr/molokai'

    " Color theme [Dracula]
    Plug 'dracula/vim'

    " Remove wihte space
    Plug 'bronson/vim-trailing-whitespace'

    " Python vertual enviroment on vim
    Plug 'plytophogy/vim-virtualenv'

    " Running linter
    Plug 'w0rp/ale'

    " Auto indent for python pep8
    Plug 'Vimjas/vim-python-pep8-indent'

    " Vimshell
    Plug 'Shougo/vimshell.vim'
    Plug 'Shougo/vimproc.vim', {'do' : 'make'}
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
let g:ale_echo_msg_format = '[%linter%] %s [%severity%]'
let g:ale_sign_column_always = 1
let g:ale_lint_on_enter = 1
let g:ale_lint_on_save = 1
let g:ale_lint_on_text_changed = 'never'
let g:ale_set_loclist = 0
let g:ale_set_quickfix = 0
let g:ale_open_list = 0
let g:ale_keep_list_window_open = 0
let g:ale_linters = {
\   'python': ['flake8'],
\}

" Jedi-vim
autocmd FileType python setlocal completeopt-=preview

" Colour theme with plugins
let g:rehash256 = 1
let g:onedark_termcolors=256
colorscheme onedark
color dracula
" set t_Co=256

" Helper
" nmap <F6> :h my-markdown-cheat-sheet.txt<CR>
" nmap <F7> :h my-help-vim.txt<CR>

" Indent visualiser
" set listchars=tab:\|\
hi SpecialKey guifg=#333333
let g:indentLine_color_term = 239
let g:indentLine_char = '┆'

" Markdown preview
" let g:previm_open_cmd = 'open -a Chrome'
" nmap <F5> :PrevimOpen<CR>

" neocomplete
let g:acp_enableAtStartup = 0
let g:neocomplcache_enable_at_startup = 1
let g:neocomplcache_enable_smart_case = 1
let g:neocomplcache_min_syntax_length = 3
let g:neocomplcache_lock_buffer_name_pattern = '\*ku\*'
let g:neocomplcache_dictionary_filetype_lists = {
            \ 'default' : ''
            \ }
inoremap <expr><C-g> neocomplcache#undo_completion()
inoremap <expr><C-l> neocomplcache#complete_common_string()
inoremap <silent> <CR> <C-r>=<SID>my_cr_function()<CR>
function! s:my_cr_function()
    return neocomplcache#smart_close_popup()."\<CR>"
endfunction
inoremap <expr><TAB> pumvisible()?"\<C-n>":"\<TAB>"
inoremap <expr><C-h> neocomplcache#smart_close_popup()."\<C-h>"
inoremap <expr><BS> neocomplcache#smart_close_popup()."\<C-h>"
inoremap <expr><C-y> neocomplcache#close_popup()
inoremap <expr><C-r> neocomplcache#cancel_popup()

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
nnoremap <silent><C-e> :NERDTreeToggle<CR>
