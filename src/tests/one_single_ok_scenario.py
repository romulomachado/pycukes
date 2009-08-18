'''
    >>> StoryRunner(story_text,
    ...             output=output,
    ...             with_colors=False,
    ...             modules=[sum_of_one_and_two_with_three_oks]).run()
    >>> print output.getvalue()
    Story: Calculator
    As a math student
    I want to use a calculator
    So that my calculations can be easy to do
    <BLANKLINE>
    Scenario 1: Sum of 1 and 2
      Given I have a calculator   ... OK
      When I enter with 1 + 2 and press =   ... OK
      Then I see 3 in my LCD   ... OK
    <BLANKLINE>
'''

from pycukes import StoryRunner
from cStringIO import StringIO
from scenarios import sum_of_one_and_two_with_three_oks


output = StringIO()
story_text = """Story: Calculator
                As a math student
                I want to use a calculator
                So that my calculations can be easy to do
                
                Scenario 1: Sum of 1 and 2
                  Given I have a calculator
                  When I enter with 1 + 2 and press =
                  Then I see 3 in my LCD"""
