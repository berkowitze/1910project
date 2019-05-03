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
        if not os.path.exists(self.syllabus_link):
            self.syllabus_link = None

        self.link = f"courses/{min_name}.html"
        self.content_link = f"content/{min_name}.jhtml"


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
            t = course_template.render(course=course)
            with open(course.link, 'w') as f:
                f.write(t)


if __name__ == '__main__':
    compile()
    print('recompiled')
