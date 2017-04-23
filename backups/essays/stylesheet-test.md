---
date: 2015-08-02T00:00:00Z
title: The Big Stylesheet Test
---

Below is just about everything you’ll need to style in the theme. Check the source code to see the many embedded elements within paragraphs.

---

# Heading 1

## Heading 2

### Heading 3

#### Heading 4

##### Heading 5

###### Heading 6

---

Lorem ipsum dolor sit amet, [test link](/test-link). **This is strong**. More running text with some _emphasis in it_. I can also do ***both***.

Here's an Octicon. <i class='octicon octicon-bug'></i>

And here's a Font Awesome icon. <i class='fa fa-puzzle-piece'></i>

What happens if I have a heading whose fragment link is already on the page?

### Signature


Below is an ordered list.

1. Spam
2. Eggs
  - fried
  - scrambled
  - hard-boiled
3. Ham

And here's an unordered one.

- snap
- crackle
  1. krackle?
  2. nah
- pop

---

Here's some code.

~~~python
def spam(eggs, ham):
  print("hello") # python 3!
  assert 2 + 2 == 5

  for i in range(5):
    yield str(i)
~~~

Let's try some real code.

~~~python
import pydoofus.common as common
import pydoofus.exceptions as exceptions
import pydoofus.protobuf.v9 as protobuf
import pydoofus.protobuf.util as util


class Header(object):
    def __init__(self, auth_protocol):
        self.magic = 'hrpc'
        self.version = 9
        self.rpc_service_class = 0.00

        # Here's a comment about the code

        if auth_protocol == 'none':
            self.auth_protocol = 0x00
        elif auth_protocol == 'sasl':
            self.auth_protocol = 0xdf
        else:
            ValueError("unknown auth protocol '%s'" % auth_protocol)

    def serialize(self):
        output = bytearray(self.magic)
        output.append(self.version)
        output.append(self.rpc_service_class)
        output.append(self.auth_protocol)
        return bytes(output)
~~~

And some C...

~~~c
#include <sys/time.h>
#include <sys/types.h>

struct timespec java_to_unix_time(int64_t java_milliseconds) {
	return struct timespec {
		.tv_sec = java_milliseconds / 1000,
		.tv_nsec = (java_milliseconds % 1000) * 1000 * 1000
	};
}

int main() {
	return 0;
}
~~~

HTML and CSS are web technologies.

Here's a citation.[^cite]

I also put a table in here for you.

| First cell | Second cell | Third cell
| --- | --- | --- | --- |
| First | Second | Third |
| First | Second | | Fourth |

---

Now let's look at some quotations.

> Here is a block quote.

Now let's do another.

> This block quote has multiple lines.
>
> We're having fun!
>
> --- Me, 2016

[^cite]: Hah, you thought that was going to go somewhere?

*[HTML]: Hella Textual Markup Language
*[CSS]: Cascading Swagger Sheets
