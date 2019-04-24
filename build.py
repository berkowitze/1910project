from jinja2 import Environment, FileSystemLoader
from dataclasses import dataclass
from typing import List

env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('index.jhtml')


@dataclass
class Course:
    code: str = 'Place'
    critical_review: str = 'hi'
    old_syllabus: str = 'hi'
    hours: float = 3.5
    difficulty: int = 2
    notes: str = 'hello there'


@dataclass
class Topic:
    description: str
    courses: List[Course]


calc1 = Topic('Intro calc', [Course(), Course(), Course()])

topics = [calc1, calc1]

rendered_template = template.render(topics=topics)

with open('index.html', 'w') as f:
    f.write(rendered_template)


print('recompiled')
