import os
import requests
import pdfplumber
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# SETUP: USDA Crop Progress Publication Page
TARGET_URL = "https://esmis.nal.usda.gov/publication/crop-progress"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

def start_automation():
    print(f"Scanning {TARGET_URL} for the latest PDF...")
    try:
        response = requests.get(TARGET_URL, headers=HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        pdf_link = None
        for link in soup.find_all('a', href=True):
            if link['href'].lower().endswith('.pdf'):
                pdf_link = urljoin(TARGET_URL, link['href'])
                break 
        
        if not pdf_link:
            print("No PDF found on this page.")
            return

        print(f"Downloading: {pdf_link}")
        pdf_file = "usda_report.pdf"
        file_data = requests.get(pdf_link, headers=HEADERS).content
        with open(pdf_file, 'wb') as f:
            f.write(file_data)

        print("Processing pages... fixing table alignment.")
        all_dfs = []
        
        settings = {
            "vertical_strategy": "text", 
            "horizontal_strategy": "text",
            "snap_tolerance": 3,
            "intersection_tolerance": 10,
        }

        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables(table_settings=settings)
                for table in tables:
                    df = pd.DataFrame(table)
                    
                    df = df.dropna(how='all').dropna(axis=1, how='all')
                    
                    if not df.empty:
                        df = df.replace(r'\n', ' ', regex=True)
                        all_dfs.append(df)

        if all_dfs:
            output_name = "Cleaned_USDA_Data.xlsx"
            final_df = pd.concat(all_dfs, ignore_index=True)
            
            try:
                final_df.to_excel(output_name, index=False, header=False)
                print(f"--- SUCCESS: Data saved to {output_name} ---")
            except PermissionError:
                print(f"--- ERROR: Close {output_name} and run again. ---")
        else:
            print("No tabular data could be parsed.")

        if os.path.exists(pdf_file):
            os.remove(pdf_file)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    start_automation()