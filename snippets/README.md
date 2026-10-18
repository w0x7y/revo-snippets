# Revo snippets

43 snippets for Revo (`.rv`) in VS Code snippet format. The `revo.json` files in `vscode/`, `zed/` and `nvim/` are identical. If you edit one, copy it to the other two.

Each snippet's prefix, and where it came from, is listed in `../revo-snippets.md`.

## VS Code

Requires the [revo-lsp](https://github.com/PizzaLvr49/revo-lsp) extension, which registers the `revo` language.

```sh
cp vscode/revo.json ~/.config/Code/User/snippets/revo.json
```

On macOS the folder is `~/Library/Application Support/Code/User/snippets/`.

## Zed

Requires the [revo-zed-extension](https://github.com/w0x7y/revo-zed-extension), which registers the `Revo` language.

```sh
mkdir -p ~/.config/zed/snippets
cp zed/revo.json ~/.config/zed/snippets/revo.json
```

## Neovim

The files use the VS Code format that LuaSnip, blink.cmp and mini.snippets all read. The filetype must be `revo`.

```sh
mkdir -p ~/.config/nvim/snippets
cp nvim/package.json nvim/revo.json ~/.config/nvim/snippets/
```

- **LuaSnip:** `lazy_load()` without arguments only scans the root of each runtimepath directory, so point it at the folder:

  ```lua
  require("luasnip.loaders.from_vscode").lazy_load({ paths = { vim.fn.stdpath("config") .. "/snippets" } })
  ```

- **blink.cmp:** reads `~/.config/nvim/snippets` by default. Nothing else to do.
- **mini.snippets:** `gen_loader.from_lang()` finds `snippets/revo.json` on the runtimepath. Nothing else to do.
