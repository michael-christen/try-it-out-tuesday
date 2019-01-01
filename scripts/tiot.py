#!/usr/bin/env python
"""
Used to convert csv of tiot experiences into an auto-generated directory of
blog posts.

> python scripts/tiot.py < scripts/tiot.csv
"""
import csv
import sys


def main():
    reader = csv.DictReader(sys.stdin)
    for tiot in reader:
        slug = tiot['name'].replace(' ', '-').replace('/', 'or').lower()
        month, day, year = tiot['date'].split('/')
        month = int(month)
        day = int(day)
        year = int(year)
        date = '{year:04d}-{month:02d}-{day:02d}'.format(year=year, month=month, day=day)
        description = tiot['description']
        if not description:
            description = "No description provided yet."
        with open('content/blog/auto-generated/{slug}.md'
                  .format(slug=slug), 'w') as f:
            f.write('''
---
title: {name}
date: '{date}'
---

{description}
'''.format(name=tiot['name'], date=date, description=description).strip()+'\n')


if __name__ == '__main__':
    main()

