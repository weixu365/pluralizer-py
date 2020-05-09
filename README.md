## Why this project?

I have compared the following alternatives, and found https://github.com/blakeembrey/pluralize is the best one for me (most accurate), so ported it into Python world.
- TextBlob: https://github.com/sloria/TextBlob
- inflect: https://github.com/jazzband/inflect
- NLTK Wordnet: https://www.nltk.org/howto/wordnet.html

This repo is simply a Python port of https://github.com/blakeembrey/pluralize which has > 1.4m usages and 340k downloads per week when I evaluating different libraries.

## Installation
```
  pip install pluralizer
```

## Usage
```
    from pluralizer import Pluralizer
    pluralizer = Pluralizer()

    assert pluralizer.pluralize('apple', 1, false) == 'apple'
    assert pluralizer.pluralize('apple', 1, true) == '1 apple'
    assert pluralizer.pluralize('apple', 2, false) == 'apples'
    assert pluralizer.pluralize('apple', 2, true) == '2 apples'

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
