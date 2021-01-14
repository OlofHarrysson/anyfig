#!/usr/bin/env python
"""Tests for `anyfig` package."""

import pytest
import anyfig
from dataclasses import FrozenInstanceError

import conftest  # Config class fixtures


def test_types(main_config):
  config = anyfig.init_config(default_config=main_config, cli_args={})
  assert type(config.int_var) == int
  assert type(config.float_var) == float
  assert type(config.string_var) == str


def test_duplicate_config_name(main_config):
  with pytest.raises(AssertionError):

    @anyfig.config_class()
    class MainConfig:
      pass


class TestFrozenConfig:
  def test_init(self, main_config):
    anyfig.init_config(default_config=main_config, cli_args={})

  def test_frozen(self, main_config):
    config = anyfig.init_config(default_config=main_config, cli_args={})
    with pytest.raises(FrozenInstanceError):
      config.int_var = 2

  def test_unfreeze(self, main_config):
    config = anyfig.init_config(default_config=main_config, cli_args={})
    config.frozen(False).int_var = 2

  def test_refreeze(self, main_config):
    config = anyfig.init_config(default_config=main_config, cli_args={})
    with pytest.raises(FrozenInstanceError):
      config.frozen(False).frozen().int_var = 2

  def test_nested(self, main_config):
    config = anyfig.init_config(default_config=main_config, cli_args={})
    with pytest.raises(FrozenInstanceError):
      config.innerfig.inner = 'new'

    config.frozen(False).innerfig.inner = 'new'
    config.frozen().innerfig.frozen(False).inner = 'new'
