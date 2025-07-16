return {
  {
    "neovim/nvim-lspconfig",
    opts = {
      servers = {
        ruby_lsp = {
          cmd = { "ruby-lsp" },
          filetypes = { "ruby" },
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
