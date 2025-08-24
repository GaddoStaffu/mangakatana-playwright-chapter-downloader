# Mangakatana Playwright Chapter Downloader

A Python script to download all manga pages from a Mangakatana chapter using Playwright.

## Features

- Downloads all images from a Mangakatana chapter URL
- Retries failed downloads automatically
- Skips already downloaded images
- Organize manga chapters with apporiate folder name

## Requirements

- Python 3.8+
- [Playwright](https://playwright.dev/python/)
- [aiohttp](https://docs.aiohttp.org/en/stable/)

## Installation

1. Clone this repository:

   ```sh
   git clone https://github.com/yourusername/mangakatana-playwright-chapter-downloader.git
   cd mangakatana-playwright-chapter-downloader
   ```

2. Install dependencies:

   ```sh
   python -m venv .env
   activate the environment ./env/scripts/activate
   pip install -r requirements.txt
   playwright install
   ```

## Usage

1. Run the script:

   ```sh
   python main.py
   ```

2. Input the Mangakatana chapter URL when prompted.

3. The script will create a folder named after the chapter and download all images into it.

## Example

```
Input mangakatana chapter url: https://mangakatana.com/manga/one-piece.1/c1
Downloaded One Piece - Chapter 1/page1.jpg
Downloaded One Piece - Chapter 1/page2.jpg
...
All pages downloaded successfully!
```

## Notes

- Only chapter URLs are supported (not manga overview pages).
- If downloads fail, the script will retry automatically (max 3 times).

## TODO

- Add ability to input the manga page url instead of the chapter and then ask the user what chapter to download (example: 1,2,3,4,5, 6-10)
