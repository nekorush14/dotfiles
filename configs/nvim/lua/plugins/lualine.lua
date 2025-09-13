return {
	{
		"nvim-lualine/lualine.nvim",
		opts = {
			options = {
				component_separators = "|",
				section_separators = { left = "", right = "" },
			},
			sections = {
				lualine_a = { { "mode", separator = { left = "" }, right_padding = 1, left_padding = 1 } },
				lualine_c = {
					{ "diagnostics" },
				},
				lualine_y = {
					{ "encoding" },
					{ "filetype" },
					{
						"lsp_status",
						ignore_lsp = { "copilot" },
					},
					-- { "progress", separator = " ", padding = { left = 1, right = 0 } },
				},
				lualine_z = {
					{ "location", padding = { left = 0, right = 1 } },
					{
						function()
							return " " .. os.date("%R")
						end,
						separator = { right = "" },
					},
				},
			},
		},
	},
}
