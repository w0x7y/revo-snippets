**all the snippets**

every snippet, what it expands to, and where tab takes you. back to the [readme](README.md)

**how to read this**

~ the code block is what you get before you type anything\
~ **tab** lists the placeholders in the order tab visits them. the last one is where the cursor ends up\
~ a placeholder marked _(×3)_ shows up three times and changes everywhere as you type\
~ indentation is two spaces here; your editor uses its own setting\
~ `spawn`, `chan`, `time`, `ffi` and `iter.map` are names you type anyway, so their snippets have longer prefixes and the menu stays out of your way

| section | snippets |
|---|---|
| [basics](#basics) | [`hdr`](#hdr) [`fn`](#fn) [`fna`](#fna) [`fori`](#fori) [`forin`](#forin) [`ife`](#ife) [`doc`](#doc) [`docm`](#docm) [`des`](#des) [`imp`](#imp) |
| [errors and matching](#errors-and-matching) | [`rok`](#rok) [`rerr`](#rerr) [`fnr`](#fnr) [`mres`](#mres) [`match`](#match) [`blk`](#blk) [`loopl`](#loopl) |
| [tests](#tests) | [`test`](#test) [`suite`](#suite) [`eq`](#eq) |
| [tables and types](#tables-and-types) | [`class`](#class) [`tobj`](#tobj) [`mfn`](#mfn) [`iterm`](#iterm) [`union`](#union) |
| [fibers and io](#fibers-and-io) | [`spawnj`](#spawnj) [`jobs`](#jobs) [`chanp`](#chanp) [`tcpserve`](#tcpserve) [`tcpconn`](#tcpconn) [`readf`](#readf) [`writef`](#writef) [`stdin`](#stdin) |
| [pipelines and debugging](#pipelines-and-debugging) | [`itmap`](#itmap) [`itfilter`](#itfilter) [`itreduce`](#itreduce) [`dbg`](#dbg) [`timeit`](#timeit) |
| [macros, native code and cli](#macros-native-code-and-cli) | [`proc`](#proc) [`procv`](#procv) [`ext`](#ext) [`ffifn`](#ffifn) [`cli`](#cli) |

---

### basics

#### `hdr`

a header for a script you run directly

```revo
#!/usr/bin/env revo
 what this script does
!#
```

**tab:** `what this script does` → the code below

`#!` starts a block comment and `!#` ends it, so the shebang line and the description are both one comment

#### `fn`

a function with a body

```revo
fn name() do

end
```

**tab:** `name` → arguments → body

a one-expression function doesn't need this: `fn double(x) x * 2` is quicker to type than to pick from a menu

#### `fna`

an anonymous function with a body, for callbacks like `iter.map`, `spawn` or `argparse.parse`

```revo
fn(x) do

end
```

**tab:** `x` → body

#### `fori`

a loop over a range of numbers

```revo
for i in 0..n do

end
```

**tab:** `i` → `0` → `n` → body

the range stops before `n`: `0..3` gives 0, 1 and 2

#### `forin`

a loop over a table, a string, or anything with an [`__iter`](#iterm)

```revo
for x in items do

end
```

**tab:** `x` → `items` → body

`for x, i in items` gives you the index too, counting from 0

#### `ife`

an if with an else, both as blocks

```revo
if cond do

end else do

end
```

**tab:** `cond` → the if branch → the else branch

`else` comes after `end`, which is the part other languages get you to write wrong. for short ones, `if cond a else b` works without blocks

#### `doc`

a doc comment, on one line

```revo
#*  *#
```

**tab:** inside the comment

put it right above a function or a table field. it shows up when you hover the name, in `:h` in the repl, and in `revo doc`

#### `docm`

a doc comment over several lines

```revo
#*

*#
```

**tab:** the empty line

#### `des`

take values out of a table into names

```revo
const {a, b} =
```

**tab:** `a` → `b` → the table

#### `imp`

an import block with a plain module and a renamed one

```revo
import {
  "module",
  alias = "path",
}
```

**tab:** `module` → `alias` → `path`

a plain import is named after the last part of its path, so `"./mod"` becomes `mod`

---

### errors and matching

revo has no exceptions. a function that can fail returns `{:ok, value}` or `{:err, :Reason}`, and `?` after a call hands an error straight back to the caller

#### `rok`

a success value

```revo
{:ok, value}
```

**tab:** `value`

#### `rerr`

an error value

```revo
{:err, :Error}
```

**tab:** `Error`

#### `fnr`

a function that checks something first and fails early

```revo
fn name() do
  if cond return {:err, :Error}
  {:ok, value}
end
```

**tab:** `name` → arguments → `cond` → `Error` → `value`

#### `mres`

handle both outcomes of a result

```revo
match expr
  | {:ok, v} => v
  | {:err, e} => e
```

**tab:** `expr` → `v` → `v` → `e` → `e`

if revo can't tell what `expr` returns, like `number("42")`, it warns that the match doesn't cover everything. it still runs

#### `match`

a match with a guarded arm and a catch-all

```revo
match x
  | v when cond => v
  | _ => :nil
```

**tab:** `x` → `v` → `cond` → `v` → `:nil`

arms are tried top to bottom. `when` adds a condition to an arm, and `_` takes whatever's left

#### `blk`

a block you can leave early, with a value

```revo
do/b
  if cond break/b(value)

end
```

**tab:** `b` _(×2)_ → `cond` → `value` → the rest of the block

`break/b(value)` leaves the block and makes `value` its result. good as a guard clause inside a match arm

#### `loopl`

a loop that gives back a value when it stops

```revo
loop/l do

  if cond break/l(value)
end
```

**tab:** `l` _(×2)_ → `cond` → `value` → the loop body

---

### tests

run them with `revo --test file.rv`

#### `test`

a test with one check

```revo
test "name" do
  expect(cond)?
end
```

**tab:** `name` → `cond`

keep the `?`. a failed `expect` returns an error, and without `?` it gets lost if more code follows it, so the test passes

#### `suite`

a group of tests under one name

```revo
suite "name" do
  test "name" do

  end
end
```

**tab:** the suite's name → the test's name → the test body

#### `eq`

check that two values are equal, inside a test

```revo
expect_eq(actual, expected)?
```

**tab:** `actual` → `expected`

---

### tables and types

#### `class`

a class: a table that holds the methods, a constructor, and one method

```revo
const Name = { class = :Name }

fn Name.new() do
  const obj = {  }
  set_meta(obj, { __index = Name })
end

fn Name:method() do

end
```

**tab:** `Name` _(×5)_ → constructor arguments → fields, like `x = x` → `method` → the method body

`set_meta` with `__index` makes an instance look up anything it doesn't have, like its methods, on `Name`. `set_meta` returns the table, so the constructor returns the new instance. a method defined with `:` gets `self`, and you call it with `obj:method()`

#### `tobj`

a typed table with a method: the type, the method's function, and a table of that type

```revo
type Counter = { n: number, inc: function }

fn counter_inc(self: Counter) do

end

let c: Counter = { n = 0, inc = counter_inc }
```

**tab:** `Counter` _(×3)_ → `n` _(×2)_ → `number` → `inc` _(×2)_ → `counter_inc` _(×2)_ → `c` → `0` → the method body

each name is written in two or three places, so you only type it once

#### `mfn`

a method inside a table you're writing out

```revo
name = fn(self) ,
```

**tab:** `name` → more arguments after `self` → body

the comma is there because it sits between other fields

#### `iterm`

make a table work in `for x in t`

```revo
__iter = fn(self) do
  let i = -1
  fn() do
    i += 1
    if i >= len(self) :done else self[i]
  end
end,
```

**tab:** `self` _(×2)_, what to go through

it goes in the metatable, `set_meta(t, { __iter = ... })`. the function it returns gives the next item each time it's called, and `:done` when there are no more

#### `union`

a type that can be one of several tagged tables

```revo
type Shape =
    {:circle, number}
  | {:point}
```

**tab:** `Shape` → `circle` → `number` → `point`

take a `Shape` apart with [`match`](#match): `| {:circle, r} => ...`

---

### fibers and io

`spawn f(x)` runs a call in a new fiber and gives back a handle right away. `join(handle)` waits for it and returns what the call returned

#### `spawnj`

run a call in a fiber, then wait for it

```revo
const h = spawn worker()
join(h)
```

**tab:** `h` _(×2)_ → `worker` → arguments

#### `jobs`

start one fiber per item, then wait for all of them

```revo
let jobs = {}
for x in items
  jobs:push(spawn worker(x))
for job in jobs
  join(job)
```

**tab:** `x` _(×2)_ → `items` → `worker`

the results are thrown away. if you need them, keep what `join(job)` returns

#### `chanp`

send a value from one fiber to another

```revo
const ch = chan()
const producer = spawn (fn() send(ch, value))()
recv(ch)
join(producer)
```

**tab:** `ch` _(×3)_ → buffer size → `producer` _(×2)_ → `value`

`chan()` has no buffer, so `send` waits until another fiber calls `recv`. `chan(2)` holds up to two values before `send` waits

#### `tcpserve`

a tcp server that echoes each line back, with one fiber per connection so clients don't wait for each other

```revo
fn handle(peer) do
  loop do
    match peer:recv({ mode = :read_line })
    | {:ok, line} => peer:send("#{line}\n")?
    | {:err, _} => do
      peer:close()?
      return :nil
    end
  end
end

const server = net.listen(8080)?
loop spawn handle(server:accept()?)
```

**tab:** `handle` _(×2)_ → `8080`

when the client hangs up, `recv` returns an error and the handler closes the connection. put your own logic where the `send` is, and try it with `nc localhost 8080`

#### `tcpconn`

connect to a server, send something, read the reply, close

```revo
const conn = net.connect("127.0.0.1", 8080)?
conn:send("hello")?
const reply = conn:recv({ mode = :read_some })?
conn:close()?
```

**tab:** `127.0.0.1` → `8080` → `"hello"`

`:read_some` takes whatever has arrived. `:read_line`, like in [`tcpserve`](#tcpserve), reads up to a newline

#### `readf`

read a whole file into a string

```revo
const text = fs.open("file.txt")?:read()?
```

**tab:** `text` → `"file.txt"`

opening and reading can both fail, so both get a `?`

#### `writef`

write a file

```revo
const f = fs.open("out.txt", "w")?
f:write("text")?
f:close()?
```

**tab:** `"out.txt"` → `"text"`

`"w"` creates the file, or empties it if it's already there

#### `stdin`

read stdin one line at a time until it ends

```revo
loop do
  match input()
  | {:ok, line} =>
  | {:err, _} => break(:nil)
end
```

**tab:** `line` → what to do with each line

at the end `input()` returns `{:err, :EndOfStream}`. it's `break(:nil)` because a bare `break` right before `end` doesn't parse. to read all of stdin at once, use `input({delimiter = :eof})?`

---

### pipelines and debugging

#### `itmap`

turn every item into something else, as a new table

```revo
xs |> iter.map(fn(x) x) |> iter.collect()
```

**tab:** `xs` → `x` → what each item becomes

`iter.map` doesn't do anything until something reads from it. `iter.collect()` reads it all into a table; without it you get an iterator

#### `itfilter`

keep the items you want, as a new table

```revo
xs |> iter.filter(fn(x) cond) |> iter.collect()
```

**tab:** `xs` → `x` → `cond`, true for the items to keep

needs `iter.collect()` for the same reason as [`itmap`](#itmap)

#### `itreduce`

fold a table into one value. as it is, it adds everything up

```revo
iter.reduce(xs, fn(acc, x) acc + x, 0)
```

**tab:** `xs` → `x` → `acc + x` → `0`, the starting value

#### `dbg`

print a value with its name

```revo
print("x = #{x:?}")
```

**tab:** `x` _(×2)_

`:?` prints the value in debug format. `:p` spreads nested tables over more lines

#### `timeit`

how long some code takes

```revo
const start = time.now()

print("took #{time.now() - start}ms")
```

**tab:** the code to time

`time.now()` is in milliseconds

---

### macros, native code and cli

#### `proc`

a proc macro

```revo
proc name!(iter) do
  let a = iter:next()

  {a}
end
```

**tab:** `name` → `a` _(×2)_ → the macro body

`iter:next()` gives you the next argument of the call as an AST node, before it runs. the macro must return a table holding one node, `{node}`. call it as `name!(...)`

#### `procv`

a proc macro that puts one operator between all its arguments

```revo
proc name!(iter) do
  let acc = iter:next()
  while iter:peek() != :nil do
    acc = {:binary, :add, acc, iter:next()}
  end
  {acc}
end
```

**tab:** `name` → `add`

with `:add`, `name!(1, 2, 3)` turns into `1 + 2 + 3`. revo's examples also use `:mul` and `:div`

#### `ext`

types for a native extension: a `.so` you built from c or zig

```revo
const ext: {
  #* doc *#
  func: fn() -> any,
} = import "./ext.so"
ext
```

**tab:** `ext` _(×3)_ → `doc` → `func` → its arguments → `any`, its return type

this is a file of its own. the bare `ext` on the last line is what the file gives back, so other files can import it. the doc comments show up when you hover a function

#### `ffifn`

call a c function from a library, with no extension to build

```revo
let libc = ffi.load("")
let strlen = ffi.func(libc, "strlen", :u64, {:string})
```

**tab:** `libc` _(×2)_ → the library path → `strlen`, the name in revo → `strlen`, the c name → `u64`, the return type → `:string`, the argument types

an empty path opens the running program, which already has libc in it. for anything else, give the library's path, like `"libm.so.6"`

#### `cli`

read command-line flags and arguments

```revo
const args = argparse.parse(fn(p) do
  p:flag(:verbose, { short = "v", description = "" })
  p:positional(:file, { description = "" })
end, argv)
if args.err panic(argparse.usage(args))
```

**tab:** `verbose` → `v` → what the flag does → `file` → what the argument is → the rest of the script

with `-v in.txt`, `args.flags` is `{ verbose = :true }` and `args.positionals` is `{ file = in.txt }`. bad arguments stop the script with a usage message
