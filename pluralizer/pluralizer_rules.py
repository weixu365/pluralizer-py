import re

#
# Irregular rules.
#
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
    re.compile(r'(?i)[^aeiou]ese$'),  # "chinese", "japanese"
    re.compile(r'(?i)deer$'),  # "deer", "reindeer"
    re.compile(r'(?i)fish$'),  # "fish", "blowfish", "angelfish"
    re.compile(r'(?i)measles$'),
    re.compile(r'(?i)o[iu]s$'),  # "carnivorous"
    re.compile(r'(?i)pox$'),  # "chickpox", "smallpox"
    re.compile(r'(?i)sheep$')
]
