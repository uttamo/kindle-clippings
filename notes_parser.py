import os.path
from pathlib import Path
from typing import Tuple
import datetime as dt
import re
# TODO why not Path.cwd()?
MODULE_DIR = os.path.dirname(os.path.realpath(__file__))


def parse_file(path: str) -> dict:
    "Given a clippings.txt file return a dictionary in the following form\
    dict[bookTitle][notes/highlights/bookmarks][], where \
    1. bookTitle, simple string\
    2. notes/highlights/bookmarks, simple string, type of note\
    3. ctype_dict: location, time_added, highlighted_text"
    # TODO perform path check
    full_path = os.path.join(MODULE_DIR, path)

    with open(full_path, 'r', encoding='utf-8-sig') as clippings_file:
        content = clippings_file.read()

    _unsuitable_sections = []
    notes_data = {}
    _highlights = {}

    sections = content.split('==========')
    for section in sections:
        if not section or section == '\n':
            continue
        elif 'Your Highlight' in section or 'Your Note' in section:
        # TODO Notes should be linked with highlights most of the time, for now, just differentiating
            pass
        elif 'Your Bookmark' in section:
            ctype =  'bookmark'
            continue
        else:
            raise NotImplementedError(f'Unsupported note type: {section}')

        lines = [line for line in section.split('\n') if line]
        if len(lines) != 3:
            _unsuitable_sections.append(lines)
            continue

        # Non-empty lines
        # line 1 - book title (author)
        # line 2 - highlight info
        # line 3 - highlighted text
        # Title and author
        book_title, author_name = parse_title_and_author_name(lines[0])
        location, time_added = parse_highlight_info(lines[1])
        highlighted_text = lines[2]

        # Sometimes the clippings file has duplicated notes, so we need to check if a particular note has already been
        # encountered
        existing_highlights_for_author = _highlights.get(book_title, [])

        # TODO, fix the naming standards here, highlights and notes are not the same
        # TODO, fix the dictionary structure here, I think it can be improved ( to allow for quicklier searching and grouping )
        #       - instead of title first, author first maybe?
        if highlighted_text in existing_highlights_for_author:
            continue
        else:
            if book_title in _highlights:
                _highlights[book_title].append(highlighted_text)
            else:
                _highlights[book_title] = [highlighted_text]
        note_dict = {'location': location, 'time_added': time_added, 'highlighted_text': highlighted_text}

        if book_title in notes_data:
            notes_data[book_title]['notes'].append(note_dict)
        else:
            notes_data[book_title] = {'author': author_name, 'notes': [note_dict]}

    return notes_data


def parse_title_and_author_name(first_line: str) -> Tuple[str, str]:
    "Given the proper line of the clippings.txt section, return the book's title and the author's name"
    _author_bracket_index = first_line.rfind('(')  # find rightmost '(' in case book title contains '('
    author_name = first_line[_author_bracket_index:][1:-1].strip()

    book_title = first_line[:_author_bracket_index].strip()
    book_title = book_title.replace('\ufeff', '')  # todo - find better solution

    return book_title, author_name


def parse_highlight_info(second_line: str) -> Tuple[str, dt.datetime]:
    "Given the proper line of the clippings.txt section, return the snippet's location, and the date in which the note was taken"
    location_str = re.findall(r'(?<=.location ).+(?= \|)', second_line)[0]
    _time_added_str = re.findall('(?<=.Added on ).+', second_line)[0]
    time_added = dt.datetime.strptime(_time_added_str, '%A, %d %B %Y %H:%M:%S')

    return location_str, time_added

def parse_highlighted_text(third_line: str) -> str:
    "Probably obsolete function here"
    return third_line.rstrip(',')
