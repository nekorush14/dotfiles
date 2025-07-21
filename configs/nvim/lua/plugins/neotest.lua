return {
	{
		"nvim-neotest/neotest",
		optional = true,
		dependencies = {
			"olimorris/neotest-rspec",
			"nvim-neotest/neotest-python",
		},
		opts = {
			adapters = {
				["neotest-rspec"] = {
					-- NOTE: By default neotest-rspec uses the system wide rspec gem instead of the one through bundler
					rspec_cmd = function()
						-- return vim.inspect({
						return vim.tbl_flatten({
							"bundle",
							"exec",
							"rspec",
						})
					end,
				},
				["neotest-python"] = {
					-- Here you can specify the settings for the adapter, i.e.
					runner = "pytest",
					python = ".venv/bin/python",
				},
			},
		},
	},
}
