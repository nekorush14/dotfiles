return {
	{
		"folke/snacks.nvim",
		keys = {
			{
				"<leader>k",
				function()
					require("snacks").dashboard()
				end,
				desc = "Open dashboard",
			},
		},
		opts = {
			picker = {
				hidden = true,
				sources = {
					files = { hidden = false },
				},
			},
			explorer = {
				show_hidden = true,
			},
			terminal = {
				win = {
					border = "none", -- Remove terminal header/title
					keys = {
						nav_h = {},
						["<C-l>"] = false, -- Disable custom Ctrl+l to allow standard terminal clear
					},
				},
			},
			dashboard = {
				preset = {
					pick = function(cmd, opts)
						return LazyVim.pick(cmd, opts)()
					end,
					header = string.format(
						[[ 
         ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄                                                                      
       ▄▀            ▄       ▀▄                                                                    
       █  ▄    ▄              █                                                                    
       █            ▄█▄▄  ▄   █ ▄▄▄      ███╗   ██╗███████╗██╗  ██╗ ██████╗ ██╗   ██╗██╗███╗   ███╗
▄▄▄▄▄  █      ▀    ▀█  ▀▄     █▀▀ ██     ████╗  ██║██╔════╝██║ ██╔╝██╔═══██╗██║   ██║██║████╗ ████║
██▄▀██▄█   ▄       ██    ▀▀▀▀▀    ██     ██╔██╗ ██║█████╗  █████╔╝ ██║   ██║██║   ██║██║██╔████╔██║
 ▀██▄▀██        ▀ ██▀             ▀██    ██║╚██╗██║██╔══╝  ██╔═██╗ ██║   ██║╚██╗ ██╔╝██║██║╚██╔╝██║
   ▀████ ▀    ▄   ██   ▄█    ▄ ▄█  ██    ██║ ╚████║███████╗██║  ██╗╚██████╔╝ ╚████╔╝ ██║██║ ╚═╝ ██║
      ▀█    ▄     ██    ▄   ▄  ▄   ██    ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝   ╚═══╝  ╚═╝╚═╝     ╚═╝
      ▄█▄           ▀▄  ▀▀▀▀▀▀▀▀  ▄▀                                                               
     █▀▀█████████▀▀▀▀████████████▀                 @nekorush14 | LazyVim | nvim: v%s          
     ████▀  ███▀      ▀███  ▀██▀                                                                   
]],
						vim.version()
					),
          -- stylua: ignore
          ---@type snacks.dashboard.Item[]
          keys = {
            { icon = " ", key = "f", desc = "Find File", action = ":lua Snacks.dashboard.pick('files')" },
            { icon = " ", key = "n", desc = "New File", action = ":ene | startinsert" },
            { icon = " ", key = "g", desc = "Find Text", action = ":lua Snacks.dashboard.pick('live_grep')" },
            { icon = " ", key = "r", desc = "Recent Files", action = ":lua Snacks.dashboard.pick('oldfiles')" },
            { icon = " ", key = "b", desc = "Browse Repo", action = function() Snacks.gitbrowse() end },
            { icon = " ", key = "c", desc = "Config", action = ":lua Snacks.dashboard.pick('files', {cwd = vim.fn.stdpath('config')})" },
            { icon = "󰁯 ", key = "s", desc = "Restore Session", section = "session" },
            { icon = " ", key = "x", desc = "Lazy Extras", action = ":LazyExtras" },
            { icon = "󰒲 ", key = "l", desc = "Lazy", action = ":Lazy" },
            { icon = " ", key = "m", desc = "Mason", action = ":Mason" },
            { icon = " ", key = "q", desc = "Quit", action = ":qa" },
          },
				},
				sections = {
					{
						section = "header",
						padding = 3,
						width = 180,
						indent = 55,
					},
					{
						pane = 2,
						section = "terminal",
						cmd = "echo ''",
						height = 15,
						indent = 55,
						padding = 2,
					},
					{ section = "keys", gap = 1, padding = 1 },
					function()
						local in_git = Snacks.git.get_root() ~= nil
						local cmds = {
							{
								title = "Open Issues",
								cmd = "gh issue list -L 3",
								key = "i",
								action = function()
									vim.fn.jobstart("gh issue list --web", { detach = true })
								end,
								icon = " ",
								height = 5,
							},
							{
								icon = " ",
								title = "Open PRs",
								cmd = "gh pr list -L 3",
								key = "P",
								action = function()
									vim.fn.jobstart("gh pr list --web", { detach = true })
								end,
								height = 5,
							},
							{
								icon = " ",
								title = "Git Status",
								cmd = "git --no-pager diff --stat -B -M -C",
								height = 10,
							},
						}
						return vim.tbl_map(function(cmd)
							return vim.tbl_extend("force", {
								pane = 2,
								section = "terminal",
								enabled = in_git,
								padding = 1,
								ttl = 5 * 60,
								indent = 3,
							}, cmd)
						end, cmds)
					end,
					{ section = "startup" },
				},
			},
		},
	},
}
