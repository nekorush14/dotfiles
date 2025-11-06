if vim.g.vscode then
	-- VSCode folding commands
	vim.keymap.set("n", "zc", "<Cmd>call VSCodeNotify('editor.fold')<CR>")
	vim.keymap.set("n", "zo", "<Cmd>call VSCodeNotify('editor.unfold')<CR>")
	vim.keymap.set("n", "za", "<Cmd>call VSCodeNotify('editor.toggleFold')<CR>")
	vim.keymap.set("n", "zC", "<Cmd>call VSCodeNotify('editor.foldRecursively')<CR>")
	vim.keymap.set("n", "zO", "<Cmd>call VSCodeNotify('editor.unfoldRecursively')<CR>")
	vim.keymap.set("n", "zM", "<Cmd>call VSCodeNotify('editor.foldAll')<CR>")
	vim.keymap.set("n", "zR", "<Cmd>call VSCodeNotify('editor.unfoldAll')<CR>")
end
