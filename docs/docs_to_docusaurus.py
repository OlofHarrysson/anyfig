#!/usr/bin/env python3
"""
Takes the output from Sphinx, clean it and send it to Docusaurus.

1. Get four main modules from _build/html/
    - Extract only the 'body' html and store it as a md file under 
            ./website/docs/api-{module_name}.md

2. Get all files under _build/html/api/
    - Extract 'body' html and store it as a md file under
            ./website/docs/api/{filenames}.md

3. Update 'sidebars.json' with the new markdown files
    - Update the 'api' section.
    - Add each module under a sub-directory.
"""
"""
Takes all relevant html files from the html output sphinx folder, parse it with Beautifulsoup, remove unnecessary html data (such as <head>) and
save a markdown file.
"""

from bs4 import BeautifulSoup
import glob
from pathlib import Path
from typing import List
import re
import json
import inspect
import anyfig
from collections import defaultdict
"""
PARAMETERS
"""

# MODULES = ["figutils", "config_functions"]
# MODULES = ["_autosummary"]
ROOT_HTML_DIRECTORY = "./build/html"
ROOT_MD_DIRECTORY = "../website/docs"
# TODO: Check that they exist


def get_content(soup):
  return soup.find("div", {"class": "body"}).find("div")


def add_docusaurus_metadata(content: str,
                            id: str,
                            title: str,
                            hide_title=False) -> str:
  return f"---\nid: {id}\ntitle: {title}\nhide_title: {hide_title}\n---\n\n" + content


def convert_to_docusaurus(soup):
  # Fix link
  for a in soup.find_all("a", {"class": "reference internal"}, href=True):
    module_member = a["href"].split('.html')[0]
    module, member = module_member.rsplit('.', 1)
    module = module.replace('anyfig.', '')
    a["href"] = f'{module}#{member}'

  # Fix table of content
  title = soup.find("h1").extract().text.replace('¶', '')
  doc = f"\n## {title}\n{soup}"

  # Fix syntax errors
  doc = doc.replace('class=', 'className=')
  doc = doc.replace('<col style="width: 10%"/>\n<col style="width: 90%"/>', '')
  return doc


def to_md(in_html_filepath: str, out_md_filepath: str, id: str, title: str,
          hide_title: str) -> None:
  with open(in_html_filepath, "r") as f:
    soup = BeautifulSoup(f.read(), "html.parser")
    body = get_content(soup)

  with open(out_md_filepath, "w") as f:
    content = add_docusaurus_metadata(str(body), id, title, hide_title)
    f.write(content)


def convert_modules(ROOT_HTML_DIRECTORY, ROOT_MD_DIRECTORY):
  html_modules = []

  for module_filepath in ROOT_HTML_DIRECTORY.iterdir():
    module_name = module_filepath.name
    content = []
    for html_file in module_filepath.glob('**/*.html'):
      if html_file.stem == f'anyfig.{module_name}':
        html_modules.append(html_file)
        continue  # Summary of the module

      id_ = html_file.stem
      title = id_
      hide_title = "false"

      with open(html_file) as f:
        soup = BeautifulSoup(f.read(), "html.parser")

      body = get_content(soup)
      a = body.find("a", {"class": "reference internal"})
      release = '0.2.0'  # TODO
      module = eval(id_)
      line_number = inspect.findsource(module)[1] + 1
      url = f"https://github.com/OlofHarrysson/anyfig/blob/{release}/anyfig/{module_name}#L{line_number}"
      a['href'] = url

      # Fix table of content
      title = body.find("h1").extract().text.replace('¶', '').split('.')[-1]
      print(title)
      body = f"\n## {title}\n{body}"

      content.append(str(body))

    content = '\n'.join(content)
    content = add_docusaurus_metadata(content, module_name, module_name,
                                      hide_title)
    out_md_filename = f"{ROOT_MD_DIRECTORY}/api/{module_name}.mdx"
    with open(out_md_filename, "w") as f:
      f.write(content)
  return html_modules


def convert_root(html_modules, ROOT_MD_DIRECTORY):
  module_content = []
  for html_filepath in html_modules:

    with open(html_filepath) as f:
      soup = BeautifulSoup(f.read(), "html.parser")
      soup = get_content(soup)
      doc = convert_to_docusaurus(soup)

    module_content.append(doc)

  out_md_filename = f"{ROOT_MD_DIRECTORY}/api/anyfig.mdx"
  with open(out_md_filename, "w") as f:
    content = '\n'.join(module_content)
    content = add_docusaurus_metadata(content,
                                      id='api-reference',
                                      title='API Reference')
    f.write(content)


def get_module_names(MODULE_SOURCE_DIR):
  module_names = [f.stem for f in MODULE_SOURCE_DIR.glob('**/*.html')]
  module_names.remove('anyfig')  # TODO
  module_names.remove('index')  # TODO
  return module_names


def main():
  ROOT_HTML_DIRECTORY = Path("./build/html/_autosummary")
  MODULE_SOURCE_DIR = ROOT_HTML_DIRECTORY / '../_modules'
  ROOT_MD_DIRECTORY = "../website/docs"  # TODO: Change to pathlib __file__
  module_names = get_module_names(MODULE_SOURCE_DIR)

  # make sure folder exists
  Path(ROOT_MD_DIRECTORY + "api").mkdir(parents=True, exist_ok=True)
  Path(ROOT_MD_DIRECTORY + "api/source").mkdir(parents=True, exist_ok=True)

  module_dir = Path(ROOT_HTML_DIRECTORY) / '_autosummary'
  html_modules = convert_modules(ROOT_HTML_DIRECTORY, ROOT_MD_DIRECTORY)
  convert_root(html_modules, ROOT_MD_DIRECTORY)


if __name__ == '__main__':
  main()
