**revo snippets**

snippets for [revo](https://revo.lung.fyi) in neovim, zed and vscode

43 of them, taken from what revo's examples, benches and docs write over and over: `do … end` functions, matching on `{:ok, v}` and `{:err, e}`, tests, metatable classes, fibers, tcp servers, proc macros

type `mres`, pick it from the menu, and you get

```revo
match expr
	| {:ok, v} => v
	| {:err, e} => e
```

with the cursor on `expr`. tab jumps to the next placeholder, and names that repeat (like the class name in `class`) change together

<p align="center">
<a href="#install">install</a> |
<a href="#snippets">snippets</a> |
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

### snippets

**basics**

| prefix | what you get |
|---|---|
| `hdr` | `#!/usr/bin/env revo` and a header comment |
| `fn` | `fn name() do … end` |
| `fna` | `fn(x) do … end`, for callbacks |
| `fori` | `for i in 0..n do … end` |
| `forin` | `for x in items do … end` |
| `ife` | `if cond do … end else do … end` |
| `doc` | `#* … *#` |
| `docm` | `#* … *#` over several lines |
| `des` | `const {a, b} = …` |
| `imp` | an `import { … }` block with an alias |

**errors and matching**

| prefix | what you get |
|---|---|
| `rok` | `{:ok, value}` |
| `rerr` | `{:err, :Error}` |
| `fnr` | a function that returns `{:err, …}` early, else `{:ok, …}` |
| `mres` | `match` on `{:ok, v}` and `{:err, e}` |
| `match` | `match` with a `when` guard and a `_` arm |
| `blk` | `do/b … end`, left early with `break/b(value)` |
| `loopl` | `loop/l do … end` that gives back `break/l(value)` |

**tests**

| prefix | what you get |
|---|---|
| `test` | `test "name" do expect(cond)? end` |
| `suite` | a `suite` with a `test` inside |
| `eq` | `expect_eq(actual, expected)?` |

**tables and types**

| prefix | what you get |
|---|---|
| `class` | a class table, a `.new` constructor with `set_meta`, and a method |
| `tobj` | a structural type, a method for it, and a table of that type |
| `mfn` | `name = fn(self) …,` inside a table |
| `iterm` | an `__iter` metamethod that ends with `:done` |
| `union` | a tagged union type |

**fibers and io**

| prefix | what you get |
|---|---|
| `spawnj` | `spawn` a call, then `join` it |
| `jobs` | one fiber per item, then join them all |
| `chanp` | a channel, a producer fiber, `recv` and `join` |
| `tcpserve` | a line server with one fiber per connection |
| `tcpconn` | connect, send, read the reply, close |
| `readf` | read a whole file |
| `writef` | write a file |
| `stdin` | read stdin line by line until it ends |

**pipelines and debugging**

| prefix | what you get |
|---|---|
| `itmap` | `xs \|> iter.map(fn(x) x) \|> iter.collect()` |
| `itfilter` | `xs \|> iter.filter(fn(x) cond) \|> iter.collect()` |
| `itreduce` | `iter.reduce(xs, fn(acc, x) acc + x, 0)` |
| `dbg` | `print("x = #{x:?}")` |
| `timeit` | how long a block takes, in ms |

**macros, native code and cli**

| prefix | what you get |
|---|---|
| `proc` | a proc macro that returns `{node}` |
| `procv` | a proc macro that folds every argument with one operator |
| `ext` | a typed binding for a `.so` extension |
| `ffifn` | `ffi.load` and one `ffi.func` |
| `cli` | `argparse` with a flag and a positional, usage on error |

`iter.map`, `spawn`, `chan`, `time` and `ffi` are names you type all the time, so their snippets get longer prefixes and the menu stays out of your way

[SURVEY.md](SURVEY.md) has how often each pattern shows up in revo's code and what didn't make the cut

### adding one

```sh
python3 tools/check.py path/to/revo
```

fills in every snippet, runs it with revo, and fails if any of them doesn't. the tcp server gets a real client. a new snippet needs an entry in `CASES` in `tools/check.py`, which wraps it into a program that runs

if you keep typing the same thing in revo, open a [pull request](https://github.com/w0x7y/revo-snippets/pulls)

_credits: [revo](https://github.com/if-not-nil/revo) by if-not-nil. license: [mit](./LICENSE)_
