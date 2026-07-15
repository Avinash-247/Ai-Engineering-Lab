'''import layoutparser as lp
import cv2
import os
from pdf2image import convert_from_path
import numpy as np

PDF_PATH = "./knowledgebase/book/book_paper.pdf"

OUTPUT_FOLDER = "./knowledgebase/extracted/images"

os.makedirs(
    OUTPUT_FOLDER,
    exist_ok=True
)

# ------------------------------------
# Load pretrained document model
# ------------------------------------

model = lp.Detectron2LayoutModel(
    config_path=
    "lp://PubLayNet/faster_rcnn_R_50_FPN_3x/config",

    label_map={
        0: "Text",
        1: "Title",
        2: "List",
        3: "Table",
        4: "Figure"
    },

    extra_config=[
        "MODEL.ROI_HEADS.SCORE_THRESH_TEST",
        0.8
    ]
)

# ------------------------------------
# Convert PDF pages to images
# ------------------------------------

pages = convert_from_path(
    PDF_PATH,
    dpi=300
)

for page_number, page in enumerate(pages):

    image = np.array(page)

    layout = model.detect(image)

    figure_counter = 1

    for block in layout:

        if block.type in [
            "Figure",
            "Table"
        ]:

            x1 = int(block.block.x_1)
            y1 = int(block.block.y_1)
            x2 = int(block.block.x_2)
            y2 = int(block.block.y_2)

            cropped = image[
                y1:y2,
                x1:x2
            ]

            filename = (
                f"page_"
                f"{page_number+1}"
                f"_figure_"
                f"{figure_counter}.png"
            )

            path = os.path.join(
                OUTPUT_FOLDER,
                filename
            )

            cv2.imwrite(
                path,
                cv2.cvtColor(
                    cropped,
                    cv2.COLOR_RGB2BGR
                )
            )

            print(
                f"Saved {filename}"
            )

            figure_counter += 1

print(
    "Extraction completed."
)'''
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

# --------------------------------------------------------
# CONFIGURATION
# --------------------------------------------------------

MIN_WIDTH = 150
MIN_HEIGHT = 150

MAX_PAGE_COVERAGE = 0.70
ZOOM_FACTOR = 3

# --------------------------------------------------------
# PROCESS PAGES
# --------------------------------------------------------

for page_number in range(len(doc)):

    page = doc.load_page(page_number)

    page_width = page.rect.width
    page_height = page.rect.height
    page_area = page_width * page_height

    # =====================================================
    # TEXT EXTRACTION
    # =====================================================

    text = page.get_text()

    all_text += (
        f"\n\n"
        f"========== PAGE {page_number + 1} ==========\n\n"
    )

    all_text += text

    # =====================================================
    # EMBEDDED IMAGE EXTRACTION
    # =====================================================

    image_list = page.get_images(full=True)

    for img in image_list:

        try:
            xref = img[0]

            base_image = doc.extract_image(xref)

            image_bytes = base_image["image"]
            image_ext = base_image["ext"]

            if len(image_bytes) < 5000:
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

    # =====================================================
    # VECTOR DIAGRAM EXTRACTION
    # =====================================================

    drawings = page.get_drawings()

    for drawing_id, drawing in enumerate(drawings):

        rect = drawing["rect"]

        width = rect.width
        height = rect.height

        area = width * height

        # Ignore tiny lines and decorations
        if width < MIN_WIDTH:
            continue

        if height < MIN_HEIGHT:
            continue

        # Ignore almost entire page captures
        if area > page_area * MAX_PAGE_COVERAGE:
            continue

        clip = pymupdf.Rect(
            rect.x0,
            rect.y0,
            rect.x1,
            rect.y1
        )

        try:

            pix = page.get_pixmap(
                matrix=pymupdf.Matrix(
                    ZOOM_FACTOR,
                    ZOOM_FACTOR
                ),
                clip=clip,
                alpha=False
            )

            # Ignore white images
            samples = pix.samples

            if len(set(samples[:1000])) <= 1:
                continue

            filename = (
                f"page_{page_number+1}"
                f"_vector_{drawing_id+1}.png"
            )

            save_path = os.path.join(
                IMAGE_OUTPUT_FOLDER,
                filename
            )

            pix.save(save_path)

            print(f"Saved {filename}")

        except Exception:
            pass

# =====================================================
# SAVE TEXT FILE
# =====================================================

with open(
    TEXT_OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:
    f.write(all_text)

print("\n--------------------------------")
print("Text extraction completed.")
print("Image extraction completed.")
print("--------------------------------")