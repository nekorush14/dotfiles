return {
  {
    "mfussenegger/nvim-lint",
    opts = function(_, opts)
      -- Disable MD013 and MD036 for markdownlint-cli2
      opts.linters = opts.linters or {}
      opts.linters["markdownlint-cli2"] = {
        args = {
          "--config",
          vim.fn.expand("~/.markdownlint-cli2.jsonc"),
        },
      }
      return opts
    end,
  },
}
