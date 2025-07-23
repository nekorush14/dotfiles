return {
	{
		"neovim/nvim-lspconfig",
		opts = {
			servers = {
				ruby_lsp = {
					cmd = { os.getenv("HOME") .. "/.rbenv/shims/ruby-lsp" },
					filetypes = { "ruby", "eruby" },
					root_dir = function(fname)
						return require("lspconfig.util").root_pattern("Gemfile", ".git")(fname)
					end,
					settings = {
						rubyLsp = {
							enabledFeatures = {
								"documentSymbols",
								"hover",
								"completion",
								"diagnostics",
								"inlayHints",
								"semanticHighlighting",
							},
						},
					},
				},
				rubocop = {
					cmd = { os.getenv("HOME") .. "/.rbenv/shims/rubocop", "--lsp" },
					filetypes = { "ruby", "eruby" },
				},
			},
		},
	},

	{
		"nvim-treesitter/nvim-treesitter",
		opts = {
			ensure_installed = {
				"ruby",
			},
		},
	},
}
