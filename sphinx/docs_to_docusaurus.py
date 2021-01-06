# Takes the output from Sphinx, clean it and send it to Docusaurus.

from bs4 import BeautifulSoup
import glob
from pathlib import Path
from typing import List
import re
import json
import inspect
import anyfig
from collections import defaultdict


def main():
  ROOT_HTML_DIRECTORY = Path("./build/html/_autosummary")
  ROOT_MD_DIRECTORY = Path("../website/docs")

  # make sure folder exists
  Path(ROOT_MD_DIRECTORY / "api").mkdir(parents=True, exist_ok=True)
  Path(ROOT_MD_DIRECTORY / "api/source").mkdir(parents=True, exist_ok=True)

  html_modules = convert_modules(ROOT_HTML_DIRECTORY, ROOT_MD_DIRECTORY)
  convert_root(html_modules, ROOT_MD_DIRECTORY)


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


def fix_document(soup):
  soup = str(soup).replace('¶', '')

  # Fix syntax errors
  soup = soup.replace('class=', 'className=')
  soup = soup.replace('<col style="width: 10%"/>\n<col style="width: 90%"/>',
                      '')
  return soup


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
      # print(body)
      print(html_file.stem)
      func_defs = body.find_all('dt')
      for func_def in func_defs:
        # Add class
        if not func_def.get("class"):
          func_def['class'] = 'function-definition'

        # Code tag -> span
        for code_block in func_def.find_all('code'):
          code_block.name = 'span'

      # qwe
      source_link = body.find("a", {"class": "reference internal"})
      release = 'master'  # TODO: Change to latest release instead?
      module = eval(id_)
      line_number = inspect.findsource(module)[1] + 1
      url = f"https://github.com/OlofHarrysson/anyfig/blob/{release}/anyfig/{module_name}.py#L{line_number}"
      source_link['href'] = url

      # Fix table of content
      title = body.find("h1").extract().text.replace('¶', '').split('.')[-1]
      # print(title)
      body = f"\n## {title}\n{body}"
      body = str(body).replace('¶', '')
      body = body.replace('reference internal',
                          'reference internal source-link')

      content.append(body)

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


if __name__ == '__main__':
  main()
