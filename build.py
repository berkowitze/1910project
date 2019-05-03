import random
import csv
import os
import json
from jinja2 import Environment, FileSystemLoader, exceptions
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from collections import defaultdict

env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('index.jhtml')
mobile = env.get_template('mobile.jhtml')

arms = ["💪"]  # #  , "💪🏿", "💪🏼", "💪🏽", "💪🏾"]


@dataclass
class Course:
    code: str
    critical_review: str
    hours: str
    diff_n: int
    notes: str

    def __post_init__(self):
        self.difficulty = [random.choice(arms) for _ in range(self.diff_n)]
        min_name = self.code.replace(' ', '').lower()
        self.syllabus_link: Optional[str] = f'syllabi/{min_name}.pdf'
        if not os.path.exists(self.syllabus_link):
            self.syllabus_link = None

        self.link = f"courses/{min_name}.html"
        self.template_link = f"templates/{min_name}.jhtml"
        try:
            self.template = env.get_template(f'{min_name}.jhtml')
        except exceptions.TemplateNotFound:
            pass


topics: Dict[str, Tuple[str, List[Course]]] = {}
topic_descrs = json.load(open('topics.json'))
for line in csv.DictReader(open('courses.csv')):
    topic = line['Topic']
    if topic not in topics:
        raw_descr = topic_descrs[topic]
        topics[topic] = ('<br/>'.join(raw_descr.split('\n')), [])

    course = Course(line['Course'], line['CriticalReview'],
                    line['Hours'],
                    int(line['Difficulty']), line['Notes'])
    topics[topic][1].append(course)


def compile():
    rendered_index = template.render(topics=topics)
    rendered_mobile = mobile.render(topics=topics)

    with open('index.html', 'w') as f:
        f.write(rendered_index)

    with open('mobile.html', 'w') as f:
        f.write(rendered_mobile)

    for topic in topics:
        descr, courses = topics[topic]
        for course in courses:
            t = course.template.render(course=course)
            with open(course.link, 'w') as f:
                f.write(t)


def write_empty_files():
    # assert False, 'u sure tho, overwrites'
    base_template = open('templates/base.html').read()
    for topic in topics:
        descr, courses = topics[topic]
        for course in courses:
            with open(course.template_link, 'w') as f:
                f.write(base_template)

            course.__post_init__()


if __name__ == '__main__':
    # write_empty_files()
    compile()
    print('recompiled')
