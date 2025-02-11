import time

from utils.chatbot import OpenAiQuery
from utils.textract import DocParser

start_time = time.time()

doc_parser = DocParser()
chatbot = OpenAiQuery()

file_path = "files\Balbec Bid (1_24_2025).docx"
parsed_data = doc_parser.extract_content(path=file_path)

for data in parsed_data:
    chatbot_response = chatbot.chat(query=data["content"])
    xml_data = chatbot_response.replace("```xml", "").replace("```", "").strip()
    xml_file_path = f'xml_output\\{data["file_name"]}.xml'

    with open(xml_file_path, "w", encoding="utf-8") as file:
        print(f'Chatbot response done. Creating the XML file: {data["file_name"]}')
        file.write(xml_data)

end_time = time.time()
total_time = round(end_time - start_time, 2)

if total_time < 60:
    print(f"Total processing time: {total_time} seconds")
else:
    minutes = int(total_time // 60)
    remaining_seconds = round(total_time % 60, 2)

    print(
        f"Total processing time: {minutes} {'minutes' if minutes > 1 else 'minute'} and {remaining_seconds} seconds"
    )
