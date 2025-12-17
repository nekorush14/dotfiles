return {
	{
		"nvim-lualine/lualine.nvim",
		opts = function(_, opts)
			-- Get the current theme colors from tokyonight
			local colors = require("tokyonight.colors").setup()

			-- Create transparent theme based on tokyonight
			local transparent_theme = {
				normal = {
					a = { bg = colors.blue, fg = colors.bg_dark, gui = "bold" },
					b = { bg = "NONE", fg = colors.blue },
					c = { bg = "NONE", fg = colors.fg_dark },
				},
				insert = {
					a = { bg = colors.green, fg = colors.bg_dark, gui = "bold" },
					b = { bg = "NONE", fg = colors.green },
					c = { bg = "NONE", fg = colors.fg_dark },
				},
				visual = {
					a = { bg = colors.magenta, fg = colors.bg_dark, gui = "bold" },
					b = { bg = "NONE", fg = colors.magenta },
					c = { bg = "NONE", fg = colors.fg_dark },
				},
				replace = {
					a = { bg = colors.red, fg = colors.bg_dark, gui = "bold" },
					b = { bg = "NONE", fg = colors.red },
					c = { bg = "NONE", fg = colors.fg_dark },
				},
				command = {
					a = { bg = colors.yellow, fg = colors.bg_dark, gui = "bold" },
					b = { bg = "NONE", fg = colors.yellow },
					c = { bg = "NONE", fg = colors.fg_dark },
				},
				inactive = {
					a = { bg = "NONE", fg = colors.dark5 },
					b = { bg = "NONE", fg = colors.dark5 },
					c = { bg = "NONE", fg = colors.dark5 },
				},
			}

			opts.options = opts.options or {}
			opts.options.theme = transparent_theme
			opts.options.component_separators = "|"
			opts.options.section_separators = { left = "", right = "" }

			opts.sections = opts.sections or {}
			opts.sections.lualine_a = { { "mode", separator = { left = "" }, right_padding = 1, left_padding = 1 } }
			opts.sections.lualine_b = {
				{ "branch" },
				{ "diff", separator = { right = "" } },
			}
			opts.sections.lualine_c = {
				{ "diagnostics", separator = { right = "" } },
			}
			opts.sections.lualine_x = {
				Snacks.profiler.status(),
          -- stylua: ignore
          {
            function() return require("noice").api.status.command.get() end,
            cond = function() return package.loaded["noice"] and require("noice").api.status.command.has() end,
            color = function() return { fg = Snacks.util.color("Statement") } end,
          },
          -- stylua: ignore
          {
            function() return require("noice").api.status.mode.get() end,
            cond = function() return package.loaded["noice"] and require("noice").api.status.mode.has() end,
            color = function() return { fg = Snacks.util.color("Constant") } end,
          },
          -- stylua: ignore
          {
            function() return "  " .. require("dap").status() end,
            cond = function() return package.loaded["dap"] and require("dap").status() ~= "" end,
            color = function() return { fg = Snacks.util.color("Debug") } end,
          },
          -- stylua: ignore
          {
            require("lazy.status").updates,
            cond = require("lazy.status").has_updates,
            color = function() return { fg = Snacks.util.color("Special") } end,
          },
			}
			opts.sections.lualine_y = {
				{ "encoding", separator = { left = "" } },
				{ "filetype" },
				{
					"lsp_status",
					ignore_lsp = { "copilot" },
				},
				-- { "progress", separator = " ", padding = { left = 1, right = 0 } },
			}
			opts.sections.lualine_z = {
				{ "location" },
				{
					function()
						return " " .. os.date("%R")
					end,
					separator = { right = "" },
				},
			}

			return opts
		end,
	},
}
