## Why this project?
This repo is simply a Python port of https://github.com/blakeembrey/pluralize which has > 1.4m github usages and 3.5 million downloads per week when I evaluating different libraries.

> This module uses a pre-defined list of rules, applied in order, to singularize or pluralize a given word. There are many cases where this is useful, such as any automation based on user input. For applications where the word(s) are known ahead of time, you can use a simple ternary (or function) which would be a much lighter alternative.

I have compared the following alternatives, and found https://github.com/blakeembrey/pluralize is the best one for me (most accurate), so ported it into Python world.
- TextBlob: https://github.com/sloria/TextBlob
- inflect: https://github.com/jazzband/inflect
- NLTK Wordnet: https://www.nltk.org/howto/wordnet.html


## Installation
```bash
pip install pluralizer
```

## Usage
```python
from pluralizer import Pluralizer

pluralizer = Pluralizer()

assert pluralizer.pluralize('apple', 1, False) == 'apple'
assert pluralizer.pluralize('apple', 1, True) == '1 apple'
assert pluralizer.pluralize('apple', 2, False) == 'apples'
assert pluralizer.pluralize('apple', 2, True) == '2 apples'

assert pluralizer.plural('apple') == 'apples'
assert pluralizer.singular('apples') == 'apple'

assert pluralizer.isPlural('apples') == True
assert pluralizer.isPlural('apple') == False
assert pluralizer.isSingular('apples') == False
assert pluralizer.isSingular('apple') == True
```

## License
MIT

All credits to https://github.com/blakeembrey/pluralize. 
