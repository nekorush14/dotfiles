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
						-- indent = 55,
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
						local has_remote = false
						if in_git then
							-- Check if git remote exists
							local handle = io.popen("git remote 2>/dev/null")
							if handle then
								local result = handle:read("*a")
								handle:close()
								has_remote = result and result:match("%S") ~= nil
							end
						end

						local cmds = {
							{
								title = "Open Issues",
								cmd = has_remote and "gh issue list -L 3" or "echo 'No remote repository'",
								key = "i",
								action = function()
									if has_remote then
										vim.fn.jobstart("gh issue list --web", { detach = true })
									end
								end,
								icon = " ",
								height = 7,
							},
							{
								icon = " ",
								title = "Open PRs",
								cmd = has_remote and "gh pr list -L 3" or "echo 'No remote repository'",
								key = "P",
								action = function()
									if has_remote then
										vim.fn.jobstart("gh pr list --web", { detach = true })
									end
								end,
								height = 7,
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
