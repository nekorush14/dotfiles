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
				lualine_y = {
					{ "encoding" },
					{ "filetype" },
					-- { "progress", separator = " ", padding = { left = 1, right = 0 } },
					{ "location", padding = { left = 0, right = 1 } },
				},
				lualine_z = {
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
