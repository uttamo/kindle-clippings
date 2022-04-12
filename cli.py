import argparse
import logging
import re
from output import output_html, output_plaintext, output_orgmode

################################################################################
# Args
################################################################################
parser = argparse.ArgumentParser(description="For parsing Amazon Kindle's 'My Clippings' files")
parser.add_argument('input', default='My Clippings.txt', help='Input filename')
parser.add_argument('output', default='output', help='Output filename')

# Single book
parser.add_argument("-t","--title", default = '.*', help="The title of the book you're interested in( or part of it )", type=str)

# Output options
# (For consistency, changed the output templates to have only Caps)
parser.add_argument('-W', action='store_true', dest='html_out', help='Output HTML')
parser.add_argument('-O', action='store_true', dest='org_out', help='Output OrgMode')

################################################################################
# Main
################################################################################
if __name__ == '__main__':
    args = parser.parse_args()
    input_filename = args.input
    output_filename = args.output

    if args.html_out:
        logging.warning('Will use html output.')
        output_html(input_filename, f'{output_filename}')
    elif args.org_out:
        logging.warning('Will use orgmode output.')
        output_orgmode(input_filename, f'{output_filename}', args.title)
    else:
        logging.warning('Will use plaintext output.\nIf this is not what you wanted run with -h or --help')
        output_plaintext(input_filename, f'{output_filename}')
