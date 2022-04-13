import os.path
import datetime as dt
import re
from jinja2 import Environment, FileSystemLoader
from notes_parser import MODULE_DIR, parse_file

OUTPUT_DIR = os.path.join(MODULE_DIR, 'output')

def output_orgmode(clippings_file: str, output_filename: str, title, starting_time, ending_time, append = False) -> str:
    title_reg = re.compile(title)
    parsed_data = parse_file(clippings_file, title_reg, starting_time, ending_time)

    # I think this is unnecessary in org mode
    # output_text = "* Highlights from '{}'\n".format(os.path.basename(clippings_file))
    output_text = "Kindle-clippings called from {} to {}".format(starting_time,ending_time)

    # No need to change that part for a single book
    for book_title in parsed_data:
        if len(parsed_data[book_title]['notes']) > 0:
            output_text += '\n\n* {}\nby {}\n'.format(book_title, parsed_data[book_title]['author'])
            for highlight in parsed_data[book_title]['notes']:
                output_text += '\n** {}\n{}\nLOC: {}'.format(highlight['highlighted_text'],
                                                                  time_to_org(highlight['time_added']),
                                                                  highlight['location'])

    # TODO Log when overwriting an existing file
    if append:
        with open(output_filename, 'a') as out:
            out.write(output_text)
    else:
        with open(output_filename, 'w') as out:
            out.write(output_text)

    return output_text

def output_plaintext(clippings_file: str, output_filename: str) -> str:
    parsed_data = parse_file(clippings_file)

    output_text = "Highlights from '{}'\n".format(os.path.basename(clippings_file))

    for book_title in parsed_data:
        book_notes_data = parsed_data[book_title]['notes']
        if len(book_notes_data) > 0:
            output_text += '\n\n{}\nby {}\n'.format(book_title, parsed_data[book_title]['author'])
            for highlight in book_notes_data:
                output_text += '\n* {}'.format(create_note_str(highlight, include_location=False))

    with open(output_filename, 'w') as out:
        out.write(output_text)

    return output_text


def output_html(clippings_file: str, output_filename: str) -> str:
    parsed_data = parse_file(clippings_file)

    variables = []
    for book, data in parsed_data.items():
        notes = data['notes']
        data = {'book_title': book,
                'author': data['author']}

        highlight_str_list = []
        for highlight in notes:
            hightlight_str = create_note_str(highlight)
            highlight_str_list.append(hightlight_str)
        data['notes'] = highlight_str_list

        variables.append(data)

    env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'html_templates')))
    template = env.get_template('basic.html')

    rendered = template.render(data=variables, input_filename=os.path.basename(clippings_file))

    with open(output_filename, 'w') as output:
        output.write(rendered)

    return rendered


def create_note_str(highlight: dict, include_location=False, include_timestamp=False) -> str:
    location = highlight['location']
    text = highlight['highlighted_text']
    time_added = highlight['time_added']

    note_str = ''
    if include_location:
        note_str += '[{}] '.format(location)

    note_str += text

    if include_timestamp:
        note_str += ' (added {})'.format(format_datetime(time_added))

    return note_str


def format_datetime(d: dt.datetime) -> str:
    """ Formats datetime to string like '2:48pm, 16th August 2018' """
    # Time
    time_str = d.strftime('%-I:%M%p').lower()

    # Date
    date_str = d.strftime('%-d{} %B %Y').format(date_suffix(d.day))

    return f'{time_str}, {date_str}'


def date_suffix(day: int) -> str:
    if not (1 <= day <= 31):
        raise ValueError('Day must be between 1-31')

    if day in range(4, 21) or day in range(24, 31):
        return 'th'
    else:
        return ['st', 'nd', 'rd'][day % 10 - 1]

def time_to_org(date: dt.datetime) -> str:
    "Simple conversion to org mode (active) timestamp"
    return date.strftime('<%Y-%m-%d %a>')
