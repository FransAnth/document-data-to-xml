import json
import os

import boto3
from dotenv import load_dotenv

load_dotenv()

ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
SECRET_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

from utils.pdf_manager import PDFManager


class DocParser:

    def __init__(self):

        self.textract = boto3.client(
            "textract",
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY,
        )
        self.collected_table_text = []

    def extract_content(self, path):
        print("Content extraction started")
        doc_extension = path.split(".")[-1]
        file_name = path.split("\\")[-1].split(".")[0]

        data = []

        try:
            if doc_extension in ["png", "jpg"]:
                table_data = self.get_image_content(path=path)
                data.append({"file_name": file_name, "content": table_data})

            elif doc_extension == "pdf":
                pdf_manager = PDFManager()
                image_paths = pdf_manager.convert_pages_to_images(file_path=path)

                for image_path in image_paths:
                    name = image_path.split("\\")[-1].split(".")[0]
                    table_data = self.get_image_content(path=image_path)

                    data.append({"file_name": name, "content": table_data})
        except Exception as e:
            print(f"ERROR: {e}")

        return data

    def get_image_content(self, path):
        print(f"Getting image content: {path}")
        # Open your document (PDF or image)
        with open(path, "rb") as document:
            image_bytes = document.read()

        # Checking if the file size is below 5mb: analyze_document has a limit of 5MB for local files
        file_size_bytes = os.path.getsize(path)
        file_size_mb = file_size_bytes / (1024 * 1024)

        if file_size_mb > 5:
            raise Exception(
                f"File size ({file_size_mb:.2f} MB) exceeds Textract's 5MB limit. File: {path}"
            )

        # Use analyze_document instead of detect_document_text
        response = self.textract.analyze_document(
            Document={"Bytes": image_bytes},
            FeatureTypes=[
                "TABLES",
                "FORMS",
            ],  # This is valid only with analyze_document
        )

        image_table_data = self.extract_table_data(response)
        image_check_boxes = self.extract_checkboxes(response)
        image_lines = self.extract_lines(response)

        image_data = image_lines + "\n" + image_check_boxes + "\n" + image_table_data

        with open("aws_content.txt", "w", encoding="utf-8") as file:
            file.write(str(json.dumps(response["Blocks"], indent=4)))

        print("IMAGE DATA")
        print(image_data)

        return image_data

    def get_text_for_cell(
        self, cell, blocks_map
    ):  # Function to extract text from a cell
        text = ""
        if "Relationships" in cell:
            for relationship in cell["Relationships"]:
                if relationship["Type"] == "CHILD":
                    for child_id in relationship["Ids"]:
                        word = blocks_map[child_id]
                        if word["BlockType"] == "WORD":
                            text += word["Text"] + " "
        return text.strip()

    def extract_table_data(self, response_data):
        # Create a map of blocks
        blocks_map = {block["Id"]: block for block in response_data["Blocks"]}
        table_data = ""
        page_data = []

        # Loop through the blocks and reconstruct the table
        for data in response_data["Blocks"]:
            if data["BlockType"] == "TABLE":
                table_data += "\n--- Table Data ---\n"
                current_table_data = self.process_table_data(
                    data, blocks_map, format="csv"
                )

                if current_table_data == None:
                    current_table_data = self.process_table_data(data, blocks_map)

                table_data += current_table_data + "\n"

            page_data.append(data)

        with open("aws_content.txt", "w", encoding="utf-8") as file:
            file.write(str(json.dumps(page_data, indent=4)))
        return table_data

    def process_table_data(self, data, blocks_map, format=None):
        current_table_data = ""
        for relationship in data["Relationships"]:
            if relationship["Type"] == "CHILD":
                row_index = 1  # initial row position
                col_index = 1  # initial col position
                for cell_id in relationship["Ids"]:
                    cell = blocks_map[cell_id]
                    if cell["BlockType"] == "CELL":

                        row = cell["RowIndex"]
                        col = cell["ColumnIndex"]
                        cell_text = self.get_text_for_cell(cell, blocks_map)

                        if format == "csv":
                            if row == row_index:
                                if row == 1 and cell_text.strip() == "":
                                    pass
                                else:
                                    current_table_data += f'"{cell_text}",'
                            else:
                                current_table_data = current_table_data.rstrip(",")
                                current_table_data += f'\n"{cell_text}",'

                            self.collected_table_text.append(cell_text)
                            row_index = row
                            col_index = col

                            # checking if the row and col are in a proper arrangement
                            # print(col - 1)
                            # print(col_index)
                            # if (
                            #     (row == row_index and (col - 1 != col_index))
                            #     or (row != row_index and col != 1)
                            #     or (row - 1 != row_index)
                            # ):
                            #     print(row == row_index and (col - 1 != col_index))
                            #     print(row != row_index and col != 1)
                            #     print(row - 1 != row_index)
                            #     print(
                            #         f"INVALID TABLE ROW AND COL {row}, {col}, {row_index}, {col_index}"
                            #     )
                            #     return None

                        else:
                            current_table_data += (
                                f"Row {row}, Column {col}: {cell_text}\n"
                            )

                current_table_data = current_table_data.rstrip(",")

        return current_table_data

    def extract_lines(self, response_data):
        lines = ""

        for data in response_data["Blocks"]:
            if data["BlockType"] == "LINE":
                text = data["Text"]
                if text not in self.collected_table_text:
                    x = round(data["Geometry"]["BoundingBox"]["Left"], 2)
                    y = round(data["Geometry"]["BoundingBox"]["Top"], 2)
                    lines += f"{text} [Axis(x,y): ({x},{y})]\n"

        if lines != "":
            lines = "--- Extracted lines ---\n" + lines

        return lines

    def extract_checkboxes(self, response_data):
        checkboxes = ""

        for data in response_data["Blocks"]:
            if data["BlockType"] == "SELECTION_ELEMENT":
                x = round(data["Geometry"]["BoundingBox"]["Left"], 2)
                y = round(data["Geometry"]["BoundingBox"]["Top"], 2)
                check_boxes += (
                    f"Check Box: {data['SelectionStatus']} [Axis(x,y): ({x},{y})]\n"
                )

        if checkboxes != "":
            checkboxes = "--- Extracted Checkboxes ---\n" + checkboxes

        return checkboxes


if __name__ == "__main__":
    doc_parser = DocParser()
    doc_parser.extract_content(path="images\sample_page_image.png")
