#!/usr/bin/env python
"""Tests for `anyfig` package."""

import pytest
import anyfig
from datetime import datetime

# import configs

# from configs import MainConfig
from configs import main_config


def test_types(main_config):
  config = anyfig.init_config(default_config=main_config, cli_args={})
  assert type(config.int_var) == int
  assert type(config.float_var) == float
  assert type(config.string_var) == str


def test_duplicate_name(main_config):
  with pytest.raises(AssertionError):

    @anyfig.config_class()
    class MainConfig:
      pass


# @pytest.mark.parametrize('tester_arg', [datetime, datetime])
# def test_build_args(target_config):
#   config = anyfig.init_config(default_config=main_config, cli_args={})
#   print(config)

# TODO: Test that checks that get_parameters() get the expexted params. When I add more default attributes I also need to change that function
