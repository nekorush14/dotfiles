" vimrc
"
" Vim configration file.
" Author: Mitsuhiro Komuro
"
" --Note--
" Plugin is starting line 124
" Plug plugin line 156
"

"""""""""""""""""
" Basic options "
"""""""""""""""""
" Set text encodeing
set encoding=utf-8
scriptencoding utf-8
set fileencoding=utf-8 " 保存時の文字コード
"set fileencodings=ucs-boms,utf-8,euc-jp,cp932 " 読み込み時の文字コードの自動判別. 左側が優先される
"set fileformats=unix,dos,mac " 改行コードの自動判別. 左側が優先される
"set ambiwidth=double "□や○文字が崩れる問題を解"

" タグファイルの指定(でもタグジャンプは使ったことがない)
set tags=~/.tags

" カーソルが何行目の何列目に置かれているかを表示する
set ruler
" コマンドラインに使われる画面上の行数
set cmdheight=1

" エディタウィンドウの末尾から2行目にステータスラインを常時表示させる
set laststatus=2

" ステータス行に表示させる情報の指定
set statusline=%<%f\%m%r%h%w%{'['.(&fenc!=''?&fenc:&enc).']['.&ff.']'}%=%l,%c%V%8P

" ウインドウのタイトルバーにファイルのパス情報等を表示する
set title

" コマンドラインモードで<Tab>キーによるファイル名補完を有効にする
set wildmenu

" 入力中のコマンドを表示する
set showcmd

" 小文字のみで検索したときに大文字小文字を無視する
set smartcase

" 検索結果をハイライト表示する
set hlsearch

" 暗い背景色に合わせた配色にする
" set background=dark

" タブ入力を複数の空白入力に置き換える
set expandtab

" 検索ワードの最初の文字を入力した時点で検索を開始する
set incsearch

" 保存されていないファイルがあるときでも別のファイルを開けるようにする
set hidden

" 不可視文字を表示する
set list

" タブと行の続きを可視化する
set listchars=tab:>\ ,extends:<

" 行番号を表示する
set number

" 対応する括弧やブレースを表示する
set showmatch

" 改行時に前の行のインデントを継続する
set autoindent

" 改行時に入力された行の末尾に合わせて次の行のインデントを増減する
set smartindent

" タブ文字の表示幅
set tabstop=4

" Vimが挿入するインデントの幅
set shiftwidth=4

" 行頭の余白内で Tab を打ち込むと、'shiftwidth' の数だけインデントする
set smarttab

" カーソルを行頭、行末で止まらないようにする
set whichwrap=b,s,h,l,<,>,[,]

" 構文毎に文字色を変化させる
syntax on

" 行番号の色
highlight LineNr ctermfg=yellow

" カラースキーマの指定
"colorscheme molokai_dark

" ハイライトON
set hlsearch

" Jump settings
"set showmatch " 括弧の対応関係を一瞬表示する
"source $VIMRUNTIME/macros/matchit.vim " Vimの「%」を拡張する

" setting History size
set history=5000

" paste settings
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

""""""""""""""""""""
" Disabled options "
""""""""""""""""""""

" スワップファイルは使わない
" set noswapfile

" ステータス行に現在のgitブランチを表示する
" set statusline+=%{fugitive#statusline()}

" バックアップディレクトリの指定
" set backupdir=$HOME/.vimbackup

" 閉じ括弧の自動追加
"imap { {}<LEFT>
"imap [ []<LEFT>
"imap ( ()<LEFT>

"""""""""""""""
" Key binding "
"""""""""""""""

" Esc Esc でハイライトOFF
nnoremap <Esc><Esc> :<C-u>set nohlsearch<Return>

" " 「/」「?」「*」「#」が押されたらハイライトをONにしてから「/」「?」「*」「#」
nnoremap / :<C-u>set hlsearch<Return>/
nnoremap ? :<C-u>set hlsearch<Return>?
nnoremap * :<C-u>set hlsearch<Return>*
nnoremap # :<C-u>set hlsearch<Return>#

""""""""""""""""""
" Plugin manager "
""""""""""""""""""
if has('vim_starting')
    set rtp+=~/.vim/plugged/vim-plug
    if !isdirectory(expand('~/.vim/plugged/vim-plug'))
        echo 'install vim-plug...'
        call system('mkdir -p ~/.vim/plugged/vim-plug')
        call system('git clone https://github.com/junegunn/vim-plug.git ~/.vim/plugged/vim-plug/autoload')
    end
endif

call plug#begin('~/.vim/plugged')
    Plug 'junegunn/vim-plug',
        \ {'dir': '~/.vim/plugged/vim-plug/autoload'}

    " Vundle/NeoBundle と同じように
    Plug 'junegunn/seoul256.vim'

    " コマンド実行時に読み込む
    Plug 'scrooloose/nerdtree', { 'on':  ['NERDTreeToggle'] }

    " 指定したファイルタイプを開いたときに読み込む
    Plug 'tpope/vim-fireplace', { 'for': ['clojure'] }

    " X | Y の時, X をインストールした後に Y をインストール
    Plug 'SirVer/ultisnips' | Plug 'honza/vim-snippets'

    " Status bar
    Plug 'itchyny/lightline.vim'

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

    " Color theme
    Plug 'tomasr/molokai'

    "
    Plug 'bronson/vim-trailing-whitespace'
call plug#end()

""""""""""""""""""
" Plugin setings "
""""""""""""""""""

"============
"Colour theme
"============
"let g:molokai_original = 1
let g:rehash256 = 1
let g:onedark_termcolors=256

"===============
"molokaiの設定
"===============
"colorscheme molokai " カラースキームにmolokaiを設定する

set t_Co=256 " iTerm2など既に256色環境なら無くても良い
syntax enable " 構文に色を付ける

"==============
"Help setings
"==============
nmap <F6> :h my-markdown-cheat-sheet.txt<CR>
nmap <F7> :h my-help-vim.txt<CR>

"=====================
"NERDTREE change icons
"=====================
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

"=================
"Indent visualiser
"=================
set list
set listchars=tab:\|\ 
hi SpecialKey guifg=#333333
let g:indentLine_color_term = 239
let g:indentLine_char = '┆'

"================
"Markdown preview
"================
let g:previm_open_cmd = 'open -a Firefox'
nmap <F5> :PrevimOpen<CR>

"===============
"neocomplete.vim
"===============
" Disable AutoComplPop.
let g:acp_enableAtStartup = 0
" Use neocomplcache.
let g:neocomplcache_enable_at_startup = 1
" Use smartcase.
let g:neocomplcache_enable_smart_case = 1
" Set minimum syntax keyword length.
let g:neocomplcache_min_syntax_length = 3
let g:neocomplcache_lock_buffer_name_pattern = '\*ku\*'

" Define dictionary.
let g:neocomplcache_dictionary_filetype_lists = {
            \ 'default' : ''
            \ }

" Plugin key-mappings.
inoremap <expr><C-g>     neocomplcache#undo_completion()
inoremap <expr><C-l>     neocomplcache#complete_common_string()

" Recommended key-mappings.
" " <CR>: close popup and save indent.
inoremap <silent> <CR> <C-r>=<SID>my_cr_function()<CR>
function! s:my_cr_function()
    return neocomplcache#smart_close_popup() . "\<CR>"
endfunction

" <TAB>: completion.
inoremap <expr><TAB>  pumvisible() ? "\<C-n>" : "\<TAB>"
" <C-h>, <BS>: close popup and delete backword char.
inoremap <expr><C-h> neocomplcache#smart_close_popup()."\<C-h>"
inoremap <expr><BS> neocomplcache#smart_close_popup()."\<C-h>"
inoremap <expr><C-y>  neocomplcache#close_popup()
inoremap <expr><C-r>  neocomplcache#cancel_popup()

"====================
"NERDTree Key binding
"====================
nnoremap <silent><C-e> :NERDTreeToggle<CR>

"=================
"lightline setings
"=================
" \ 'colorscheme': 'landscape',
let g:lightline = {
      \ 'mode_map': { 'c': 'NORMAL' },
      \ 'active': {
      \   'left': [ [ 'mode', 'paste' ], [ 'fugitive', 'filename' ] ]
      \ },
      \ 'component_function': {
      \   'modified': 'LightlineModified',
      \   'readonly': 'LightlineReadonly',
      \   'fugitive': 'LightlineFugitive',
      \   'filename': 'LightlineFilename',
      \   'fileformat': 'LightlineFileformat',
      \   'filetype': 'LightlineFiletype',
      \   'fileencoding': 'LightlineFileencoding',
      \   'mode': 'LightlineMode',
      \ },
      \ 'separator': { 'left': '⮀', 'right': '⮂' },
      \ 'subseparator': { 'left': '⮁', 'right': '⮃' }
      \}

function! LightlineModified()
    return &ft =~ 'help\|vimfiler\|gundo' ? '' : &modified ? '+' : &modifiable ? '' : '-'
endfunction

function! LightlineReadonly()
    return &ft !~? 'help\|vimfiler\|gundo' && &readonly ? '⭤' : ''
endfunction

function! LightlineFilename()
    return ('' != LightlineReadonly() ? LightlineReadonly() . ' ' : '') .
                \ (&ft == 'vimfiler' ? vimfiler#get_status_string() :
                \  &ft == 'unite' ? unite#get_status_string() :
                \  &ft == 'vimshell' ? vimshell#get_status_string() :
                \ '' != expand('%:t') ? expand('%:t') : '[No Name]') .
                \ ('' != LightlineModified() ? ' ' . LightlineModified() : '')
endfunction

function! LightlineFugitive()
    if &ft !~? 'vimfiler\|gundo' && exists("*fugitive#head")
        let branch = fugitive#head()
        return branch !=# '' ? '⭠ '.branch : ''
    endif
    return ''
endfunction

function! LightlineFileformat()
    return winwidth(0) > 70 ? &fileformat : ''
endfunction

function! LightlineFiletype()
    return winwidth(0) > 70 ? (&filetype !=# '' ? &filetype : 'no ft') : ''
endfunction

function! LightlineFileencoding()
    return winwidth(0) > 70 ? (&fenc !=# '' ? &fenc : &enc) : ''
endfunction

function! LightlineMode()
    return winwidth(0) > 60 ? lightline#mode() : ''
endfunction
