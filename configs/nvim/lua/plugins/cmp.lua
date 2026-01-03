-- nvim-cmp configuration
-- Use Tab to confirm completion instead of Enter
return {
  {
    "hrsh7th/nvim-cmp",
    opts = function(_, opts)
      local cmp = require("cmp")

      opts.mapping = vim.tbl_extend("force", opts.mapping or {}, {
        -- Tab to confirm completion
        ["<Tab>"] = cmp.mapping.confirm({ select = true }),
        -- Disable Enter for confirmation (optional - comment out to keep Enter as well)
        ["<CR>"] = cmp.config.disable,
      })

      return opts
    end,
  },
}
