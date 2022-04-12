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
