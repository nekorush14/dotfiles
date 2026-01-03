-- Copilot configuration
-- Disable auto-trigger and use Tab key to accept suggestions
return {
  {
    "zbirenbaum/copilot.lua",
    opts = {
      suggestion = {
        auto_trigger = false, -- Disable automatic suggestions
        keymap = {
          accept = "<Tab>", -- Accept suggestion with Tab
          next = "<M-]>", -- Next suggestion
          prev = "<M-[>", -- Previous suggestion
          dismiss = "<C-]>", -- Dismiss suggestion
        },
      },
    },
  },
}
