# Web to Pdf
A Python script to crawl a website, convert its pages and subpages into PDF files, and combine them into a single PDF document. This tool is useful for archiving web content or creating offline copies of websites. Eg. to feed into an LLM.

## Requirements
- Python 3.x
- wkhtmltopdf
    - https://wkhtmltopdf.org/downloads.html
    - Add to PATH (on Windows)
        - Go to System Properties → Advanced → Environment Variables.
        - Find the Path variable and edit it.
        - Add the path to the wkhtmltopdf binary (e.g., C:\Program Files\wkhtmltopdf\bin).

## Run (on Windows)
2. create .venv 
    - ```pip install virtualenv```
    - ```virtualenv venv```
    - ```source venv/bin/activate```
    - ```pip install -r requirements.txt```
3. Edit ```base_url``` and ```start_url``` in ```main.py```
4. Execute the script
    - ```python main.py```