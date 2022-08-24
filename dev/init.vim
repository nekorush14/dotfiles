" general settings
set number
set hlsearch
set smartindent
set laststatus=2
set wildmenu
set ruler
set encoding=utf8
set clipboard+=unnamed

syntax enable

" plugin settings
call plug#begin('~/.config/nvim/plugged')

  Plug 'vim-airline/vim-airline'
  Plug 'vim-airline/vim-airline-themes'
  Plug 'tpope/vim-commentary'
  Plug 'neoclide/coc.nvim', {'branch': 'release'}
  Plug 'preservim/nerdtree'
  Plug 'ryanoasis/vim-devicons'
  Plug 'nvim-lua/plenary.nvim'
  Plug 'nvim-telescope/telescope.nvim', { 'branch': '0.1.x' }
  Plug 'airblade/vim-gitgutter'
  Plug 'dense-analysis/ale'

call plug#end()

" NERD Tree settings
nmap <silent><C-T> :NERDTreeToggle<CR>
let g:airline#extensions#tabline#enabled = 1
nmap <C-p> <Plug>AirlineSelectPrevTab
nmap <C-n> <Plug>AirlineSelectNextTab

" Airline settings
let g:airline_powerline_fonts = 1

" Telescope settings
nnoremap <C-p> <cmd>Telescope find_files<CR>
nnoremap <C-g> <cmd>Telescope live_grep<CR>

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

