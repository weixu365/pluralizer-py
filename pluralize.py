import re

# Rule storage - pluralize and singularize need to be run sequentially,
# while other rules can be optimized using an object for instant lookups.
pluralRules = []
singularRules = []
uncountables = {}
irregularPlurals = {}
irregularSingles = {}

# /**
#   * Sanitize a pluralization rule to a usable regular expression.
#   *
#   * @param  {(RegExp|string)} rule
#   * @return {RegExp}
#   */
def sanitizeRule (rule):
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
def restoreCase (word, token):
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

def interpolate (s, match):
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
def replace (word, rule):
  def replace_(match):
    result = interpolate(rule[1], match)

    if not match.lastindex:
      return restoreCase(word[match.endpos - 1], result)

    return restoreCase(match.group(0), result)
    
  return rule[0].sub(replace_, word)

# /**
#   * Sanitize a word by passing in the word and sanitization rules.
#   *
#   * @param  {string}   token
#   * @param  {string}   word
#   * @param  {Array}    rules
#   * @return {string}
#   */
def sanitizeWord (token, word, rules):
  # Empty string or doesn't need fixing.
  if ((not token) or token in uncountables):
    return word

  # Iterate over the sanitization rules and use the first one to match.
  for rule in reversed(rules):
    if rule[0].search(word):
      return replace(word, rule)
      
  return word

# /**
#   * Replace a word with the updated word.
#   *
#   * @param  {Object}   replaceMap
#   * @param  {Object}   keepMap
#   * @param  {Array}    rules
#   * @return {Function}
#   */
def replaceWord (replaceMap, keepMap, rules):
  def fun(word):
    # Get the correct token and case restoration functions.
    token = word.lower()

    # Check against the keep object map.
    if (token in keepMap):
      return restoreCase(word, token)

    # Check against the replacement map for a direct word replacement.
    if (token in replaceMap):
      return restoreCase(word, replaceMap[token])

    # Run all the rules against the word.
    return sanitizeWord(token, word, rules)

  return fun

# /**
#   * Check if a word is part of the map.
#   */
def checkWord (replaceMap, keepMap, rules, bool):
  def fun(word):
    token = word.lower()

    if (token in keepMap):
      return True
    if (token in replaceMap):
      return False

    return sanitizeWord(token, token, rules) == token
  
  return fun

# /**
#   * Pluralize or singularize a word based on the passed in count.
#   *
#   * @param  {string}  word      The word to pluralize
#   * @param  {number}  count     How many of the word exist
#   * @param  {boolean} inclusive Whether to prefix with the number (e.g. 3 ducks)
#   * @return {string}
#   */
# def pluralize (word, count, inclusive) {
#   pluralized = count == 1
#     ? pluralize.singular(word) : pluralize.plural(word)

#   return (inclusive ? count + ' ' : '') + pluralized
# }


  # /**
  #  * Pluralize a word.
  #  *
  #  * @type {Function}
  #  */
plural = replaceWord(irregularSingles, irregularPlurals, pluralRules)

  # /**
  #  * Check if a word is plural.
  #  *
  #  * @type {Function}
  #  */
# isPlural = checkWord(irregularSingles, irregularPlurals, pluralRules)

singular = replaceWord(irregularPlurals, irregularSingles, singularRules)

# /**
#   * Check if a word is singular.
#   *
#   * @type {Function}
#   */
# pluralize.isSingular = checkWord(
#   irregularPlurals, irregularSingles, singularRules
# )

# /**
#   * Add a pluralization rule to the collection.
#   *
#   * @param {(string|RegExp)} rule
#   * @param {string}          replacement
#   */
def addPluralRule(rule, replacement):
  pluralRules.append([sanitizeRule(rule), replacement])

# /**
#   * Add a singularization rule to the collection.
#   *
#   * @param {(string|RegExp)} rule
#   * @param {string}          replacement
#   */
def addSingularRule(rule, replacement):
  singularRules.append([sanitizeRule(rule), replacement])

# /**
#   * Add an uncountable word rule.
#   *
#   * @param {(string|RegExp)} word
#   */
def addUncountableRule(word):
  if isinstance(word, str):
    uncountables[word.lower()] = True
    return

  # Set singular and plural references for the word.
  addPluralRule(word, '$0')
  addSingularRule(word, '$0')

# /**
#   * Add an irregular word definition.
#   *
#   * @param {string} single
#   * @param {string} plural
#   */
def addIrregularRule(single, plural):
  plural = plural.lower()
  single = single.lower()

  irregularSingles[single] = plural
  irregularPlurals[plural] = single

# /**
#   * Irregular rules.
#   */
irregular_rules = [
  # Pronouns.
  ['I', 'we'],
  ['me', 'us'],
  ['he', 'they'],
  ['she', 'they'],
  ['them', 'them'],
  ['myself', 'ourselves'],
  ['yourself', 'yourselves'],
  ['itself', 'themselves'],
  ['herself', 'themselves'],
  ['himself', 'themselves'],
  ['themself', 'themselves'],
  ['is', 'are'],
  ['was', 'were'],
  ['has', 'have'],
  ['this', 'these'],
  ['that', 'those'],
  # Words ending in with a consonant and `o`.
  ['echo', 'echoes'],
  ['dingo', 'dingoes'],
  ['volcano', 'volcanoes'],
  ['tornado', 'tornadoes'],
  ['torpedo', 'torpedoes'],
  # Ends with `us`.
  ['genus', 'genera'],
  ['viscus', 'viscera'],
  # Ends with `ma`.
  ['stigma', 'stigmata'],
  ['stoma', 'stomata'],
  ['dogma', 'dogmata'],
  ['lemma', 'lemmata'],
  ['schema', 'schemata'],
  ['anathema', 'anathemata'],
  # Other irregular rules.
  ['ox', 'oxen'],
  ['axe', 'axes'],
  ['die', 'dice'],
  ['yes', 'yeses'],
  ['foot', 'feet'],
  ['eave', 'eaves'],
  ['goose', 'geese'],
  ['tooth', 'teeth'],
  ['quiz', 'quizzes'],
  ['human', 'humans'],
  ['proof', 'proofs'],
  ['carve', 'carves'],
  ['valve', 'valves'],
  ['looey', 'looies'],
  ['thief', 'thieves'],
  ['groove', 'grooves'],
  ['pickaxe', 'pickaxes'],
  ['passerby', 'passersby']
]

for rule in irregular_rules:
  addIrregularRule(rule[0], rule[1])

# /**
#   * Pluralization rules.
#   */
pluralization_rules = [
  [re.compile(r'(?i)s?$'), 's'],
  [re.compile(r'(?i)[^\u0000-\u007F]$'), '$0'],
  [re.compile(r'(?i)([^aeiou]ese)$'), '$1'],
  [re.compile(r'(?i)(ax|test)is$'), '$1es'],
  [re.compile(r'(?i)(alias|[^aou]us|t[lm]as|gas|ris)$'), '$1es'],
  [re.compile(r'(?i)(e[mn]u)s?$'), '$1s'],
  [re.compile(r'(?i)([^l]ias|[aeiou]las|[ejzr]as|[iu]am)$'), '$1'],
  
  [re.compile(r'(?i)(alumn|syllab|vir|radi|nucle|fung|cact|stimul|termin|bacill|foc|uter|loc|strat)(?:us|i)$'), '$1i'],
  [re.compile(r'(?i)(alumn|alg|vertebr)(?:a|ae)$'), '$1ae'],
  [re.compile(r'(?i)(seraph|cherub)(?:im)?$'), '$1im'],
  [re.compile(r'(?i)(her|at|gr)o$'), '$1oes'],
  [re.compile(r'(?i)(agend|addend|millenni|dat|extrem|bacteri|desiderat|strat|candelabr|errat|ov|symposi|curricul|automat|quor)(?:a|um)$'), '$1a'],
  [re.compile(r'(?i)(apheli|hyperbat|periheli|asyndet|noumen|phenomen|criteri|organ|prolegomen|hedr|automat)(?:a|on)$'), '$1a'],
  [re.compile(r'(?i)sis$'), 'ses'],
  [re.compile(r'(?i)(?:(kni|wi|li)fe|(ar|l|ea|eo|oa|hoo)f)$'), '$1$2ves'],
  [re.compile(r'(?i)([^aeiouy]|qu)y$'), '$1ies'],
  [re.compile(r'(?i)([^ch][ieo][ln])ey$'), '$1ies'],
  [re.compile(r'(?i)(x|ch|ss|sh|zz)$'), '$1es'],
  [re.compile(r'(?i)(matr|cod|mur|sil|vert|ind|append)(?:ix|ex)$'), '$1ices'],
  [re.compile(r'(?i)\b((?:tit)?m|l)(?:ice|ouse)$'), '$1ice'],
  [re.compile(r'(?i)(pe)(?:rson|ople)$'), '$1ople'],
  [re.compile(r'(?i)(child)(?:ren)?$'), '$1ren'],
  [re.compile(r'(?i)eaux$'), '$0'],
  [re.compile(r'(?i)m[ae]n$'), 'men'],
  ['thou', 'you']
]

for rule in pluralization_rules:
  addPluralRule(rule[0], rule[1])

# /**
#   * Singularization rules.
#   */
singularization_rules = [
  [re.compile(r'(?i)s$'), ''],
  [re.compile(r'(?i)(ss)$'), '$1'],
  [re.compile(r'(?i)(wi|kni|(?:after|half|high|low|mid|non|night|[^\w]|^)li)ves$'), '$1fe'],
  [re.compile(r'(?i)(ar|(?:wo|[ae])l|[eo][ao])ves$'), '$1f'],
  [re.compile(r'(?i)ies$'), 'y'],
  [re.compile(r'(?i)(dg|ss|ois|lk|ok|wn|mb|th|ch|ec|oal|is|ck|ix|sser|ts|wb)ies$'), '$1ie'],
  [re.compile(r'(?i)\b(l|(?:neck|cross|hog|aun)?t|coll|faer|food|gen|goon|group|hipp|junk|vegg|(?:pork)?p|charl|calor|cut)ies$'), '$1ie'],
  [re.compile(r'(?i)\b(mon|smil)ies$'), '$1ey'],
  [re.compile(r'(?i)\b((?:tit)?m|l)ice$'), '$1ouse'],
  [re.compile(r'(?i)(seraph|cherub)im$'), '$1'],
  [re.compile(r'(?i)(x|ch|ss|sh|zz|tto|go|cho|alias|[^aou]us|t[lm]as|gas|(?:her|at|gr)o|[aeiou]ris)(?:es)?$'), '$1'],
  [re.compile(r'(?i)(analy|diagno|parenthe|progno|synop|the|empha|cri|ne)(?:sis|ses)$'), '$1sis'],
  [re.compile(r'(?i)(movie|twelve|abuse|e[mn]u)s$'), '$1'],
  [re.compile(r'(?i)(test)(?:is|es)$'), '$1is'],
  [re.compile(r'(?i)(alumn|syllab|vir|radi|nucle|fung|cact|stimul|termin|bacill|foc|uter|loc|strat)(?:us|i)$'), '$1us'],
  [re.compile(r'(?i)(agend|addend|millenni|dat|extrem|bacteri|desiderat|strat|candelabr|errat|ov|symposi|curricul|quor)a$'), '$1um'],
  [re.compile(r'(?i)(apheli|hyperbat|periheli|asyndet|noumen|phenomen|criteri|organ|prolegomen|hedr|automat)a$'), '$1on'],
  [re.compile(r'(?i)(alumn|alg|vertebr)ae$'), '$1a'],
  [re.compile(r'(?i)(cod|mur|sil|vert|ind)ices$'), '$1ex'],
  [re.compile(r'(?i)(matr|append)ices$'), '$1ix'],
  [re.compile(r'(?i)(pe)(rson|ople)$'), '$1rson'],
  [re.compile(r'(?i)(child)ren$'), '$1'],
  [re.compile(r'(?i)(eau)x?$'), '$1'],
  [re.compile(r'(?i)men$'), 'man']
]

for rule in singularization_rules:
  addSingularRule(rule[0], rule[1])

# /**
#   * Uncountable rules.
#   */
uncountable_rules = [
  # Singular words with no plurals.
  'adulthood',
  'advice',
  'agenda',
  'aid',
  'aircraft',
  'alcohol',
  'ammo',
  'analytics',
  'anime',
  'athletics',
  'audio',
  'bison',
  'blood',
  'bream',
  'buffalo',
  'butter',
  'carp',
  'cash',
  'chassis',
  'chess',
  'clothing',
  'cod',
  'commerce',
  'cooperation',
  'corps',
  'debris',
  'diabetes',
  'digestion',
  'elk',
  'energy',
  'equipment',
  'excretion',
  'expertise',
  'firmware',
  'flounder',
  'fun',
  'gallows',
  'garbage',
  'graffiti',
  'hardware',
  'headquarters',
  'health',
  'herpes',
  'highjinks',
  'homework',
  'housework',
  'information',
  'jeans',
  'justice',
  'kudos',
  'labour',
  'literature',
  'machinery',
  'mackerel',
  'mail',
  'media',
  'mews',
  'moose',
  'music',
  'mud',
  'manga',
  'news',
  'only',
  'personnel',
  'pike',
  'plankton',
  'pliers',
  'police',
  'pollution',
  'premises',
  'rain',
  'research',
  'rice',
  'salmon',
  'scissors',
  'series',
  'sewage',
  'shambles',
  'shrimp',
  'software',
  'staff',
  'swine',
  'tennis',
  'traffic',
  'transportation',
  'trout',
  'tuna',
  'wealth',
  'welfare',
  'whiting',
  'wildebeest',
  'wildlife',
  'you',
  re.compile(r'(?i)pok[eé]mon$'),
  # Regexes.
  re.compile(r'(?i)[^aeiou]ese$'), # "chinese", "japanese"
  re.compile(r'(?i)deer$'), # "deer", "reindeer"
  re.compile(r'(?i)fish$'), # "fish", "blowfish", "angelfish"
  re.compile(r'(?i)measles$'),
  re.compile(r'(?i)o[iu]s$'), # "carnivorous"
  re.compile(r'(?i)pox$'), # "chickpox", "smallpox"
  re.compile(r'(?i)sheep$')
]
for rule in uncountable_rules:
  addUncountableRule(rule)
