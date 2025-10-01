return {
	"rachartier/tiny-inline-diagnostic.nvim",
	event = "VeryLazy",
	priority = 1000,
	config = function()
		require("tiny-inline-diagnostic").setup({
			preset = "ghost",
			options = {
				-- Configuration for multiline diagnostics
				-- Can be a boolean or a table with detailed options
				multilines = {
					-- Enable multiline diagnostic messages
					enabled = true,

					-- Always show messages on all lines for multiline diagnostics
					always_show = true,
				},
				-- Display all diagnostic messages on the cursor line, not just those under cursor
				show_all_diags_on_cursorline = false,
			},
		})
		vim.diagnostic.config({ virtual_text = false }) -- Disable default virtual text
	end,
}
