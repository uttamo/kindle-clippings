import os.path

from notes_parse import MODULE_DIR, parse_file

OUTPUT_DIR = os.path.join(MODULE_DIR, 'output')


def output_plaintext(clippings_file: str, output_filename: str) -> str:
    parsed_data = parse_file(clippings_file)
    output_filename = os.path.join(OUTPUT_DIR, output_filename)

    output_text = f'Parsed Kindle clippings file: {clippings_file}\n\n'

    for book_title in parsed_data:
        book_notes_data = parsed_data[book_title]['notes']
        if len(book_notes_data) > 0:
            output_text += '\n{}\nby {}\n\n'.format(book_title, parsed_data[book_title]['author'])
            for highlight in book_notes_data:
                output_text += '* [{}] "{}" (added {})\n'.format(highlight['location'],
                                                           highlight['highlighted_text'],
                                                           highlight['time_added'])

    with open(output_filename, 'w') as out:
        out.write(output_text)

    return output_text
