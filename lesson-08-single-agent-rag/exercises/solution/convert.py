import os
import requests

docs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")
md_files = [f for f in os.listdir(docs_dir) if f.endswith(".md")]

for md_file in md_files:
    md_file_path = os.path.join(docs_dir, md_file)
    pdf_file_path = os.path.join(docs_dir, md_file.replace(".md", ".pdf"))

    with open(md_file_path, "r") as f:
        md_content = f.read()

    headers = {"Content-Type": "text/markdown"}
    response = requests.post("https://md-to-pdf.fly.dev", data=md_content.encode('utf-8'), headers=headers)

    if response.status_code == 200:
        with open(pdf_file_path, "wb") as f:
            f.write(response.content)
        print(f"Successfully converted {md_file} to {os.path.basename(pdf_file_path)}")
    else:
        print(f"Error converting {md_file}: {response.status_code} - {response.text}")
