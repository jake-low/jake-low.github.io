---
date: 2016-02-09
license: CC BY 4.0
title: The for-else construct in Python
---

Thought your Python `else` clauses needed to be preceded by `if`s? Think again. Python's loop constructs (`for` and `while`) can also have `else` branches. Read on if you're wondering how these constructions work.

## The short version

> Loop statements may have an `else` clause; it is executed when the loop terminates through exhaustion of the list (with `for`) or when the condition becomes false (with `while`), but not when the loop is terminated by a `break` statement.
>
> --- <cite>[Python 3 tutorial][tut-3], §4.4</cite> [^first-introduced]

## Why was this syntax chosen?

The `for…else` syntax has been widely attributed in the Python community to Donald Knuth.[^knuth] I've sometimes heard criticism of Guido van Rossum's choice to emulate the Knuth syntax in Python, rooted in the seemingly unintuitive behaviour of the `for…else` and `while…else` constructions when compared to the traditional `if…else`. Why not choose a different keyword? The most commonly suggested is `nobreak`, which is appealingly self-describing.

These concerns come from a desire to make Python intuitive and friendly, which I am wholeheartedly on-board with. It does seem that this feature is both little-known and commonly misunderstood; a poll[^poll] in the Python community shows that even seasoned Python developers are unaware of it, and frequently misunderstand its semantics when shown example usages.

However, I think there is a compelling explanation for the Knuth syntax. With any luck, knowing this explanation will make the Python syntax seem much more intuitive.

Let's start by considering `while`, because it will be helpful in understanding `for` later on.

```python
cards = ['ace', 'queen', 'ten', 'six', 'two']
tries = 0

while tries < 5:
  tries += 1
  card = random.choice(cards)
  if card == 'ace':
    print("drew an ace on try {}".format(tries))
    break
else: # if tries >= 5:
  print("tried 5 times, failed to draw an ace")
```

The code above loops up to five times, trying to draw the ace from the list of cards. If it happens to succeed, it will inform the user that it did, otherwise it will print a message indicating failure.

The key observation is that the `else` branch executes _if and when the condition becomes false_. Note the comment on the `else` line -- that else could be replaced with the commented-out `if` without changing the code's behavior.

An `else` statement always "shares" a condition with another statement; this is why `else` can't stand on its own. In the case you're used to seeing, `else` shares the condition of the previous `if`. In this new syntax, the `else` shares the condition of the `while`.

Now let's look at `for`.

```python
coins = ['penny', 'nickel', 'dime']

for coin in coins:
  flip = random.choice(('heads', 'tails'))
  if flip == 'heads':
    print("flipping the {} came up heads".format(flip))
    break
else:
  print "flipped all the coins, but none came up heads"
```

This is weird, right? There's no condition in the `for` statement, so what condition is the `else` branch using?

To understand this code, let's rewrite it in pseudo-C.

```c
const char * coins[3] = {"penny", "nickel", "dime"};

for (int i = 0; i < 3; ++i) {
  bool heads = rand() % 2;
  if (heads) {
    printf("flipping the %s came up heads\n", coins[i]);
    break;
  }
} else { // this isn't real C syntax; just pretend
  printf("flipped all the coins, but none came up heads");
}
```

Now, in this made-up example it's clear what condition the `else` is sharing -- it's the `i < 3` condition in the `for` loop. When this condition becomes false, the loop body stops executing, and the `else` branch is executed once instead.

Deconstructing Python's `for` loop, which operates on iterables[^foreach], into a lower-level C-style `for` loop (which is just syntax sugar for a `while`) makes it much easier to understand Python's `for…else` behavior. The `else` shares the _implicit_ condition of the `for` loop: the one that _would_ be necessary in a lower-level language like C, where the programmer has to do the iterating by hand.

Of course, not all iterators are sequences. When considering `for` loops that iterate over dictionaries, file objects, or `yield` generators, the analogy breaks[^pun] down. Nonetheless, recalling C's loop syntax is a useful tool to remind yourself of the meaning of `for…else` in Python: the `else` shares the implicit condition that the `for` loop is using to determine _whether iteration will continue_; if and when that condition becomes false, the `else` is evaluated.

## Use case

I find the `else` syntax for loops primarily useful when the code inside the loop is _attempting something that may fail_, and the loop itself is a retry mechanism.

In these cases it's typical to `break` out of the loop once the action succeeds. But to handle the error in the case that the loop finishes without the action ever succeeding, you need to keep a flag to track whether or not the conditional `break` has been executed.

As an example, consider this code which connects to any of several servers, raising an error if none can be reached.

```python
servers = ['alpha.example.com', 'beta.example.com', 'gamma.example.com']
connected = False

for server in servers:
    try:
        sock = socket.create_connection((server, 443))
        connected = True
        break
    except socket.error:
        continue

if not connected:
    raise RuntimeError("couldn't connect to any server")
```

In the above code, the `connected` boolean is being used to track whether the loop was exited because a connection was successful, or because we ran out of servers. Tracking state in a boolean like this is error-prone -- what if we forget to set it, or set it incorrectly?

Instead, we can use a `for…else` loop to capture the error-handling logic, and eliminate the boolean.

```python
servers = ['alpha.example.com', 'beta.example.com', 'gamma.example.com']

for server in servers:
    try:
        sock = socket.create_connection((server, 443))
        break
    except socket.error:
        continue
else:
    raise RuntimeError("couldn't connect to any server")
```

Now, we're using the `for…else` semantics to raise an error _only if the loop exhausts the iterable_, which in this case happens when we run out of servers to try.

In the case that we successfully connect to a server, the `break` statement ends the loop early, skipping the `else` branch.

## In conclusion

As a semantic construct, `else` cannot stand on its own; it must share the condition of another block. In the familiar case, the `else` shares the condition of the previous `if`. The `if` possesses an explicit condition, provided by the programmer, and the `else` implicitly represents its inverse.

Loops possess a condition too; it dictates whether iteration will continue. The `while` loop's condition is explicit; the programmer provides an expression to use. In Python, the `for` loop's condition is implicit; the condition is the conceptual test of _whether there are items remaining in the provided iterable_. In either case, the loop terminates when the condition becomes false.

When used with a loop construct, the `else` branch shares the loop condition. If the condition becomes false, the loop will exit, and the `else` will be evaluated. However, it's also possible to exit a loop before the condition becomes false, by using a `break` statement. When a loop terminates due to a `break`, the condition is still true, so the `else` is not evaluated.


[^first-introduced]: Though I've cited the Python 3 documentation here, this feature is nearly as old as Python itself; you can see that the language in the tutorial is [exactly the same][tut-1] in the documentation for Python 1.4.

[^knuth]: I suspected it might have appeared in <cite>Structured Programming with Go To Statements</cite>, but I was unable to find a citation.

[^poll]: Referenced in [this discussion][for-each-ideas] about the syntax.

[^foreach]: This is referred to, both in certain languages' syntax and colloquially, as a "foreach" loop.

[^pun]: Pun intended.

[tut-3]: https://docs.python.org/3/tutorial/controlflow.html#break-and-continue-statements-and-else-clauses-on-loops
[tut-1]: https://docs.python.org/release/1.4/tut/node31.html#SECTION00540000000000000000
[for-each-ideas]: https://mail.python.org/pipermail/python-ideas/2009-October/006155.html
