import asyncio
import aiohttp
import os
from playwright.async_api import async_playwright
import re



def sanitize_filename(name: str) -> str:
    # Replace invalid Windows characters with underscores
    return re.sub(r'[\\/:\*\?"<>\|]', "_", name)


async def download_image(session, url, filename, retries=3):
    for attempt in range(1, retries + 1):
        try:
            # Skip if file exists and has content
            if os.path.exists(filename) and os.path.getsize(filename) > 0:
                print(f"Skipped {filename} (already exists)")
                return True

            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.read()
                    if len(data) > 0:  # Checks for corrupted downloads
                        with open(filename, "wb") as f:
                            f.write(data)
                        print(f"Downloaded {filename}")
                        return True
                    else:
                        print(f"Attempt {attempt}: {filename} empty file")
                else:
                    print(f"Attempt {attempt}: {filename} failed (status {response.status})")

        except Exception as e:
            print(f"Attempt {attempt}: error downloading {filename}: {e}")

        await asyncio.sleep(2)

    print(f"Failed to download {filename} after {retries} attempts")
    return False


async def main():
    target_url = str(input("Input mangakatana chapter url: "))

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto(target_url, wait_until="domcontentloaded")

        # Use tab title for folder name
        Directory_name = sanitize_filename(await page.title())
        os.makedirs(Directory_name, exist_ok=True)

        # Scroll down slowly to trigger lazy-loading
        prev_count = 0
        while True:
            await page.mouse.wheel(0, 3000)
            await asyncio.sleep(1)
            divs = await page.query_selector_all("div[id^='page'] img")
            if len(divs) == prev_count:  # No new images loaded
                break
            prev_count = len(divs)

        await page.wait_for_selector("div[id^='page'] img", timeout=60000)

        divs = await page.query_selector_all("div[id^='page']")
        images = []
        for div in divs:
            page_id = await div.get_attribute("id")
            img = await div.query_selector("img")
            if img:
                img_url = await img.get_attribute("data-src") or await img.get_attribute("src")
                if img_url:
                    filename = os.path.join(Directory_name, f"{page_id}.jpg")
                    images.append((img_url, filename))

        await browser.close()

        # Keep retrying until all pages are downloaded
        async with aiohttp.ClientSession() as session:
            remaining = images
            while remaining:
                tasks = [download_image(session, url, filename) for url, filename in remaining]
                results = await asyncio.gather(*tasks)

                # Filter out successful downloads, retry failed ones
                remaining = [img for img, success in zip(remaining, results) if not success]

                if remaining:
                    print(f"🔄 Retrying {len(remaining)} failed downloads...")
                    await asyncio.sleep(3)

        print("All pages downloaded successfully!")


if __name__ == "__main__":
    asyncio.run(main())
