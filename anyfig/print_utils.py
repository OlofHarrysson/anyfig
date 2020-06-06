import inspect
import functools

from . import figutils


def comments_string(config_obj):
  ''' Returns a "help" string for the config object that contain attributes and any matching comments '''
  comments = _extract_config_obj_comments(config_obj)

  indent_width = 4  # In spaces
  comment_indents = {}  # attribute-name=indent. key = '' for main config class
  formated_comments = []

  # Calculate comment indents
  for attribute_name, comment in comments.items():
    # Access nested value -> config.attribute.value
    attribute_names = attribute_name.split('.')
    attribute_value = functools.reduce(getattr, attribute_names, config_obj)

    # Formats the attribute string
    attribute_type = attribute_value.__class__.__name__
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

  return '\n'.join(help_strings)


def _extract_config_obj_comments(config_obj):
  ''' Extracts comments for a config object and any config-class children objects '''
  config_classes = figutils.get_config_classes().values()
  config_class = config_obj.__class__
  comments = _extract_comments(config_class)

  flat_comments = {}
  for attribute_name, comment in comments.items():
    flat_comments[attribute_name] = comment

    # Check if config class has config-class children
    attribute_value = getattr(config_obj, attribute_name)
    if attribute_value.__class__ in config_classes:
      child_comments = _extract_config_obj_comments(attribute_value)

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
