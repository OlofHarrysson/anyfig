# Takes the output from Sphinx, clean it and send it to Docusaurus.

from bs4 import BeautifulSoup
from pathlib import Path
import inspect
import anyfig  # Needed for eval


def main():
  ROOT_HTML_DIRECTORY = Path("./build/html/_autosummary")
  ROOT_MD_DIRECTORY = Path("../website/docs")

  # make sure folder exists
  Path(ROOT_MD_DIRECTORY / "api").mkdir(parents=True, exist_ok=True)
  Path(ROOT_MD_DIRECTORY / "api/source").mkdir(parents=True, exist_ok=True)

  html_modules = convert_modules(ROOT_HTML_DIRECTORY, ROOT_MD_DIRECTORY)
  convert_root(html_modules, ROOT_MD_DIRECTORY)


def convert_modules(ROOT_HTML_DIRECTORY, ROOT_MD_DIRECTORY):
  module_paths = []

  for module_filepath in ROOT_HTML_DIRECTORY.iterdir():
    module_name = module_filepath.name
    content = []
    for html_file in module_filepath.glob('**/*.html'):
      if html_file.stem == f'anyfig.{module_name}':
        module_paths.append(html_file)
        continue

      soup = read_content(html_file)
      func_defs = soup.find_all('dt')
      for func_def in func_defs:
        func_def['class'] = 'function-definition'

        # Code tag -> span
        for code_block in func_def.find_all('code'):
          code_block.name = 'span'

        # Change source link to Github
        func_name = func_def.get('id')
        if func_name:
          source_link = func_def.find("a", {"class": "reference internal"})
          release = 'master'  # TODO: Change to latest release instead?
          func = eval(func_name)
          line_number = inspect.findsource(func)[1] + 1
          url = f"https://github.com/OlofHarrysson/anyfig/blob/{release}/anyfig/{module_name}.py#L{line_number}"
          source_link['href'] = url
          source_link['class'] = 'reference internal source-link'

      soup = fix_document(soup)
      content.append(soup)

    content = '\n'.join(content)
    out_md_filename = f"{ROOT_MD_DIRECTORY}/api/{module_name}.mdx"
    write_markdown(out_md_filename,
                   content,
                   md_id=module_name,
                   title=module_name)
  return module_paths


def convert_root(html_modules, ROOT_MD_DIRECTORY):
  module_content = []
  for html_filepath in html_modules:
    soup = read_content(html_filepath)
    soup = convert_internal_link(soup)
    soup = fix_document(soup)
    module_content.append(soup)

  out_md_filename = f"{ROOT_MD_DIRECTORY}/api/anyfig.mdx"
  content = '\n'.join(module_content)
  write_markdown(out_md_filename,
                 content,
                 md_id='api-reference',
                 title='API Reference')


def convert_internal_link(soup):
  for a in soup.find_all("a", {"class": "reference internal"}, href=True):
    module_member = a["href"].split('.html')[0]
    module, member = module_member.rsplit('.', 1)
    module = module.replace('anyfig.', '')
    a["href"] = f'{module}#{member}'

  return soup


def read_content(html_filepath):
  with open(html_filepath) as f:
    soup = BeautifulSoup(f.read(), "html.parser")
  return soup.find("div", {"class": "body"}).find("div")


def add_docusaurus_metadata(content, md_id, title):
  return f"---\nid: {id}\ntitle: {title}\n---\n\n" + content


def write_markdown(md_filepath, content, md_id, title):
  with open(md_filepath, "w") as f:
    content = add_docusaurus_metadata(content,
                                      md_id='api-reference',
                                      title='API Reference')
    f.write(content)


def fix_document(soup):
  title = soup.find("h1").extract().text.replace('¶', '').split('.')[-1]
  soup = f"\n## {title}\n{soup}"
  soup = soup.replace('¶', '')

  # Fix syntax errors
  soup = soup.replace('class=', 'className=')
  soup = soup.replace('<col style="width: 10%"/>\n<col style="width: 90%"/>',
                      '')
  return soup


if __name__ == '__main__':
  main()
