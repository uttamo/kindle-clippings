import os.path
from typing import Tuple
import re
import datetime as dt

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))


def parse_file(path: str) -> dict:
    full_path = os.path.join(MODULE_DIR, path)

    with open(full_path, 'r', encoding='utf-8-sig') as clippings_file:
        content = clippings_file.read()

    _unsuitable_sections = []
    notes_data = {}
    _highlights = {}

    sections = content.split('==========')
    for section in sections:
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
            raise NotImplementedError(f'Unsupported note type: {section}')

        lines = [line for line in section.split('\n') if line]
        if len(lines) != 3:
            _unsuitable_sections.append(lines)
            continue

        # Title and author
        title_and_author_str = lines[0]
        book_title, author_name = parse_title_and_author_name(title_and_author_str)

        # Highlight info - location and time added
        highlight_info_str = lines[1]
        location, time_added = parse_highlight_info(highlight_info_str)

        # Highlighted text
        highlighted_text = lines[2]
        # Sometimes the clippings file has duplicated notes, so we need to check if a particular note has already been
        # encountered
        existing_highlights_for_author = _highlights.get(book_title, [])
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
    _author_bracket_index = first_line.rfind('(')  # find rightmost '(' in case book title contains '('
    author_name = first_line[_author_bracket_index:][1:-1].strip()

    book_title = first_line[:_author_bracket_index].strip()
    book_title = book_title.replace('\ufeff', '')  # todo - find better solution

    return book_title, author_name


def parse_highlight_info(second_line: str) -> Tuple[str, dt.datetime]:
    location_str = re.findall('(?<=.location ).+(?= \|)', second_line)[0]
    _time_added_str = re.findall('(?<=.Added on ).+', second_line)[0]
    time_added = dt.datetime.strptime(_time_added_str, '%A, %d %B %Y %H:%M:%S')

    return location_str, time_added


def parse_highlighted_text(third_line: str) -> str:
    return third_line.rstrip(',')
