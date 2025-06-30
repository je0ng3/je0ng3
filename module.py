import os
from bs4 import BeautifulSoup
import re


def get_summary_content(filename):
    with open(filename, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    summary_header = soup.find("h2", string="Summary")
    if not summary_header:
        return ""

    summary_parts = []
    for sibling in summary_header.find_next_siblings():
        if sibling.name == "br":
            break
        summary_parts.append(str(sibling))

    return "\n".join(summary_parts).strip()


def get_folders_with_summary(base_path):
    result = []
    if not os.path.exists(base_path):
        return result

    folders = []
    for folder in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder)
        index_file = os.path.join(folder_path, "index.html")
        if os.path.isdir(folder_path) and os.path.isfile(index_file):
            folders.append(folder)

    for folder in sorted(folders):
        folder_path = os.path.join(base_path, folder)
        index_file = os.path.join(folder_path, "index.html")
        summary = get_summary_content(index_file)
        result.append(
            {
                "title": folder,
                "path": f"/{base_path}/{folder}/index.html",
                "summary": summary,
            }
        )
    return result
