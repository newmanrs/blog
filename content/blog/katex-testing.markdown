+++
title = "Katex, Tables, Codeblock testing"
date = 2018-01-04T14:26:24-08:00
categories = ["Katex", "Syntax Highlighting"]
+++

Someday I'll try to find the time to actually write some real content here.  Mostly testing different blog features here.
$$ x = {-b \pm \sqrt{b^2-4ac} \over 2a} $$

It works!

<!--more-->
---------------------------------------

## Checking some basic code highlighting:  Python

```python
import sqrt

if __name__ == "__main__":
    print(sqrt(2))
    print("Hello World");
```

## HTML syntax test

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.13.1/languages/julia.min.js" integrity="sha256-DLro//cZeKoh2+YDxAxfvvEpSUByFKPpE9z9b9k6aIc=" crossorigin="anonymous"></script>
```

## Latex syntax test

Note:  This is not standard in highlight.min.js, and needs to be added somewhere in the external scripts within the templates wherever the rest of highlight.js is.

```tex
\begin{equation} x = {-b \pm \sqrt{b^2-4ac} \over 2a} \end{equation}
```

## Json syntax test

```json
{
    foo : "bar",
    bar : "foo"
}
```

## Haskell syntax highlighting test:

```haskell
fibcase n =
  case n of
    0 -> 1
    1 -> 1
    _ -> fibcase (n-1) + fibcase (n-2)
```
## Bash


```

dpi=300.0
xdim=6.5  #Inches
ydim=9.0  #Inches
xpx=$(expr $dpi*$xdim | bc)  #Bash can't natively multiply floats.  Okay.
ypx=$(expr $dpi*$ydim | bc)
#If there are originals starting w/ name image process them
for file in $@; do
    echo "convert $file -resize ${xpx}x$ypx fitpage$file;"
    convert $file -resize ${xpx}x$ypx fitpage$file;
done 
```


## Tables test with katex:

|  Item  | Cost   | Date   |
|:----------:|:------------:|:------------:|
| Apple | $1.50 | 24 Jan 2018 |
| Orange | $2 | 24 Jan 2018 |
| Banana | $0.60 | 24 Jan 2018 |
| Tomato | $$ \$\sqrt{2} $$ | 24 Jan 2018 |

Katex does work within tables, but for some reason the equation will be center-aligned even if the markdown table's column asks for left alignment.  That's workable, but... incorrect.  Sigh.  Some day auto-generating everything will have sane behaviour.

