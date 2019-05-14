import os.path
from typing import Tuple
import re
import datetime as dt

from pdb import set_trace as bp
from pprint import pprint

MODULE_PATH = os.path.dirname(os.path.realpath(__file__))


def parse_file(path: str):
    full_path = os.path.join(MODULE_PATH, path)

    with open(full_path, 'r', encoding='utf-8-sig') as inp:
        content = inp.read()

    bad_sections = []
    notes = {}

    sections = content.split('==========')
    for enn, section in enumerate(sections):
        # Non-empty lines
        # line 1 - book title (author)
        # line 2 - highlight info
        # line 3 - highlighted text
        if not section or section == '\n':
            continue
        elif 'Your Highlight' in section:
            pass
        elif 'Your Bookmark' in section or 'Your Note' in section:
            continue
        else:
            bp()
            raise NotImplementedError(f'Unsupported note type: {section}')

        lines = [line for line in section.split('\n') if line]
        if len(lines) != 3:
            bad_sections.append(lines)
            continue

        # Title and author
        title_and_author_str = lines[0]  # regex: (?<=.)\(.+\)
        book_title, author_name = _parse_title_and_author_name(title_and_author_str)

        # Highlight info
        highlight_info_str = lines[1]
        location, time_added = _parse_highlight_info(highlight_info_str)

        # Highlighted text
        highlighted_text = lines[2]
        note_dict = {'location': location, 'time_added': time_added, 'highlighted_text': highlighted_text}

        if book_title in notes:
            notes[book_title]['notes'].append(note_dict)
        else:
            notes[book_title] = {'author': author_name, 'notes': []}

    return notes


def _parse_title_and_author_name(first_line: str) -> Tuple[str, str]:
    _author_bracket_index = first_line.rfind('(')  # find rightmost '(' in case book title contains '('
    author_name = first_line[_author_bracket_index:][1:-1].strip()

    book_title = first_line[:_author_bracket_index].strip()
    book_title = book_title.replace('\ufeff', '')  # todo - find better solution

    return book_title, author_name


def _parse_highlight_info(second_line: str) -> Tuple[str, dt.datetime]:
    location_str = re.findall('(?<=.location ).+(?= \|)', second_line)[0]
    _time_added_str = re.findall('(?<=.Added on ).+', second_line)[0]
    time_added = dt.datetime.strptime(_time_added_str, '%A, %d %B %Y %H:%M:%S')

    return location_str, time_added


def _parse_highlighted_text(third_line: str) -> str:
    return third_line.rstrip(',')
