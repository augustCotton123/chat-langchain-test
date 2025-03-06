from langchain_community.document_loaders import JSONLoader

import json
from pathlib import Path
from pprint import pprint

from bs4 import BeautifulSoup

# function for removing html tags from the json file
def cleanup(element):
    if isinstance(element, list):
        for i, item in enumerate(element):
            element[i] = cleanup(item)
    elif isinstance(element, dict):
        for key in element.keys():
            element[key] = cleanup(element[key])
    elif isinstance(element, str):
        element = BeautifulSoup(element).get_text()
    return element

# cleaning the json file
file_path='./backend/VF-FCFS-202401-06.json'
data = json.loads(Path(file_path).read_text())
cleanup(data)

# save the cleaned json file
with open("./backend/vf_data_cleaned.json", "w") as outfile:
    json.dump(data, outfile)

# function for custom metadata
def metadata_func(record: dict, metadata: dict) -> dict:

    metadata["title"] = record.get("article_title")
    metadata["publish_date"] = record.get("publish_date")
    metadata["claim_author"] = record.get("claim_author")
    metadata["rating"] = record.get("rating")
    metadata["source"] = record.get("url")

    # if "source" in metadata:
    #     source = metadata["source"].split("/")
    #     source = source[source.index("langchain"):]
    #     metadata["source"] = "/".join(source)

    return metadata

# loader = JSONLoader(
#     file_path='./backend/vf_data_cleaned.json',
#     jq_schema='.[].data[] | {publish_date, url, rating, explanation, post_content}',
#     text_content=False
# )
loader = JSONLoader(
    file_path='./backend/vf_data_cleaned.json',
    jq_schema='.[].data[]',
    content_key="post_content",
    metadata_func=metadata_func
)

data = loader.load()
pprint(data)
