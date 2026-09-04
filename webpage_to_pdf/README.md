# Webpage to PDF Downloader

A Python-based utility that converts a webpage into a **PDF document** using [Playwright](https://playwright.dev/) and Chromium.

The application accepts:

1. A webpage URL
2. A destination path where the PDF should be saved

It then opens the webpage in a real Chromium browser, waits for the page to render, loads lazy-loaded content and images, and finally generates a PDF that closely represents the rendered webpage.

---

## Features

* Convert a webpage into PDF
* Supports modern JavaScript-based websites
* Uses a real Chromium browser through Playwright
* Waits for dynamically loaded content
* Scrolls through the webpage to trigger lazy loading
* Waits for images to finish loading
* Preserves webpage styling as much as possible
* Preserves text, images, tables, backgrounds, and layout
* Automatically creates the output directory if it does not exist
* Automatically adds `.pdf` extension
* Uses A4 page format
* Prints background graphics
* Supports Windows file paths

---

# How It Works

The overall workflow looks like this:

```text
                    User
                      │
                      │
              Enter webpage URL
                      │
                      ▼
              Enter output path
                      │
                      ▼
                Python Program
                      │
                      ▼
                  Playwright
                      │
                      ▼
              Launch Chromium
                      │
                      ▼
                Open Webpage
                      │
                      ▼
        Wait for JavaScript / Network
                      │
                      ▼
              Scroll the webpage
                      │
                      ▼
        Trigger lazy-loaded content
                      │
                      ▼
             Wait for images
                      │
                      ▼
          Fully rendered webpage
                      │
                      ▼
                Generate PDF
                      │
                      ▼
              Save PDF to disk
```

---

# Project Structure

```text
webpage-to-pdf/
│
├── main.py
│
├── pyproject.toml
│
├── uv.lock
│
└── README.md
```

### `main.py`

Contains the complete Python application.

It is responsible for:

* Reading user input
* Launching Chromium
* Opening the webpage
* Waiting for webpage content
* Handling lazy-loaded content
* Waiting for images
* Generating the PDF
* Saving the PDF

### `pyproject.toml`

Contains the Python project configuration and dependencies.

For this project, Playwright is installed as a dependency.

### `uv.lock`

Created and maintained by `uv`.

It locks the exact dependency versions so the project can be reproduced more consistently on another machine.

### `README.md`

Contains project documentation, installation instructions, usage instructions, and technical explanation.

---

# Requirements

You need:

* Python 3.9+
* `uv`
* Playwright
* Chromium

---

# Installation

## 1. Create the project

```powershell
mkdir webpage-to-pdf
cd webpage-to-pdf
```

Initialize the project:

```powershell
uv init
```

---

## 2. Install Playwright

Install Playwright using `uv`:

```powershell
uv add playwright
```

This installs the **Python Playwright package**.

However, there is an important distinction here.

Installing Playwright does **not automatically mean that Chromium is installed**.

---

# Playwright vs Chromium

Playwright consists of two important parts:

```text
Playwright
│
├── Python package
│      │
│      └── Installed using:
│          uv add playwright
│
└── Browser binaries
       │
       └── Chromium
              │
              └── Installed using:
                  uv run playwright install chromium
```

### Install the Python package

```powershell
uv add playwright
```

This gives Python access to Playwright APIs such as:

```python
from playwright.sync_api import sync_playwright
```

But Playwright still needs an actual browser to perform browser automation.

### Install Chromium

Run:

```powershell
uv run playwright install chromium
```

This downloads the Chromium browser binary required by Playwright.

After this, your system has:

```text
Python
  │
  └── Playwright
          │
          └── Chromium
```

Now Python can control Chromium.

---

# Why Do We Need Chromium?

A simple HTTP request can download the HTML of a webpage:

```python
import requests

response = requests.get(url)
```

However, modern websites are often not just static HTML.

For example:

```text
HTML
 │
 ├── JavaScript
 ├── CSS
 ├── Images
 ├── API requests
 ├── Dynamic components
 └── Lazy-loaded content
```

The initial HTML might not contain all the content visible in the browser.

For example:

```text
User opens webpage
       │
       ▼
Initial HTML loads
       │
       ▼
JavaScript executes
       │
       ▼
API request
       │
       ▼
Data arrives
       │
       ▼
Page updates
       │
       ▼
Content becomes visible
```

A simple `requests.get()` call may only retrieve the initial HTML.

Playwright solves this by opening the page inside a real browser.

```text
Python
  │
  ▼
Playwright
  │
  ▼
Chromium
  │
  ▼
Website
  │
  ├── HTML
  ├── CSS
  ├── JavaScript
  ├── Images
  └── Dynamic content
```

Therefore, Playwright is much more suitable for modern JavaScript-heavy websites.

---

# Running the Application

Run:

```powershell
uv run main.py
```

The application will display:

```text
============================================================
        WEBPAGE → PDF DOWNLOADER
============================================================

Enter webpage URL:
```

Enter the webpage URL:

```text
https://directai.blog/2026/09/03/python-classroom-notes-03-sep-2026/
```

Then it asks:

```text
Enter complete PDF save location:
```

Example:

```text
C:\Users\vempa\Documents\QT-classes-videos\directai.io notes.pdf
```

The program will then process the webpage.

---

# Example

```text
============================================================
        WEBPAGE → PDF DOWNLOADER
============================================================

Enter webpage URL: https://directai.blog/2026/09/03/python-classroom-notes-03-sep-2026/

Enter complete PDF save location: C:\Users\vempa\Documents\QT-classes-videos\directai.io notes.pdf

Opening: https://directai.blog/2026/09/03/python-classroom-notes-03-sep-2026/

Page loaded.

Content loaded.

PDF successfully created:

C:\Users\vempa\Documents\QT-classes-videos\directai.io notes.pdf
```

---

# Detailed Code Explanation

## 1. Import Required Libraries

```python
from pathlib import Path
from playwright.sync_api import sync_playwright
import sys
```

### `Path`

```python
from pathlib import Path
```

`Path` is used to work with file and directory paths.

For example:

```python
output_file = Path(output_path)
```

This allows us to easily create directories and handle file paths.

---

### `sync_playwright`

```python
from playwright.sync_api import sync_playwright
```

This imports Playwright's synchronous API.

It allows us to control Chromium using normal Python code.

---

### `sys`

```python
import sys
```

`sys` is used to terminate the program when an error occurs.

For example:

```python
sys.exit(1)
```

---

# 2. Webpage-to-PDF Function

The main functionality is contained inside:

```python
def webpage_to_pdf(url: str, output_path: str):
```

The function receives two values:

```text
url
 │
 └── Webpage that we want to convert

output_path
 │
 └── Location where we want to save the PDF
```

For example:

```python
webpage_to_pdf(
    "https://example.com",
    "C:/Users/Avi/Documents/example.pdf"
)
```

---

# 3. Create the Output Directory

```python
output_file = Path(output_path)

output_file.parent.mkdir(
    parents=True,
    exist_ok=True
)
```

Suppose the user enters:

```text
C:\Users\vempa\Documents\QT-classes-videos\notes.pdf
```

The program checks whether:

```text
QT-classes-videos
```

exists.

If it does not exist, Python creates it.

```text
Documents
└── QT-classes-videos
    └── notes.pdf
```

The important part is:

```python
parents=True
```

which allows Python to create missing parent directories.

And:

```python
exist_ok=True
```

means:

> Don't throw an error if the directory already exists.

---

# 4. Start Playwright

```python
with sync_playwright() as p:
```

This starts Playwright.

Think of it as:

```text
Start Playwright
      │
      ▼
Get access to browser automation
      │
      ▼
Launch Chromium
```

The `with` statement also makes sure Playwright is properly cleaned up afterward.

---

# 5. Launch Chromium

```python
browser = p.chromium.launch()
```

This starts the Chromium browser.

Conceptually:

```text
Python
  │
  ▼
Playwright
  │
  ▼
Chromium
```

The browser runs separately from Python.

Python sends commands to Playwright, and Playwright controls Chromium.

---

# 6. Create a Browser Page

```python
page = browser.new_page(
    viewport={
        "width": 1440,
        "height": 900
    }
)
```

This creates a new browser tab/page.

The viewport is set to:

```text
Width  = 1440px
Height = 900px
```

This is similar to opening the website in a desktop browser.

---

# 7. Open the Webpage

```python
page.goto(
    url,
    wait_until="networkidle",
    timeout=120000
)
```

This tells Chromium to navigate to the provided URL.

### `url`

The webpage provided by the user.

### `wait_until="networkidle"`

Playwright waits until network activity becomes mostly idle.

This is useful because modern websites often load content through JavaScript.

Instead of:

```text
Open page
↓
Immediately create PDF
```

we want:

```text
Open page
↓
Load HTML
↓
Load CSS
↓
Execute JavaScript
↓
Load API data
↓
Load images
↓
Wait
↓
Create PDF
```

### `timeout=120000`

The timeout is:

```text
120000 milliseconds
=
120 seconds
=
2 minutes
```

This prevents the program from waiting forever if a website fails to load.

---

# 8. Handle Lazy-Loaded Content

Many modern websites use **lazy loading**.

For example, an image might not load until the user scrolls near it.

Initially:

```text
Browser opens page

┌──────────────────────┐
│ Image 1              │ ← loaded
│                      │
│ Text                 │
│                      │
│ Image 2              │ ← loaded
│                      │
├──────────────────────┤
│ Image 3              │ ← not loaded yet
│                      │
│ Image 4              │ ← not loaded yet
└──────────────────────┘
```

When the user scrolls:

```text
Scroll
  ↓
Image 3 loads
  ↓
Scroll
  ↓
Image 4 loads
```

Our program automatically scrolls through the page:

```python
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
```

Conceptually:

```text
Top
 │
 ▼
Scroll 500px
 │
 ▼
Scroll 500px
 │
 ▼
Scroll 500px
 │
 ▼
Continue...
 │
 ▼
Bottom reached
 │
 ▼
Return to top
```

This gives lazy-loaded content an opportunity to load.

---

# 9. Wait for Images

After scrolling, the program waits:

```python
page.wait_for_timeout(2000)
```

This gives the browser additional time to finish loading resources.

Then it checks the images:

```python
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
```

The purpose is:

```text
Find all images
      │
      ▼
Check each image
      │
      ├── Already loaded → Continue
      │
      └── Not loaded
             │
             ▼
       Wait for image
             │
             ▼
          Continue
```

This reduces the chance of generating a PDF with missing images.

---

# 10. Generate the PDF

The actual PDF generation happens here:

```python
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
```

### `path`

Specifies where the PDF should be saved.

Example:

```text
C:\Users\vempa\Documents\QT-classes-videos\notes.pdf
```

### `format="A4"`

Creates the PDF using A4 paper dimensions.

### `print_background=True`

Includes background colors and background images where supported.

Without this, some webpages may lose their background styling.

### `prefer_css_page_size=True`

If the webpage defines its own print page size using CSS, Playwright can prefer that size.

### Margins

The PDF uses:

```text
Top:    15mm
Bottom: 15mm
Left:   10mm
Right:  10mm
```

---

# 11. Close the Browser

After generating the PDF:

```python
browser.close()
```

This closes Chromium.

The overall lifecycle is:

```text
Launch browser
      │
      ▼
Open webpage
      │
      ▼
Render content
      │
      ▼
Load images
      │
      ▼
Generate PDF
      │
      ▼
Close browser
```

---

# 12. Get User Input

The `main()` function asks the user for the webpage URL:

```python
url = input("\nEnter webpage URL: ").strip()
```

Then it asks where the PDF should be saved:

```python
output_path = input(
    "Enter complete PDF save location: "
).strip()
```

This makes the program reusable.

We don't need to modify the Python code every time we want to download a different webpage.

---

# 13. Automatically Add `.pdf`

The program checks:

```python
if not output_path.lower().endswith(".pdf"):
    output_path += ".pdf"
```

So if the user enters:

```text
C:\Users\vempa\Documents\notes
```

the program automatically changes it to:

```text
C:\Users\vempa\Documents\notes.pdf
```

---

# Error Handling

The main operation is wrapped inside:

```python
try:
    webpage_to_pdf(url, output_path)

except Exception as e:
    print("\nFailed to create PDF.")
    print(f"Error: {e}")
    sys.exit(1)
```

If something goes wrong, instead of showing a Python traceback, the program reports the error.

For example:

```text
Failed to create PDF.

Error: BrowserType.launch: Executable doesn't exist...
```

---

# Common Installation Error

You may see:

```text
BrowserType.launch: Executable doesn't exist
```

This usually means Playwright is installed but Chromium is not.

### Incorrect assumption

```text
uv add playwright
       │
       └── "Playwright + Chromium installed"
```

This is not correct.

### Correct process

```text
uv add playwright
       │
       ▼
Install Python Playwright package
       │
       ▼
uv run playwright install chromium
       │
       ▼
Download Chromium browser
       │
       ▼
uv run main.py
```

Therefore, after cloning this project on a new machine, run:

```powershell
uv sync
uv run playwright install chromium
```

Then:

```powershell
uv run main.py
```

---

# Why Not Use `requests`?

A common approach would be:

```python
import requests

html = requests.get(url).text
```

This works well for simple static websites.

However:

```text
requests
   │
   ▼
HTTP response
   │
   ▼
Initial HTML
```

It does not behave like a complete browser.

Modern websites may use:

* JavaScript
* React
* Vue
* Angular
* API calls
* Lazy loading
* Client-side rendering

Therefore:

```text
requests
   │
   └── Downloads response

Playwright
   │
   └── Runs a real browser
          │
          ├── HTML
          ├── CSS
          ├── JavaScript
          ├── Images
          ├── API requests
          └── Dynamic content
```

For webpage-to-PDF conversion, browser automation is generally the better approach.

---

# Important Limitation

This tool attempts to create a PDF representation of the **rendered webpage**.

It does not guarantee a 100% identical reproduction of every website.

Some websites may contain:

* Login-protected content
* Content hidden behind user interaction
* Infinite scrolling
* Embedded videos
* Cross-origin resources
* Canvas-based graphics
* Content generated after specific user actions
* Anti-bot protection
* Content that is intentionally unavailable to automated browsers

In such cases, additional handling may be required.

---

# Security and Responsible Usage

Only download webpages that you are authorized to access.

Do not use the tool to bypass:

* Authentication
* Access controls
* Paywalls
* DRM
* Anti-bot protections
* Other technical restrictions

The tool is intended for legitimate webpage archiving, documentation, personal notes, research, and offline reading.

---

# Quick Start

Clone/download the project and run:

```powershell
uv sync
```

Install Chromium:

```powershell
uv run playwright install chromium
```

Run the application:

```powershell
uv run main.py
```

Enter:

```text
Webpage URL
```

and:

```text
PDF output path
```

The resulting PDF will be saved at the specified location.

---

# Technology Stack

| Technology | Purpose                              |
| ---------- | ------------------------------------ |
| Python     | Application programming language     |
| Playwright | Browser automation                   |
| Chromium   | Webpage rendering                    |
| uv         | Python dependency/project management |
| PDF        | Final output format                  |

---

# Architecture

```text
┌─────────────────────────────┐
│          User               │
│                             │
│  URL + Output File Path     │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│          main.py            │
│                             │
│  Input validation           │
│  File path handling         │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│         Playwright          │
│                             │
│  Browser automation         │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│          Chromium           │
│                             │
│  Render webpage             │
│  Execute JavaScript         │
│  Load CSS                   │
│  Load images                │
│  Load dynamic content       │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│       Fully Rendered        │
│          Webpage            │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│       Playwright PDF        │
│                             │
│  A4                         │
│  Backgrounds                │
│  CSS page size              │
│  Margins                    │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│        Output PDF           │
│                             │
│ C:\...\your-file.pdf        │
└─────────────────────────────┘
```

---

# Future Improvements

Possible improvements for the project include:

* Command-line arguments
* GUI interface
* Batch URL processing
* Multiple URLs → one PDF
* Automatic PDF filename generation
* Custom page sizes
* Header and footer support
* Page numbers
* Authentication support
* Better handling of infinite scrolling
* Automatic screenshot capture
* Downloading linked resources
* Custom browser user-agent
* Retry mechanism
* Logging
* Progress indicators
* Configuration file
* Docker support

---

## Summary

The application follows a simple but powerful workflow:

```text
URL
 ↓
Playwright
 ↓
Chromium
 ↓
Render webpage
 ↓
Execute JavaScript
 ↓
Load dynamic content
 ↓
Scroll for lazy-loaded content
 ↓
Wait for images
 ↓
Generate PDF
 ↓
Save to requested location
```

The most important concept is that **Playwright is not itself the browser**.

Playwright is the automation tool, while **Chromium is the browser that actually renders the webpage**.

Therefore, both are required:

```text
Playwright = Controls the browser
Chromium   = Renders the webpage
```

Install both with:

```powershell
uv add playwright
uv run playwright install chromium
```

Then run:

```powershell
uv run main.py
```
