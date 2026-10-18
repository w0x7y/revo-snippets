# Revo snippet candidates

Survey of `if-not-nil/revo` at commit `d2f1644` (2026-10-16): all 56 `.rv` files (examples, bench, issues, `src/baselib/base.rv`) and the code blocks in `docs/*.md` and `README.md`.

Counts are matching lines: **rv** = `.rv` files, **docs** = markdown docs. Every snippet below was expanded with its default placeholders and run on a `revo` binary built from that commit. All of them pass. The TCP server was also tested against a real client.

Neither the LSP (`src/lang/workspace/completion.zig`) nor the VS Code extension (`PizzaLvr49/revo-lsp`) ships structural snippets. The LSP only fills in call arguments (`name(${1:p1})`).

The finished snippet files are in `snippets/` (see `snippets/README.md`). Their bodies are the final versions. They differ slightly from the drafts below: more placeholders have runnable defaults, and prefixes that clash with stdlib names were renamed, e.g. `time` became `timeit`.

Bodies use LSP/VS Code snippet syntax: `${1:default}` is a tab stop, a repeated number mirrors the same text, `$0` is the final cursor.

---

## Tier 1: used constantly

### `fn`: multi-line function
rv 102, docs 14. A one-line `fn f(x) expr` is the default, so anything longer needs `do … end`.
```
fn ${1:name}(${2}) do
  $0
end
```

### `fna`: anonymous block function
rv 31, docs 4. Callbacks for pipes, `spawn`, `argparse.parse`, and the `bind` chains in `pipes.rv`.
```
fn(${1:x}) do
  $0
end
```

### `mres`: match on a result
`| {:ok` arms: rv 20, docs 11. `| {:err` arms: rv 18, docs 11. This is the main way errors get handled.
```
match ${1:expr}
  | {:ok, ${2:v}} => ${3:v}
  | {:err, ${4:e}} => ${0:e}
```
When the subject is typed `any` (e.g. `number(...)`), the checker warns "match is not exhaustive". It still runs.

### `match`: match with a guard and a wildcard
`match` rv 54, docs 27. `when` guards rv 28, docs 34.
```
match ${1:x}
  | ${2:v} when ${3:cond} => ${4}
  | _ => ${0}
```

### `rok` / `rerr`: result values
`{:ok,` rv 75, docs 25. `{:err,` rv 50, docs 24. Short, but the brace, colon and comma are fiddly to type.
```
{:ok, ${1}}
```
```
{:err, :${1:Error}}
```

### `fnr`: function that returns a result
`safe_div` alone is rewritten 5 times across docs and examples. `parse_version` in the docs and `undotree.rv` follow the same shape.
```
fn ${1:name}(${2}) do
  if ${3:cond} return {:err, :${4:Error}}
  {:ok, ${0}}
end
```

### `fori` / `forin`: loops
`for … in` rv 49, docs 7, including 27 over ranges. `for x, i in t` gives the index too.
```
for ${1:i} in ${2:0}..${3:n} do
  $0
end
```
```
for ${1:x} in ${2:items} do
  $0
end
```

### `ife`: if/else block
`end else do` rv 10. Block-form `if … do` rv 20. In this form `else` goes *after* `end`, which you don't guess from other languages.
```
if ${1:cond} do
  $2
end else do
  $0
end
```

### `doc` / `docm`: doc comments
`#*` rv 61 outside the stdlib, 264 inside `base.rv`. They feed the LSP hover, `:h` in the REPL, and `revo doc`.
```
#* $0 *#
```
```
#*
$0
*#
```

### `hdr`: script header
24 of the 47 example and bench files start with one. The shebang line opens a block comment that `!#` closes.
```
#!/usr/bin/env revo
 ${1:what this script does}
!#
$0
```

---

## Tier 2: structure

### `test` / `suite` / `eq`
`test "…"` rv 13, docs 6. `suite` rv 4. `expect(…)?` rv 13, docs 6. A failure only propagates if the call ends in `?`, which is easy to forget.
```
test "${1:name}" do
  expect(${0:cond})?
end
```
```
suite "${1:name}" do
  test "${2:name}" do
    $0
  end
end
```
```
expect_eq(${1:actual}, ${2:expected})?
```

### `class`: Lua-style class with a metatable
`bench/richards.rv` repeats this skeleton 8 times: 8 `fn X.new` constructors, 8 identical `set_meta(obj, { __index = X })` calls, and 28 `fn X:method` definitions. The class name appears four times, so mirroring saves real typing.
```
const ${1:Name} = { class = :${1} }

fn ${1}.new(${2}) do
  const obj = { ${3} }
  set_meta(obj, { __index = ${1} })
end

fn ${1}:${4:method}() do
  $0
end
```

### `tobj`: typed table with methods
`demo.rv` does this 3 times and `markov.rv` twice. Each method name is written three times: in the type, in the `fn`, and in the table literal.
```
type ${1:Counter} = { ${2:n}: ${3:number}, ${4:inc}: function }

fn ${5:counter_inc}(self: ${1}) do
  $0
end

let ${6:c}: ${1} = { ${2} = ${7:0}, ${4} = ${5} }
```

### `mfn`: method field inside a table literal
`fn(self` rv 19.
```
${1:name} = fn(self${2}) ${0},
```

### `iterm`: `__iter` metamethod
4 hand-written copies (`builtins/iter.rv` twice, docs twice). The iterator must return `:done` to stop, and the counter setup is easy to get wrong.
```
__iter = fn(self) do
  let i = -1
  fn() do
    i += 1
    if i >= len(${1:self}) :done else ${1}[i]
  end
end,
```

### `blk` / `loopl`: labeled block and loop
Labeled forms rv 6, docs 6. `redis.rv` uses `do/a … break/a` three times as guard clauses inside match arms. The label has to match, so it is mirrored.
```
do/${1:b}
  if ${2:cond} break/${1}(${3:value})
  $0
end
```
```
loop/${1:l} do
  $0
  if ${2:cond} break/${1}(${3:value})
end
```

### `union`: tagged union type
`type X =` rv 12, docs 9.
```
type ${1:Shape} =
    {:${2:circle}, ${3:number}}
  | {:${4:point}}
```

### `des`: destructuring
rv 18, docs 6. Marginal: it's short, but it's everywhere.
```
const {${1:a}, ${2:b}} = ${0}
```

### `imp`: import block with an alias
```
import {
  "${1:module}",
  ${2:alias} = "${3:path}",
}
```

---

## Tier 3: concurrency and I/O

### `spawnj` / `jobs`
`spawn` rv 21, docs 11. `join(` rv 14, docs 6. `threads.rv` shows the fan-out pattern.
```
const ${1:h} = spawn ${2:worker}(${3})
join(${1})
```
```
let jobs = {}
for ${1:x} in ${2:items}
  jobs:push(spawn ${3:worker}(${1}))
for job in jobs
  join(job)
```

### `tcpserve`: async TCP server
There are 5 near-copies: `nbnet.rv`, `redis.rv`, twice in `async.md`, and once in `docs.md`. `spawn` per connection is what makes it concurrent.
```
fn ${1:handle}(peer) do
  loop do
    match peer:recv({ mode = :read_line })
    | {:ok, line} => peer:send("#{line}\n")?
    | {:err, _} => do
      peer:close()?
      return :nil
    end
  end
end

const server = net.listen(${2:8080})?
loop spawn ${1}(server:accept()?)
```

### `tcpconn`: TCP client
```
const conn = net.connect("${1:127.0.0.1}", ${2:8080})?
conn:send(${3:"hello"})?
const reply = conn:recv({ mode = :read_some })?
conn:close()?
```

### `readf` / `writef`: files
`fs.open` rv 4, docs 6 (`markov.rv`, `errors.rv`, docs).
```
const ${1:text} = fs.open(${2:path})?:read()?
```
```
const f = fs.open(${1:path}, "w")?
f:write(${2:data})?
f:close()?
```

### `stdin`: read stdin line by line
`json.rv` and `plot.rv` both do this, and `plot.rv` needs a `while do … end do` trick for it.
```
loop do
  match input()
  | {:ok, ${1:line}} => $0
  | {:err, _} => break(:nil)
end
```
A bare `break` at the end of the last arm, right before `end`, fails with "unexpected token". Use `break(:nil)`. To read everything at once, use `input({delimiter = :eof})?`.

### `chanp`: channel between fibers
Rare in the code (rv 2, docs 3) but it's the standard pairing with `spawn`.
```
const ${1:ch} = chan(${2})
const ${3:p} = spawn (fn() send(${1}, ${4:value}))()
recv(${1})
```

---

## Tier 4: pipelines and debugging

### `itmap` / `itfilter` / `itreduce`
`collect` rv 18, docs 4. `map` rv 10, `reduce`/`fold` rv 10. `map` and `filter` are lazy, so forgetting `collect()` hands you an iterator instead of a table. Including it in the snippet prevents that.
```
${1:xs} |> iter.map(fn(${2:x}) ${3}) |> iter.collect()
```
```
${1:xs} |> iter.filter(fn(${2:x}) ${3}) |> iter.collect()
```
```
iter.reduce(${1:xs}, fn(acc, ${2:x}) ${3:acc + x}, ${4:0})
```

### `dbg`: labeled debug print
`#{x:p}` / `#{x:?}` rv 12, `inspect` rv 13. `:?` is the debug format, `:p` pretty-prints.
```
print("${1:x} = #{${1}:?}")
```

### `timeit`: timing a block
`time.now()` rv 8, across the benches and `threads.rv`.
```
const start = time.now()
$0
print("took #{time.now() - start}ms")
```

---

## Tier 5: metaprogramming, FFI, CLI

### `proc` / `procv`: proc macros
`proc name!(` rv 14, docs 6. `iter:next` rv 19, docs 16. The return value must be a table wrapping one AST node (`{node}`).
```
proc ${1:name}!(iter) do
  let ${2:a} = iter:next()
  {${0:a}}
end
```
```
proc ${1:name}!(iter) do
  let acc = iter:next()
  while iter:peek() != :nil do
    acc = {:binary, :${2:add}, acc, iter:next()}
  end
  {acc}
end
```

### `ext`: typed binding for a native extension
5 files (`foreign/c`, `zig`, `raylib`, `cffi`) plus `c.md`. The bare name on the last line is the module value, and it's easy to leave out.
```
const ${1:ext}: {
  #* ${2:doc} *#
  ${3:func}: fn(${4}) -> ${5:any},
} = import "./${1}.so"
${1}
```

### `ffifn`: call a C function directly
```
let ${1:libc} = ffi.load("${2}")
let ${3:strlen} = ffi.func(${1}, "${4:strlen}", :${5:u64}, {${6::string}})
```

### `cli`: argparse
Only `builtins/args.rv` uses it, but every CLI script needs it, and the callback-plus-`argv` shape is hard to remember.
```
const args = argparse.parse(fn(p) do
  p:flag(:${1:verbose}, { short = "${2:v}", description = "${3}" })
  p:positional(:${4:file}, { description = "${5}" })
end, argv)
if args.err panic(argparse.usage(args))
$0
```

---

## Not worth a snippet

- **One-line `fn name(a) expr`** (rv 36, docs 26): faster to type than to pick from a menu.
- **`|> _:method()`**: three characters of syntax.
- **`lib:func("Name", {...}, :v)`** (rv 25): all 25 are in 3 raylib files, one per bound function. That's a case for generating bindings, not a snippet.
- **`comp (...)`**: used once in the examples.

## Repeated code that belongs in the stdlib or docs, not in snippets

- **Result combinators.** `pipes.rv` hand-writes `bind`, `unwrap_or_else` and `or_else_msg`, and `errors.rv` has `# TODO: add good and_then patterns`. `table` only has `unwrap` and `unwrap_err`.
- **Max of a table.** `undotree.rv` writes `_histmax` with the comment "math.max doesn't do tables". `math.max` is variadic only.
- **Examples rewriting functions that already exist:**
  - `one_of` in `markov.rv` duplicates `table:contains?`.
  - `indices` in `plot.rv` duplicates `iter.enumerate`.
  - `append` in `plot.rv` duplicates `:push`.

  Worth fixing, since people copy from the examples.
