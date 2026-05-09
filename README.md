# PDF Table Extractor (Web to Excel)

## Description

This script automatically:

* Scans a webpage for PDF links
* Downloads the first available PDF
* Extracts tabular data from the PDF
* Saves the data into an Excel file

It is designed to work with any webpage that contains direct `.pdf` links.

---

## Features

* Works with any website (just change the URL)
* Automatically detects PDF links
* Extracts tables using pdfplumber
* Cleans and merges data into a single Excel file
* Removes temporary files after execution

---

## Requirements

Install dependencies:

```bash
pip install -r requirements.txt 
```

---

## Usage

Run the script:

```bash
python main.py
```

---

## Configuration

Open the script and change the target page:

```bash
TARGET_PAGE = "https://example.com/page-with-pdf"
```

---

## How It Works

1. Sends a request to the target webpage
2. Parses HTML using BeautifulSoup
3. Finds links that contain `.pdf`
4. Downloads the first PDF found
5. Extracts tables using pdfplumber
6. Converts data into pandas DataFrame
7. Saves output as `result.xlsx`

---

## Output

* Excel file: `result.xlsx`
* Temporary file: `temp.pdf` (deleted automatically)

---

## Limitations

* Works only if the PDF link is directly available in HTML
* Does not support JavaScript-rendered links
* May fail on scanned PDFs (images instead of text)
* Table extraction depends on PDF structure

---

## Possible Improvements

* Support multiple PDFs per page
* Add OCR for scanned PDFs (pytesseract)
* Export each table to separate Excel sheets
* Add GUI or web interface

---

## Example

```bash
TARGET_PAGE = "https://esmis.nal.usda.gov/publication/crop-progress"
```

---

## License

Free to use for educational and personal projects
