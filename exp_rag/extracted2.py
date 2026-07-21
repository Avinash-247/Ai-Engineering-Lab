import pymupdf
import os

PDF_PATH = "./knowledgebase/book/book_paper.pdf"

TEXT_OUTPUT_FOLDER = "./knowledgebase/extracted/text"
IMAGE_OUTPUT_FOLDER = "./knowledgebase/extracted/images"

os.makedirs(TEXT_OUTPUT_FOLDER, exist_ok=True)
os.makedirs(IMAGE_OUTPUT_FOLDER, exist_ok=True)

TEXT_OUTPUT_FILE = os.path.join(
    TEXT_OUTPUT_FOLDER,
    "document.txt"
)

doc = pymupdf.open(PDF_PATH)

all_text = ""

image_counter = 1
vector_counter = 1

# -----------------------------
# CONFIGURATION
# -----------------------------

MIN_WIDTH = 180
MIN_HEIGHT = 180

MAX_PAGE_COVERAGE = 0.55

PADDING = 20

ZOOM_FACTOR = 4

saved_regions = []

# -----------------------------
# PROCESS PDF
# -----------------------------

for page_number in range(len(doc)):

    page = doc.load_page(page_number)

    page_rect = page.rect
    page_area = page_rect.width * page_rect.height

    # ==========================================
    # TEXT EXTRACTION
    # ==========================================

    text = page.get_text()

    all_text += (
        f"\n\n"
        f"========== PAGE {page_number + 1} ==========\n\n"
    )

    all_text += text

    # ==========================================
    # EMBEDDED IMAGES
    # ==========================================

    image_list = page.get_images(full=True)

    for img in image_list:

        try:
            xref = img[0]

            base_image = doc.extract_image(xref)

            image_bytes = base_image["image"]
            image_ext = base_image["ext"]

            if len(image_bytes) < 10000:
                continue

            filename = (
                f"page_{page_number+1}"
                f"_embedded_{image_counter}"
                f".{image_ext}"
            )

            image_path = os.path.join(
                IMAGE_OUTPUT_FOLDER,
                filename
            )

            with open(image_path, "wb") as f:
                f.write(image_bytes)

            print(f"Saved {filename}")

            image_counter += 1

        except Exception:
            pass

    # ==========================================
    # VECTOR FIGURES / TABLES / DIAGRAMS
    # ==========================================

    drawings = page.get_drawings()

    for drawing in drawings:

        try:

            rect = drawing["rect"]

            width = rect.width
            height = rect.height

            area = width * height

            # Ignore small objects
            if width < MIN_WIDTH:
                continue

            if height < MIN_HEIGHT:
                continue

            # Ignore whole page captures
            if area > page_area * MAX_PAGE_COVERAGE:
                continue

            # Add padding
            clip = pymupdf.Rect(
                max(0, rect.x0 - PADDING),
                max(0, rect.y0 - PADDING),
                min(page_rect.width, rect.x1 + PADDING),
                min(page_rect.height, rect.y1 + PADDING)
            )

            # Avoid duplicates
            duplicate = False

            for old_clip in saved_regions:

                overlap = clip.intersect(old_clip)

                if overlap.is_empty:
                    continue

                overlap_area = (
                    overlap.width *
                    overlap.height
                )

                clip_area = (
                    clip.width *
                    clip.height
                )

                if overlap_area / clip_area > 0.8:
                    duplicate = True
                    break

            if duplicate:
                continue

            saved_regions.append(clip)

            pix = page.get_pixmap(
                matrix=pymupdf.Matrix(
                    ZOOM_FACTOR,
                    ZOOM_FACTOR
                ),
                clip=clip,
                alpha=False
            )

            # Skip blank images
            samples = pix.samples

            unique_values = len(
                set(samples[:5000])
            )

            if unique_values < 5:
                continue

            filename = (
                f"page_{page_number+1}"
                f"_vector_{vector_counter}.png"
            )

            save_path = os.path.join(
                IMAGE_OUTPUT_FOLDER,
                filename
            )

            pix.save(save_path)

            print(f"Saved {filename}")

            vector_counter += 1

        except Exception:
            pass

# ==========================================
# SAVE TEXT
# ==========================================

with open(
    TEXT_OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:
    f.write(all_text)

print("\n--------------------------------")
print("document.txt saved")
print("Figures/diagrams extracted")
print("--------------------------------")