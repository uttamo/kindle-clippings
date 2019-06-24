# Kindle Clippings

Parse the **My Clippings.txt** file that is stored on your Amazon Kindle which contains highlights you've made across all of the books you've read.

## Usage

```
positional arguments:
  input       Input filename
  output      Output filename

optional arguments:
  -h, --help  show this help message and exit
  -w          Output HTML
  -t          Output plaintext
```

## Usage example

Default output is plaintext

`python cli.py 'My Clippings.txt' 'output.txt'`

Generating HTML instead

`python cli.py 'My Clippings.txt' 'output.html' -w`
