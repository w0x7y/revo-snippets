# `revo snippets`
### The tests for this project was made using AI Agents!
snippets for [revo](https://revo.lung.fyi) in neovim, zed and vscode

example:
type `mres`, pick it from the menu, and you get

```revo
match expr
	| {:ok, v} => v
	| {:err, e} => e
```

with the cursor on `expr`. tab jumps to the next placeholder, and names that repeat (like the class name in `class`) change together. [snippets.md](snippets.md) has every snippet with what it expands to

<p align="center">
	<a href="#install">install</a> |
	<a href="snippets.md">all snippets</a> |
	<a href="#adding-one">adding one</a>
</p>

### install

all three editors read the same file, [`snippets/revo.json`](snippets/revo.json). the file has to be recognized as revo, otherwise no snippets show up

**neovim**

with lazy.nvim and LuaSnip

```lua
{
  "L3MON4D3/LuaSnip",
  dependencies = { "w0x7y/revo-snippets" },
  config = function()
    require("luasnip.loaders.from_vscode").lazy_load()
  end,
}
```

if you already load friendly-snippets this way, adding `"w0x7y/revo-snippets"` to the dependencies is enough

~ **mini.snippets:** install the plugin, `gen_loader.from_lang()` finds it\
~ **blink.cmp:** install the plugin and add it to the search paths

```lua
sources = {
  providers = {
    snippets = {
      opts = {
        search_paths = {
          vim.fn.stdpath("config") .. "/snippets",
          vim.fn.stdpath("data") .. "/lazy/revo-snippets",
        },
      },
    },
  },
},
```

neovim doesn't know `.rv` files yet. if nothing in your config sets the filetype, add

```lua
vim.filetype.add({ extension = { rv = "revo", revo = "revo" } })
```

**zed**

needs [revo-zed-extension](https://github.com/w0x7y/revo-zed-extension)

```sh
curl -fL --create-dirs -o ~/.config/zed/snippets/revo.json \
  https://raw.githubusercontent.com/w0x7y/revo-snippets/main/snippets/revo.json
```

**vscode**

needs [revo-lsp](https://github.com/PizzaLvr49/revo-lsp), which adds the revo language

```sh
curl -fL --create-dirs -o ~/.config/Code/User/snippets/revo.json \
  https://raw.githubusercontent.com/w0x7y/revo-snippets/main/snippets/revo.json
```

on macos the folder is `~/Library/Application Support/Code/User/snippets/`, on windows `%APPDATA%\Code\User\snippets\`

### adding one

```sh
python3 tools/check.py path/to/revo
```

fills in every snippet, runs it with revo, and fails if any of them doesn't. the tcp server gets a real client. a new snippet needs an entry in `CASES` in `tools/check.py`, which wraps it into a program that runs, and a section in [snippets.md](snippets.md)

if you keep typing the same thing in revo, open a [pull request](https://github.com/w0x7y/revo-snippets/pulls)

_credits: [revo](https://github.com/if-not-nil/revo) by if-not-nil. license: [mit](./LICENSE)_
