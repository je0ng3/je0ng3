from flask import Flask, render_template, send_from_directory
from module import get_folders_with_summary
from jinja2 import Environment, FileSystemLoader
import os, sys
import shutil

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route("/career/<path:folder>/index.html")
def serve_career_index(folder):
    return send_from_directory(f"career/{folder}", "index.html")


@app.route("/project/<path:folder>/index.html")
def serve_project_index(folder):
    return send_from_directory(f"project/{folder}", "index.html")


@app.route("/")
def index():
    data = {
        "career_files": get_folders_with_summary("career"),
        "project_files": get_folders_with_summary("project"),
    }
    return render_template("index.html", data=data)


def generate_static_pages():

    OUTPUT_DIR = "docs"
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # static 폴더 복사
    if os.path.exists(os.path.join(OUTPUT_DIR, "static")):
        shutil.rmtree(os.path.join(OUTPUT_DIR, "static"))
    shutil.copytree("static", os.path.join(OUTPUT_DIR, "static"))

    # Jinja 템플릿 수동 렌더링
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("index.html")

    context = {
        "career_files": get_folders_with_summary("career"),
        "project_files": get_folders_with_summary("project"),
    }

    rendered = template.render(data=context)
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(rendered)

    print("index.html 생성 완료")

    # career와 project 폴더의 하위 index.html 복사
    for base in ["career", "project"]:
        folders = context[f"{base}_files"]
        for folder in folders:
            src = os.path.join(base, folder["title"], "index.html")
            dst_dir = os.path.join(OUTPUT_DIR, base, folder["title"])
            os.makedirs(dst_dir, exist_ok=True)
            shutil.copy(src, os.path.join(dst_dir, "index.html"))
            print(f"복사됨: {src} → {dst_dir}/index.html")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        generate_static_pages()
    else:
        app.run(debug=True)
