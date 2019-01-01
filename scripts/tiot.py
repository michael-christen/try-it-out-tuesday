#!/usr/bin/env python
"""
Used to convert csv of tiot experiences into an auto-generated directory of
blog posts.

> python scripts/tiot.py < scripts/tiot.csv
"""
import csv
import sys
import glob


def main():
    reader = csv.DictReader(sys.stdin)
    tiots = []
    for tiot in reader:
        tiots.append(tiot)
    # Look at images
    image_paths = glob.glob('content/blog/auto-generated/pics/IMG_*.jpg')
    date2path = {}
    for path in image_paths:
        raw_date = path.split('_')[1]
        year = raw_date[:4]
        month = raw_date[4:6]
        day = raw_date[6:]
        formatted_date = '{}-{}-{}'.format(year, month, day)
        date2path[formatted_date] = path
    used_images = set()
    for tiot in tiots:
        slug = tiot['name'].replace(' ', '-').replace('/', 'or').lower()
        month, day, year = tiot['date'].split('/')
        month = int(month)
        day = int(day)
        year = int(year)
        date = '{year:04d}-{month:02d}-{day:02d}'.format(year=year, month=month, day=day)
        image_path = date2path.get(date)
        if image_path:
            optional_image_spec = '\nfeaturedImage: ./pics/{}'.format(
                image_path.split('/')[-1])
            used_images.add(date)
        else:
            optional_image_spec = '\nfeaturedImage: ./pics/blank.jpg'
        description = tiot['description']
        if not description:
            description = "No description provided yet."
        with open('content/blog/auto-generated/{slug}.md'
                  .format(slug=slug), 'w') as f:
            f.write('''
---
title: {name}
date: '{date}'{opt_image}
---

{description}
'''.format(name=tiot['name'], date=date, description=description,
           opt_image=optional_image_spec,
          ).strip()+'\n')


if __name__ == '__main__':
    main()

