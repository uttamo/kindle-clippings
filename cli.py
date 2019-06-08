import argparse
import sys
import logging

from output import output_html, output_plaintext


parser = argparse.ArgumentParser(description="For parsing Amazon Kindle's 'My Clippings' files")

parser.add_argument('input', default='My Clippings.txt', help='Input filename')
parser.add_argument('output', default='output', help='Output filename without extension')
parser.add_argument('-w', action='store_true', dest='html_output', help='Output HTML')
parser.add_argument('-t', action='store_true', dest='plaintext_output', help='Output plaintext')


if __name__ == '__main__':
    namespace = parser.parse_args(sys.argv[1:])
    input_filename = namespace.input
    output_filename = namespace.output
    plaintext_output = namespace.plaintext_output
    html_output = namespace.html_output

    if plaintext_output and html_output:
        logging.warning('Both plaintext and HTML output flags are True, will use plaintext output.')

    if html_output and not plaintext_output:
        output_html(input_filename, f'{output_filename}')
    else:
        output_plaintext(input_filename, f'{output_filename}')
