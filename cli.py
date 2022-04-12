import argparse
import sys
import logging

from output import output_html, output_plaintext, output_orgmode

parser = argparse.ArgumentParser(description="For parsing Amazon Kindle's 'My Clippings' files")

parser.add_argument('input', default='My Clippings.txt', help='Input filename')
parser.add_argument('output', default='output', help='Output filename')

# For consistency, changed the output templates to have only Caps
parser.add_argument('-W', action='store_true', dest='html_output', help='Output HTML')
parser.add_argument('-T', action='store_true', dest='plaintext_output', help='Output plaintext')
parser.add_argument('-O', action='store_true', dest='orgmode_output', help='Output OrgMode')


if __name__ == '__main__':
    namespace = parser.parse_args(sys.argv[1:])
    input_filename = namespace.input
    output_filename = namespace.output
    plaintext_output = namespace.plaintext_output
    orgmode_output = namespace.orgmode_output
    html_output = namespace.html_output

    if plaintext_output and html_output or plaintext_output and orgmode_output or orgmode_output and html_output:
        logging.warning('Both plaintext and HTML output flags are True, will use plaintext output.')

    if html_output:
        output_html(input_filename, f'{output_filename}')
    elif orgmode_output:
        output_orgmode(input_filename, f'{output_filename}')
    else:
        output_plaintext(input_filename, f'{output_filename}')
