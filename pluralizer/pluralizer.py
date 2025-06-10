import re
from typing import Tuple

from .pluralizer_rules import irregular_rules, pluralization_rules, singularization_rules, uncountable_rules

IrregularSingles = dict[str, str]
IrregularPlurals = dict[str, str]
SingularRule = Tuple[re.Pattern[str], str]
PluralRule = Tuple[re.Pattern[str], str]


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

        assert pluralizer.is_plural('apples') == True
        assert pluralizer.is_plural('apple') == False
        assert pluralizer.is_singular('apples') == False
        assert pluralizer.is_singular('apple') == True
    """

    def __init__(self):
        super().__init__()

        # Rule storage - pluralize and singularize need to be run sequentially,
        # while other rules can be optimized using an object for instant lookups.
        self.pluralRules: list[PluralRule] = []
        self.singularRules: list[SingularRule] = []
        self.uncountables: dict[str, bool] = {}
        self.irregularPlurals: IrregularPlurals = {}
        self.irregularSingles: IrregularSingles = {}

        for single, plural in irregular_rules:
            self.add_irregular_rule(single, plural)

        for pattern, replacement in pluralization_rules:
            self.add_plural_rule(pattern, replacement)

        for pattern, replacement in singularization_rules:
            self.add_singular_rule(pattern, replacement)

        for pattern in uncountable_rules:
            self.add_uncountable_rule(pattern)

    def _sanitize_rule(self, rule: str | re.Pattern[str]) -> re.Pattern[str]:
        """Sanitize a pluralization rule to a usable regular expression."""
        if isinstance(rule, str):
            return re.compile("(?i)^" + rule + "$")

        return rule

    def _restore_case(self, word: str, token: str) -> str:
        """Pass in a word token to produce a function that can replicate the case on another word."""
        # Tokens are an exact match.
        if word == token:
            return token

        # Lower cased words. E.g. "hello".
        if word == word.lower():
            return token.lower()

        # Upper cased words. E.g. "WHISKY".
        if word == word.upper():
            return token.upper()

        # Title cased words. E.g. "Title".
        if word[0] == word[0].upper():
            return token[0].upper() + token[1:].lower()

        # Lower cased words. E.g. "test".
        return token.lower()

    def _interpolate(self, s: str, match: re.Match[str]) -> str:
        """Interpolate a regexp string."""

        def replace_rest(sub_match: re.Match[str]):
            return match.group(int(sub_match.group(1))) or ""

        return re.sub(r"\$(\d{1,2})", replace_rest, s)

    def _replace(self, word: str, pattern: re.Pattern[str], replacement: str) -> str:
        """Replace a word using a rule."""

        def replace_(match: re.Match[str]) -> str:
            result = self._interpolate(replacement, match)

            matched_start, matched_end = match.span()
            if matched_end == matched_start:
                return self._restore_case(word[matched_start - 1], result)

            return self._restore_case(match.group(0), result)

        return pattern.sub(replace_, word, 1)

    def _sanitize_word(self, token: str, word: str, rules: list[SingularRule] | list[PluralRule]) -> str:
        """Sanitize a word by passing in the word and sanitization rules."""
        # Empty string or doesn't need fixing.
        if (not token) or token in self.uncountables:
            return word

        # Iterate over the sanitization rules and use the first one to match.
        for pattern, replacement in reversed(rules):
            if pattern.search(word):
                return self._replace(word, pattern, replacement)

        return word

    def _replace_word(
        self,
        replaceMap: IrregularSingles | IrregularPlurals,
        keepMap: IrregularSingles | IrregularPlurals,
        rules: list[SingularRule] | list[PluralRule],
        word: str,
    ) -> str:
        """Replace a word with the updated word."""
        # Get the correct token and case restoration functions.
        token = word.lower()

        # Check against the keep object map.
        if token in keepMap:
            return self._restore_case(word, token)

        # Check against the replacement map for a direct word replacement.
        if token in replaceMap:
            return self._restore_case(word, replaceMap[token])

        # Run all the rules against the word.
        return self._sanitize_word(token, word, rules)

    def _check_word(
        self,
        replaceMap: IrregularSingles | IrregularPlurals,
        keepMap: IrregularSingles | IrregularPlurals,
        rules: list[SingularRule] | list[PluralRule],
        word: str,
    ) -> bool:
        """Check if a word is part of the map."""
        token = word.lower()

        if token in keepMap:
            return True
        if token in replaceMap:
            return False

        return self._sanitize_word(token, token, rules) == token

    def pluralize(self, word: str, count: int | None = None, inclusive: bool = False) -> str:
        """Pluralize or singularize a word based on the passed in count.

        Args:
            word: str: The word to pluralize
            count: int | None: How many of the word exist
            inclusive: bool: Whether to prefix with the number (e.g. 3 ducks)

        Returns:
            str: The pluralized or singularized word, optionally prefixed with the count.
        """
        pluralized = self.singular(word) if count == 1 else self.plural(word)

        return (str(count) + " " if inclusive else "") + pluralized

    def plural(self, word: str) -> str:
        """Pluralize a word."""
        return self._replace_word(self.irregularSingles, self.irregularPlurals, self.pluralRules, word)

    def is_plural(self, word: str) -> bool:
        """Check if a word is plural."""
        return self._check_word(self.irregularSingles, self.irregularPlurals, self.pluralRules, word)

    def singular(self, word: str) -> str:
        """Singular a word."""
        return self._replace_word(self.irregularPlurals, self.irregularSingles, self.singularRules, word)

    def is_singular(self, word: str):
        """Check if a word is singular."""
        return self._check_word(self.irregularPlurals, self.irregularSingles, self.singularRules, word)

    def add_plural_rule(self, rule: str | re.Pattern[str], replacement: str) -> None:
        """Add a pluralization rule to the collection."""
        self.pluralRules.append((self._sanitize_rule(rule), replacement))

    def add_singular_rule(self, rule: str | re.Pattern[str], replacement: str) -> None:
        """Add a singularization rule to the collection."""
        self.singularRules.append((self._sanitize_rule(rule), replacement))

    def add_uncountable_rule(self, word: str | re.Pattern[str]) -> None:
        """Add an uncountable word rule."""
        if isinstance(word, str):
            self.uncountables[word.lower()] = True
            return

        # Set singular and plural references for the word.
        self.add_plural_rule(word, "$0")
        self.add_singular_rule(word, "$0")

    def add_irregular_rule(self, single: str, plural: str) -> None:
        """Add an irregular word definition."""
        plural = plural.lower()
        single = single.lower()

        self.irregularSingles[single] = plural
        self.irregularPlurals[plural] = single
