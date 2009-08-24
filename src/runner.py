from pyhistorian import Story, Scenario
from story_parser import parse_text


class StoryRunner(object):
    def __init__(self, story_text, output, colored, modules=[]):
        self._story_text = story_text
        self._output = output
        self._modules = modules
        self._colored = colored
        self._parsed_story = parse_text(story_text)
        self._pycukes_story = self._get_pycukes_story()
        self._all_givens = {}
        self._all_whens = {}
        self._all_thens = {}
        self._collect_steps()

    def _collect_steps(self):
        for module in self._modules:
            for step_name in ['given', 'when', 'then']:
                steps = getattr(module, '_%ss' % step_name, [])
                for method, message, args in steps:
                    all_this_step = getattr(self, '_all_%ss' % step_name)
                    all_this_step[message] = (method, args)

    def _get_header(self):
        story = self._parsed_story.get_stories()[0]
        return story.header

    def _get_pycukes_story(self):
        return type('PyCukesStory',
                    (Story,),
                    {'__doc__' :'\n'.join(self._get_header().split('\n')[1:]),
                     'output': self._output,
                     'title': self._parsed_story.get_stories()[0].title,
                     'colored': self._colored,
                     'scenarios': [],
                     'template_color':'yellow'})

    def run(self):
        scenarios = self._parsed_story.get_stories()[0].scenarios
        for scenario_title, steps in scenarios:
            new_scenario = type('PyCukesScenario',
                                (Scenario,),
                                {'__doc__': scenario_title,
                                '_givens': [],
                                '_whens': [],
                                '_thens': [],
                                })

            for step_name in ['given', 'when', 'then']:
                for step_message in steps[step_name]:
                    scenario_steps = getattr(new_scenario, '_%ss' % step_name)
                    all_runner_steps = getattr(self, '_all_%ss' % step_name)
                    if step_message not in all_runner_steps:
                        scenario_steps.append( (None, step_message, ()) )
                    for step_regex, (step_method, step_args) in all_runner_steps.items():
                        if step_message == step_regex:
                            scenario_steps.append( (step_method, step_message, step_args) )
 
            self._pycukes_story.scenarios.append(new_scenario)
        self._pycukes_story.run()
