# coding: utf-8

"""IPA v2 front-end views."""

from error import Error
from home import Home
from judge_aea import JudgeAea
from judge_ipa import JudgeIpa

# This is here to get PyFlakes to stop complaining about unused imports
__all__ = [
    'Error',
    'Home',
    'JudgeAea',
    'JudgeIpa',
]
