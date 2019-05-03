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
course_template = env.get_template('course.jhtml')


class Course:
    def __init__(self, code: str, cr: str,
                 hours: str, difficulty: int, notes: str) -> None:
        self.code: str = code
        min_name = self.code.replace(' ', '').lower()

        self.critical_review: str = cr
        self.hours: str = hours
        self.diff_n: int = difficulty
        self.notes: str = notes
        self.difficulty = ["💪" for _ in range(self.diff_n)]

        self.syllabus_link: Optional[str] = f'syllabi/{min_name}.pdf'
        if not os.path.exists(f'out/{self.syllabus_link}'):
            self.syllabus_link = None

        self.link = f"courses/{min_name}.html"
        self.content_link = f"content/{min_name}.jhtml"


class Topic:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.mini_name = self.name.replace(' ', '').lower()
        self.courses: List[Course] = []
        self.content_link = f"topics/{self.mini_name}.jhtml"


topics: Dict[str, Topic] = {}
for line in csv.DictReader(open('courses.csv')):
    topic_name = line['Topic']
    if topic_name not in topics:
        topics[topic_name] = Topic(topic_name)

    course = Course(line['Course'], line['CriticalReview'],
                    line['Hours'],
                    int(line['Difficulty']), line['Notes'])
    topics[topic_name].courses.append(course)


def compile():
    rendered_index = template.render(topics=topics)
    rendered_mobile = mobile.render(topics=topics)

    with open('out/index.html', 'w') as f:
        f.write(rendered_index)

    with open('out/mobile.html', 'w') as f:
        f.write(rendered_mobile)

    for topic in topics:
        for course in topics[topic].courses:
            t = course_template.render(course=course)
            with open(f'out/{course.link}', 'w') as f:
                f.write(t)


if __name__ == '__main__':
    compile()
    print('recompiled')
