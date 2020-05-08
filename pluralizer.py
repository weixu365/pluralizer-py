import re
from pluralizer_rules import irregular_rules, pluralization_rules, singularization_rules, uncountable_rules

class Pluralizer:
  # Rule storage - pluralize and singularize need to be run sequentially,
  # while other rules can be optimized using an object for instant lookups.

  def __init__(self):
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

  # /**
  #   * Sanitize a pluralization rule to a usable regular expression.
  #   *
  #   * @param  {(RegExp|string)} rule
  #   * @return {RegExp}
  #   */
  def sanitizeRule(self, rule):
    if isinstance(rule, str):
      return re.compile('(?i)^' + rule + '$')

    return rule

  # /**
  #   * Pass in a word token to produce a function that can replicate the case on
  #   * another word.
  #   *
  #   * @param  {string}   word
  #   * @param  {string}   token
  #   * @return {Function}
  #   */
  def restoreCase(self, word, token):
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

  # /**
  #   * Interpolate a regexp string.
  #   *
  #   * @param  {string} str
  #   * @param  {Array}  args
  #   * @return {string}
  #   */

  def interpolate(self, s, match):
    def replace_rest(sub_match):
      return match.group(int(sub_match.group(1))) or ''
    return re.sub(r'\$(\d{1,2})', replace_rest, s)

  # /**
  #   * Replace a word using a rule.
  #   *
  #   * @param  {string} word
  #   * @param  {Array}  rule
  #   * @return {string}
  #   */
  def replace(self, word, rule):
    def replace_(match):
      result = self.interpolate(rule[1], match)

      matched_start, matched_end = match.span()
      if matched_end == matched_start:
        return self.restoreCase(word[matched_start - 1], result)

      return self.restoreCase(match.group(0), result)
      
    return rule[0].sub(replace_, word, 1)

  # /**
  #   * Sanitize a word by passing in the word and sanitization rules.
  #   *
  #   * @param  {string}   token
  #   * @param  {string}   word
  #   * @param  {Array}    rules
  #   * @return {string}
  #   */
  def sanitizeWord(self, token, word, rules):
    # Empty string or doesn't need fixing.
    if ((not token) or token in self.uncountables):
      return word

    # Iterate over the sanitization rules and use the first one to match.
    for rule in reversed(rules):
      if rule[0].search(word):
        return self.replace(word, rule)
        
    return word

  # /**
  #   * Replace a word with the updated word.
  #   *
  #   * @param  {Object}   replaceMap
  #   * @param  {Object}   keepMap
  #   * @param  {Array}    rules
  #   * @return {Function}
  #   */
  def replaceWord(self, replaceMap, keepMap, rules, word):
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

  # /**
  #   * Check if a word is part of the map.
  #   */
  def checkWord(self, replaceMap, keepMap, rules, word):
    token = word.lower()

    if (token in keepMap):
      return True
    if (token in replaceMap):
      return False

    return self.sanitizeWord(token, token, rules) == token
    
  # /**
  #   * Pluralize or singularize a word based on the passed in count.
  #   *
  #   * @param  {string}  word      The word to pluralize
  #   * @param  {number}  count     How many of the word exist
  #   * @param  {boolean} inclusive Whether to prefix with the number (e.g. 3 ducks)
  #   * @return {string}
  #   */
  def pluralize(self, word, count=None, inclusive=False):
    pluralized = self.singular(word) if count == 1 else self.plural(word)

    return (str(count) + ' ' if inclusive else '') + pluralized


    # /**
    #  * Pluralize a word.
    #  *
    #  * @type {Function}
    #  */
  def plural(self, word):
    return self.replaceWord(self.irregularSingles, self.irregularPlurals, self.pluralRules, word)

    # /**
    #  * Check if a word is plural.
    #  *
    #  * @type {Function}
    #  */
  def isPlural(self, word):
    return self.checkWord(self.irregularSingles, self.irregularPlurals, self.pluralRules, word)

  def singular(self, word):
    return self.replaceWord(self.irregularPlurals, self.irregularSingles, self.singularRules, word)

  # /**
  #   * Check if a word is singular.
  #   *
  #   * @type {Function}
  #   */
  def isSingular(self, word):
    return self.checkWord(self.irregularPlurals, self.irregularSingles, self.singularRules, word)

  # /**
  #   * Add a pluralization rule to the collection.
  #   *
  #   * @param {(string|RegExp)} rule
  #   * @param {string}          replacement
  #   */
  def addPluralRule(self, rule, replacement):
    self.pluralRules.append([self.sanitizeRule(rule), replacement])

  # /**
  #   * Add a singularization rule to the collection.
  #   *
  #   * @param {(string|RegExp)} rule
  #   * @param {string}          replacement
  #   */
  def addSingularRule(self, rule, replacement):
    self.singularRules.append([self.sanitizeRule(rule), replacement])

  # /**
  #   * Add an uncountable word rule.
  #   *
  #   * @param {(string|RegExp)} word
  #   */
  def addUncountableRule(self, word):
    if isinstance(word, str):
      self.uncountables[word.lower()] = True
      return

    # Set singular and plural references for the word.
    self.addPluralRule(word, '$0')
    self.addSingularRule(word, '$0')

  # /**
  #   * Add an irregular word definition.
  #   *
  #   * @param {string} single
  #   * @param {string} plural
  #   */
  def addIrregularRule(self, single, plural):
    plural = plural.lower()
    single = single.lower()

    self.irregularSingles[single] = plural
    self.irregularPlurals[plural] = single
