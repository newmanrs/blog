---
title: "Python Safety"
date: 2018-03-07T16:39:32-08:00
draft: True
---

Warning: Post requires some knowledge of programming with python.  Skip otherwise.

Every now and then I feel the urge to try to make my python scripts more gracefully validate inputs without descending into an entirely unfortunate mindless snarl. Here's one such approach.

<!--more-->

So it came to pass I wanted to at least assert when parsing large amounts of irregular data from irregular sources^[I work at a hospital.  There is no data curation.].  And in general I loathe software that runs on nothing but dictionaries where you can't easily understand the program's control flow by reading it.  Codebases like this seem common since academics know nothing of software engineering, so I propose actually defining classes instead of an unfortunate snarl of manual checking using `isinstance`, `haskey` or `hasattr`.

I also like code that ties my hands, and other user's hands as much as possible. Schemaless and typeless seems so great until you remember how fragile the results are.

So here we are introducing my container class, which is pulling from collections.MutableMapping which forces me to implement enough abstract methods.  Setting the `metaclass = abc.ABCMeta` allows me to define more abstact methods that must be overwritten.  This is some classic object oriented programming that I rarely have seen in python scripts built by academics.  It would have been nice if I could use the `abc.ABCMeta` and derive from type `dict`, but this does not appear to work in `python3.6.4`.

```python

class Container(collections.MutableMapping, metaclass = abc.ABCMeta):
    def __init__(self,*args, **kwargs):

        if not self._required_kwargs() <= kwargs.keys():
            msg = "Received kwargs {}, require kwargs {}".format(
                kwargs.keys(),
                self._required_kwargs())
            raise AttributeError(msg)
        self.__dict__.update(*args, **kwargs)

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __str__(self):
        return str(self.__dict__)

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, key):
        return self.__dict__[key]

    def __delitem__(self, key):
        """ Check key requirements before deletion """
        if not key in self._required_kwargs():
            del self.__dict__[key]
        else:
            msg = "Cannot delete required key {}, required keys {}".format(
                key,
                self._required_kwargs())
        raise RuntimeError(msg);

    @abc.abstractmethod
    def _required_kwargs(self):
        """ Replace this prototype """
        required_kwargs = set([])
        return required_kwargs

```

Then implementations of concrete classes that derive this now have to override the abstract method `_required_kwargs`  to contain the required keywords.  Failure to do so will cause an exception upon construction.  An example concrete class is given as:

```python
class StateSpace(Container):

    def _required_kwargs(self):
        return set(['name','ordered_values','unordered_values'])
```

To use these we can just build and feed in dictionaries using python's periodically nifty kwargs:

```python
    d = dict()
    d['name'] = 'whatever'
    d['ordered_values'] = [1,2,3]
    d['unordered_values'] = ['a','b']
    d['cruft'] = 'someextrastuff'
    s = StateSpace(**d)
```

and the resulting class behaves like a dictionary except that you cannot remove required keys.

I've found this to give myself a reasonable bit of safety, for not too much effort.  I think having named dictionary types with a set of keys (shown here) is nice, but mandating both keys, and the type of the keys is pretty easy to add as well.

This simple pattern seems to do a good job of balancing the desire for adding type safety to a project after doing the initial prototyping without having to do significant rewrites.

But perhaps trying to validate in python is foolish.  It sure is a lot of initial boilerplate to do so.  
