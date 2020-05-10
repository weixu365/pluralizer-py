import re
from .pluralizer_rules import irregular_rules, pluralization_rules, singularization_rules, uncountable_rules


class Pluralizer:
    """This module uses a pre-defined list of rules, applied in order, to singularize or pluralize a given word.
    There are many cases where this is useful, such as any automation based on user input.

    Usage:
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
    """

    def __init__(self):
        # Rule storage - pluralize and singularize need to be run sequentially,
        # while other rules can be optimized using an object for instant lookups.
        self.pluralRules = []
        self.singularRules = []
        self.uncountables = {}
        self.irregularPlurals = {}
        self.irregularSingles = {}

        for rule in irregular_rules:
            self.addIrregularRule(rule[0], rule[1])

        for rule in pluralization_rules:
            self.addPluralRule(rule[0], rule[1])

        for rule in singularization_rules:
            self.addSingularRule(rule[0], rule[1])

        for rule in uncountable_rules:
            self.addUncountableRule(rule)

    def sanitizeRule(self, rule):
        """Sanitize a pluralization rule to a usable regular expression.

         @param  {(Pattern|string)} rule
         @return {Pattern}
        """
        if isinstance(rule, str):
            return re.compile('(?i)^' + rule + '$')

        return rule

    def restoreCase(self, word, token):
        """Pass in a word token to produce a function that can replicate the case on another word.

          @param  {string}   word
          @param  {string}   token
          @return string of {token} following the same case of {word}
        """
        # Tokens are an exact match.
        if word == token:
            return token

        # Lower cased words. E.g. "hello".
        if (word == word.lower()):
            return token.lower()

        # Upper cased words. E.g. "WHISKY".
        if (word == word.upper()):
            return token.upper()

        # Title cased words. E.g. "Title".
        if (word[0] == word[0].upper()):
            return token[0].upper() + token[1:].lower()

        # Lower cased words. E.g. "test".
        return token.lower()

    def interpolate(self, s, match):
        """Interpolate a regexp string.

          @param  {string} str
          @param  {Array}  args
          @return {string}
        """
        def replace_rest(sub_match):
            return match.group(int(sub_match.group(1))) or ''
        return re.sub(r'\$(\d{1,2})', replace_rest, s)

    def replace(self, word, rule):
        """Replace a word using a rule.

          @param  {string} word
          @param  {Array}  rule
          @return {string}
        """
        def replace_(match):
            result = self.interpolate(rule[1], match)

            matched_start, matched_end = match.span()
            if matched_end == matched_start:
                return self.restoreCase(word[matched_start - 1], result)

            return self.restoreCase(match.group(0), result)

        return rule[0].sub(replace_, word, 1)

    def sanitizeWord(self, token, word, rules):
        """Sanitize a word by passing in the word and sanitization rules.

          @param  {string}   token
          @param  {string}   word
          @param  {Array}    rules
          @return {string}
        """
        # Empty string or doesn't need fixing.
        if ((not token) or token in self.uncountables):
            return word

        # Iterate over the sanitization rules and use the first one to match.
        for rule in reversed(rules):
            if rule[0].search(word):
                return self.replace(word, rule)

        return word

    def replaceWord(self, replaceMap, keepMap, rules, word):
        """Replace a word with the updated word.

          @param  {Object}   replaceMap
          @param  {Object}   keepMap
          @param  {Array}    rules
          @return string
        """
        # Get the correct token and case restoration functions.
        token = word.lower()

        # Check against the keep object map.
        if (token in keepMap):
            return self.restoreCase(word, token)

        # Check against the replacement map for a direct word replacement.
        if (token in replaceMap):
            return self.restoreCase(word, replaceMap[token])

        # Run all the rules against the word.
        return self.sanitizeWord(token, word, rules)

    def checkWord(self, replaceMap, keepMap, rules, word):
        """Check if a word is part of the map."""
        token = word.lower()

        if (token in keepMap):
            return True
        if (token in replaceMap):
            return False

        return self.sanitizeWord(token, token, rules) == token

    def pluralize(self, word, count=None, inclusive=False):
        """Pluralize or singularize a word based on the passed in count.

          @param  {string}  word      The word to pluralize
          @param  {number}  count     How many of the word exist
          @param  {boolean} inclusive Whether to prefix with the number (e.g. 3 ducks)
          @return {string}
        """
        pluralized = self.singular(word) if count == 1 else self.plural(word)

        return (str(count) + ' ' if inclusive else '') + pluralized

    def plural(self, word):
        """Pluralize a word.

          @return string of plural form of the word
        """
        return self.replaceWord(self.irregularSingles, self.irregularPlurals, self.pluralRules, word)

    def isPlural(self, word):
        """Check if a word is plural.

          @return True if the word is plural else False
        """
        return self.checkWord(self.irregularSingles, self.irregularPlurals, self.pluralRules, word)

    def singular(self, word):
        """Singular a word.

          @return string of singular form of the word
        """
        return self.replaceWord(self.irregularPlurals, self.irregularSingles, self.singularRules, word)

    def isSingular(self, word):
        """Check if a word is singular.

          @return True if the word is singular else False
        """
        return self.checkWord(self.irregularPlurals, self.irregularSingles, self.singularRules, word)

    def addPluralRule(self, rule, replacement):
        """Add a pluralization rule to the collection.

          @param {(string|RegExp)} rule
          @param {string}          replacement
        """
        self.pluralRules.append([self.sanitizeRule(rule), replacement])

    def addSingularRule(self, rule, replacement):
        """Add a singularization rule to the collection.

          @param {(string|RegExp)} rule
          @param {string}          replacement
        """
        self.singularRules.append([self.sanitizeRule(rule), replacement])

    def addUncountableRule(self, word):
        """Add an uncountable word rule.

          @param {(string|RegExp)} word
        """
        if isinstance(word, str):
            self.uncountables[word.lower()] = True
            return

        # Set singular and plural references for the word.
        self.addPluralRule(word, '$0')
        self.addSingularRule(word, '$0')

    def addIrregularRule(self, single, plural):
        """Add an irregular word definition.

          @param {string} single
          @param {string} plural
        """
        plural = plural.lower()
        single = single.lower()

        self.irregularSingles[single] = plural
        self.irregularPlurals[plural] = single
