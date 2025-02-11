import os

from pdf2image import convert_from_path


class PDFManager:
    def __init__(self):
        self.output_folder = "images\output"
        # Ensure output directory exists
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def convert_pages_to_images(self, file_path):
        file = file_path.split("\\")[-1]
        file_name = file.split(".")[0]

        print(f"Processing images for file: {file}")

        # Convert PDF to Images
        pages = convert_from_path(
            file_path, 350, poppler_path="C:\poppler-23.11.0\Library\\bin"
        )

        image_paths = []
        for i, page in enumerate(pages, start=1):
            image_name = f"{self.output_folder}\{i}_{file_name}.png"
            page.save(image_name, "PNG")
            image_paths.append(image_name)

        print(f"Done processing images. Saved {len(image_paths)} images.")

        return image_paths
