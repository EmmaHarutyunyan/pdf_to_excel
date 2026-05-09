import os
import requests
import pdfplumber
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin

HEADERS = {"User-Agent": "Mozilla/5.0"}

def find_pdf_link(page_url):
    print(f"Scanning page: {page_url}")
    
    response = requests.get(page_url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')

    pdf_links = []

    for link in soup.find_all('a', href=True):
        href = link['href']
        if '.pdf' in href.lower():
            full_link = urljoin(page_url, href)
            pdf_links.append(full_link)

    if not pdf_links:
        return None

    return pdf_links[0]


def download_pdf(pdf_url):
    print(f"Downloading PDF: {pdf_url}")
    file_name = "temp.pdf"

    response = requests.get(pdf_url, headers=HEADERS)
    with open(file_name, "") as f:
        f.write(response.content)

    return file_name


def extract_tables(pdf_path):
    print("Extracting tables...")

    all_dfs = []

    settings = {
        "vertical_strategy": "text",
        "horizontal_strategy": "text",
        "snap_tolerance": 3,
        "intersection_tolerance": 10,
    }

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables(table_settings=settings)

            for table in tables:
                df = pd.DataFrame(table)
                df = df.dropna(how='all').dropna(axis=1, how='all')

                if not df.empty:
                    df = df.replace(r'\n', ' ', regex=True)
                    all_dfs.append(df)

    return all_dfs


def save_excel(dfs):
    if not dfs:
        print("No tables found in PDF.")
        return

    final_df = pd.concat(dfs, ignore_index=True)
    output_file = "result.xlsx"

    try:
        final_df.to_excel(output_file, index=False, header=False)
        print(f"SUCCESS: Saved to {output_file}")
    except PermissionError:
        print("Close Excel file and try again.")


def start(page_url):
    pdf_link = find_pdf_link(page_url)

    if not pdf_link:
        print("No PDF found on this page.")
        return

    pdf_file = download_pdf(pdf_link)
    dfs = extract_tables(pdf_file)
    save_excel(dfs)

    if os.path.exists(pdf_file):
        os.remove(pdf_file)


if __name__ == "__main__":
    TARGET_PAGE = "https://esmis.nal.usda.gov/publication/crop-progress"
    
    start(TARGET_PAGE)
