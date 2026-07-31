import fitz
import os 

doc=fitz.open("knowledge/ncrt_book.pdf")

page=doc[0]
images=page.get_images()
for image in images:
    print(image[0])

xref=images[0][0]
image_data =doc.extract_image(xref)

print(type(image_data))
print(image_data.keys())
print(images)

output_folder="knowledge/extracted_images"
os.makedirs(output_folder, exist_ok=True)
image_bytes=image_data["image"]
image_extension=image_data['ext']
filename=f"page1.{image_extension}"

image_path=os.path.join(output_folder,filename)
with open(image_path, "wb") as file:
    file.write(image_bytes)
print("save", image_path)

#extracting all pdf images
for page_numbers in range(len(doc)):
    page=doc[page_numbers]
    images = page.get_images()

    print(f"page {page_numbers +1} has {len(images)} images")

    for image_index,image in enumerate(images):
        print(page_numbers+1,image_index+1)
