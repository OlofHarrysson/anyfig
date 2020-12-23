import inspect
import functools

from . import figutils
from .fields import InputField, InterfaceField


def cli_help(config_obj):
  ''' Returns string for config's cli-arguments with corresponding comments '''
  comments = extract_config_obj_comments(config_obj)

  indent_width = 4  # In spaces
  comment_indents = {}  # attribute-name=indent. key = '' for main config class
  formated_comments = []

  # Calculate comment indents
  for attribute_name, comment in comments.items():
    # Access nested value -> config.attribute.value
    attribute_names = attribute_name.split('.')
    attribute_value = functools.reduce(getattr, attribute_names, config_obj)

    # Formats the attribute string
    attribute_type = type(attribute_value).__name__
    if isinstance(attribute_value, InputField):
      attribute_type = str(attribute_value.type_pattern.__name__)
    elif isinstance(attribute_value, InterfaceField):
      attribute_type = type(attribute_value.value).__name__

    nested_level = attribute_name.count('.')
    nested_indent = ' ' * (indent_width * nested_level)
    attr_string = f"{nested_indent}--{attribute_name} ({attribute_type}):"

    # Save strings for further formating
    attribute_chain = '.'.join(attribute_names[:-1])
    formated_comments.append((attribute_chain, attr_string, comment))

    # Calculate even indention width
    n_spaces = len(attr_string) + indent_width
    if n_spaces > comment_indents.get(attribute_chain, -1):
      comment_indents[attribute_chain] = n_spaces

  # Adds indention based on which config class
  help_strings = []
  for attribute_chain, attr_string, comment in formated_comments:
    n_spaces = comment_indents[attribute_chain]
    comment = (' ' * n_spaces).join(comment.splitlines(True)).rstrip('\n')
    help_string = f"{attr_string}{' ' * (n_spaces - len(attr_string))}{comment}"
    help_strings.append(help_string)

  # Add header info
  cli_help_header = []
  config_classes = list(figutils.get_config_classes())
  if len(config_classes) > 1:
    header = (
      f"Current config is '{type(config_obj).__name__}'. Available config classes {config_classes}. "
      "Set config with --config=OtherConfigClass")
    cli_help_header.append(header)

  if help_strings:
    cli_help_header.append("{}The available input arguments are".format(
      '\n' if cli_help_header else ''))

  return '\n'.join(cli_help_header + help_strings)


def extract_config_obj_comments(config_obj):
  ''' Extracts comments for a config object and any config-class children objects '''
  config_classes = figutils.get_config_classes().values()
  comments = _extract_comments(type(config_obj))

  # Remove the keys that aren't allowed from command line input
  allowed_cli_args = figutils.get_allowed_cli_args(config_obj)
  comments = {k: v for k, v in comments.items() if k in allowed_cli_args}

  flat_comments = {}
  for attribute_name, comment in comments.items():
    flat_comments[attribute_name] = comment

    # Check if config class has config-class children
    attribute_value = getattr(config_obj, attribute_name)
    if type(attribute_value) in config_classes:
      child_comments = extract_config_obj_comments(attribute_value)

      # Add child comments
      for child_attribute_name, child_comment in child_comments.items():
        nested_name = f'{attribute_name}.{child_attribute_name}'
        flat_comments[nested_name] = child_comment

  return flat_comments


def _extract_comments(class_type):
  ''' Extracts comments for a config class '''
  comments = {}
  parents = class_type.__bases__

  # Find comments for parents, skip Python built in code
  for parent in parents:
    if parent.__module__ == 'builtins':
      continue
    parent_comments = _extract_comments(parent)
    comments.update(parent_comments)

  # Find attribute name and matching comment
  code_lines, _ = inspect.getsourcelines(class_type)
  for row_index, code_line in enumerate(code_lines):
    if code_line.lstrip().startswith('self.'):
      comment = _extract_comment(code_lines, row_index)

      # Extract attribute name
      attribute_name = code_line.split('=')[0]
      if ':' in attribute_name:
        attribute_name = attribute_name.split(':')[0]
      attribute_name = attribute_name.strip().replace('self.', '', 1)

      # Override parent comment
      if comment or attribute_name not in comments:
        comments[attribute_name] = comment

  return comments


def _extract_comment(code_lines, row_line_index):
  ''' Extracts an eventual source code comment directly above a row '''

  multiline_commet = False
  comment_lines = []
  for row_index in range(row_line_index, 0, -1):
    row_code = code_lines[row_index].strip(' ')

    # Break at blank line above attribute line
    if row_code.isspace() and not multiline_commet:
      break

    # Break if we reach an attribute
    if row_code.startswith('self.') and row_index != row_line_index:
      break

    # Starts with #
    if row_code.startswith('#'):
      comment_lines.insert(0, row_code)

    # Starts with ''' or """
    if multiline_commet and (row_code.startswith("'''")
                             or row_code.startswith('"""')):
      comment_lines.insert(0, row_code)
      break

    # Line between ''' or """
    if multiline_commet:
      comment_lines.insert(0, row_code)

    # Ends with ''' or """
    if row_code.rstrip().endswith("'''") or row_code.rstrip().endswith('"""'):
      comment_lines.insert(0, row_code)
      multiline_commet = True

  comment_string = ''.join(comment_lines).strip("# \n'\"")
  return comment_string
