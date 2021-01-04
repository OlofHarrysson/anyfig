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
    a["href"] = a["href"].split('.html')[0]

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


def convert_modules(members, ROOT_MD_DIRECTORY):

  for rel_source_file, html_files in members.items():
    # out_md_filename = f"{ROOT_MD_DIRECTORY}/api/{html_file.stem}.mdx"
    content = []
    for html_file in html_files:
      id_ = html_file.stem
      title = id_

      # Create one page per file. Group them

      hide_title = "false"
      # to_md(html_file, out_md_filename, id_, title, hide_title)

      with open(html_file, "r") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

      body = get_content(soup)
      a = body.find("a", {"class": "reference internal"})
      release = '0.2.0'  # TODO
      module = eval(id_)
      line_number = inspect.findsource(module)[1] + 1
      # source_file = Path(inspect.getfile(module))
      # root_source = Path(inspect.getfile(anyfig)).parent
      # rel_source_file = source_file.relative_to(root_source)
      url = f"https://github.com/OlofHarrysson/anyfig/blob/{release}/anyfig/{rel_source_file}#L{line_number}"
      a['href'] = url

      print(html_file, rel_source_file)
      content.append(str(body))

    name = rel_source_file.stem
    content = '\n'.join(content)
    content = add_docusaurus_metadata(content, name, name, hide_title)
    out_md_filename = f"{ROOT_MD_DIRECTORY}/api/{name}.mdx"
    print(out_md_filename)
    with open(out_md_filename, "w") as f:
      f.write(content)

  # with open(out_md_filename, "w") as f:
  #   content = add_docusaurus_metadata(str(body), id_, title, hide_title)
  #   f.write(content)

  # for name, content in file_to_content.items():
  #   print(name)
  #   content = '\n'.join(content)
  #   content = add_docusaurus_metadata(content, name, name, hide_title)
  #   out_md_filename = f"{ROOT_MD_DIRECTORY}/api/{name}.mdx"
  #   print(out_md_filename)
  #   with open(out_md_filename, "w") as f:
  #     f.write(content)


def convert_root(module_dir, ROOT_MD_DIRECTORY, module_names):
  module_content = []
  for module_name in module_names:
    if module_name == 'anyfig':
      html_path = module_dir / 'anyfig.html'
    else:
      html_path = module_dir / f'anyfig.{module_name}.html'

    with open(html_path) as f:
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


# def convert_source(MODULE_SOURCE_DIR, ROOT_MD_DIRECTORY):
#   for in_html_filename in MODULE_SOURCE_DIR.glob('**/*.html'):
#     if str(in_html_filename).endswith('index.html'):
#       continue

#     out_md_filename = f"{ROOT_MD_DIRECTORY}/api/source/{in_html_filename.stem}.mdx"
#     id_ = in_html_filename.stem
#     title = id_

#     hide_title = "true"
#     # to_md(in_html_filename, out_md_filename, id_, title, hide_title)
#     import html

#     with open(in_html_filename) as f:
#       text = f.read()
#       body = html.escape(text)
#       # text.replace('&quot;', '&-quot')
#       # soup = BeautifulSoup(text, "html.parser")
#       # body = get_content(soup)

#       # for t in body.findAll(text=True):
#       #   text = t.replace('\\', '&bsol;')
#       #   t.replaceWith(html.escape(text))

#       body = str(body)
#       body = body.replace('&amp;', '&')

#       # Fix syntax errors
#       body = body.replace('class=', 'className=')
#       # body = body.replace(
#       #   '<col style="width: 10%"/>\n<col style="width: 90%"/>', '')
#       # body = body.replace('"', '&quot;').replace("'", "&apos;")

#     with open(out_md_filename, "w") as f:
#       content = add_docusaurus_metadata(str(body), id_, title, hide_title)
#       f.write(content)


def get_module_names(MODULE_SOURCE_DIR):
  module_names = [f.stem for f in MODULE_SOURCE_DIR.glob('**/*.html')]
  module_names.remove('index')
  module_names.remove('anyfig')  # TODO
  return module_names


def main():
  ROOT_HTML_DIRECTORY = Path("./build/html")
  MODULE_SOURCE_DIR = ROOT_HTML_DIRECTORY / '_modules'
  ROOT_MD_DIRECTORY = "../website/docs"  # TODO: Change to pathlib __file__
  module_names = get_module_names(MODULE_SOURCE_DIR)

  # make sure folder exists
  Path(ROOT_MD_DIRECTORY + "api").mkdir(parents=True, exist_ok=True)
  Path(ROOT_MD_DIRECTORY + "api/source").mkdir(parents=True, exist_ok=True)

  module_dir = Path(ROOT_HTML_DIRECTORY) / '_autosummary'

  html_files = list(module_dir.glob('*.html'))
  html_files = [p for p in html_files if 'dummyfields' not in p.stem]

  modules = []
  members = defaultdict(list)
  for html_file in html_files:
    if 'dummyfields' in html_file.stem:
      continue

    if html_file.stem == 'anyfig':
      modules.append(html_file)

    module = eval(html_file.stem)
    source_file = Path(inspect.getfile(module))
    root_source = Path(inspect.getfile(anyfig)).parent
    rel_source_file = source_file.relative_to(root_source)
    # print(f'anyfig.{rel_source_file.stem}' == html_file.stem,
    # rel_source_file.stem, html_file.stem)
    if f'anyfig.{rel_source_file.stem}' == html_file.stem:
      modules.append(html_file)
    else:
      members[rel_source_file].append(html_file)

  # Remove modules, keep memebers # TODO
  # html_files = [p for p in html_files if 'dummyfields' not in p.stem]
  # print(html_files)
  # print(module_names)

  # convert_source(MODULE_SOURCE_DIR, ROOT_MD_DIRECTORY)
  convert_modules(members, ROOT_MD_DIRECTORY)
  convert_root(module_dir, ROOT_MD_DIRECTORY, module_names)


if __name__ == '__main__':
  main()
