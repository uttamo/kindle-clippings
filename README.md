# Kindle Clippings

Parse the **My Clippings.txt** file that is stored on your Amazon Kindle which contains highlights you've made across all of the books you've read.

## Usage

```
positional arguments:
  input                 Input filename
  output                Output filename

optional arguments:
  -h, --help            show this help message and exit
  -t TITLE, --title TITLE
                        The title of the book you're interested in( or part of it )
  -sT STARTING_TIME, --starting-time STARTING_TIME
                        The starting date for your (new) notes. Notes with older timestamps will be omitted. Defaults to /the beginning/, (i doubt you'll go somewhere that back in time). To be given in isoformat
  -eT ENDING_TIME, --ending-time ENDING_TIME
                        The ending date for your (old) notes. Notes with newer timestamps will be ommited. Defaults to the present. To be given in isoformat
  -W                    Output HTML
  -O                    Output OrgMode
```

## Usage example
Feel free to run them with the given example input

### Output Types
Default output is plaintext

`python cli.py 'My Clippings.txt' 'output.txt'`

Generating HTML instead

`python cli.py 'My Clippings.txt' 'output.html' -W`

Generating Org-Mode

`python cli.py 'My Clippings.txt' -O 'output.org'`

### Filtering by Book title
`python cli.py 'My Clippings.txt' -O 'output.org' --title "Black Edge"`

### Filtering by time
These last examples do not work with the provided input, they just show how the time parameters should be used:

By starting time:
`python cli.py 'My Clippings.txt' -O 'output.org' -sT '2021-04-14'`

By /ending/ time:
`python cli.py 'My Clippings.txt' -O 'output.org' -eT '2022-04-14'`

Using both start and end time:
`python cli.py 'My Clippings.txt' -O 'output.org' -sT '2021-04-14' -eT '2022-04-14'`
