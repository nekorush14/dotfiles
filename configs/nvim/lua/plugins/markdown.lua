-- Disable markdown-toc auto-generation on save
return {
  {
    "stevearc/conform.nvim",
    opts = {
      formatters_by_ft = {
        -- Override LazyVim's markdown extra: exclude markdown-toc
        ["markdown"] = { "prettier", "markdownlint-cli2" },
        ["markdown.mdx"] = { "prettier", "markdownlint-cli2" },
      },
    },
  },
}
