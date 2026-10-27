"""Arxiv Curator - Shared utilities for LLMOps Course on Databricks"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("arxiv-curator")  # must match `name` in pyproject.toml
except PackageNotFoundError:  # running from source without the package installed
    __version__ = "unknown"
