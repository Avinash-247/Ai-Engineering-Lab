from pathlib import Path
from playwright.sync_api import sync_playwright
import sys


def webpage_to_pdf(url: str, output_path: str):
    output_file = Path(output_path)

    # Create parent directory if it doesn't exist
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:

        # Launch Chromium
        browser = p.chromium.launch()

        # Create browser page
        page = browser.new_page(
            viewport={
                "width": 1440,
                "height": 900
            }
        )

        print(f"\nOpening: {url}")

        # Open webpage
        page.goto(
            url,
            wait_until="networkidle",
            timeout=120000
        )

        print("Page loaded.")

        # Give lazy-loaded content a chance to appear
        page.evaluate("""
            async () => {
                await new Promise((resolve) => {
                    let totalHeight = 0;
                    const distance = 500;

                    const timer = setInterval(() => {
                        window.scrollBy(0, distance);
                        totalHeight += distance;

                        if (totalHeight >= document.body.scrollHeight) {
                            clearInterval(timer);
                            window.scrollTo(0, 0);
                            resolve();
                        }
                    }, 200);
                });
            }
        """)

        # Wait for images to finish loading
        page.wait_for_timeout(2000)

        page.evaluate("""
            async () => {
                const images = Array.from(document.images);

                await Promise.all(
                    images.map(img => {
                        if (img.complete) {
                            return Promise.resolve();
                        }

                        return new Promise(resolve => {
                            img.addEventListener("load", resolve);
                            img.addEventListener("error", resolve);
                        });
                    })
                );
            }
        """)

        print("Content loaded.")

        # Generate PDF
        page.pdf(
            path=str(output_file),
            format="A4",
            print_background=True,
            prefer_css_page_size=True,
            margin={
                "top": "15mm",
                "bottom": "15mm",
                "left": "10mm",
                "right": "10mm"
            }
        )

        browser.close()

    print(f"\nPDF successfully created:")
    print(output_file)


def main():

    print("=" * 60)
    print("        WEBPAGE → PDF DOWNLOADER")
    print("=" * 60)

    # Get URL from user
    url = input("\nEnter webpage URL: ").strip()

    if not url:
        print("URL cannot be empty.")
        sys.exit(1)

    # Get output location
    output_path = input(
        "Enter complete PDF save location: "
    ).strip()

    if not output_path:
        print("Output location cannot be empty.")
        sys.exit(1)

    # Add .pdf automatically
    if not output_path.lower().endswith(".pdf"):
        output_path += ".pdf"

    try:
        webpage_to_pdf(url, output_path)

    except Exception as e:
        print("\nFailed to create PDF.")
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()