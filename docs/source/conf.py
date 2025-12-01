import os
import sys

# -- Path to project ----------------------------------------------------------
current_dir = os.path.dirname(os.path.abspath(__file__))  # docs/source
docs_dir = os.path.dirname(current_dir)                   # docs
project_root = os.path.dirname(docs_dir)                  # Корень проекта

# Добавляем корень проекта в sys.path
sys.path.insert(0, project_root)

# -- Project information -----------------------------------------------------
project = 'PatInfo'
copyright = '2025, Denis Kolodin'
author = 'Denis Kolodin'
release = 'v1.0.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.coverage',
]

# Настройки Napoleon для Google Style
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_param = True
napoleon_use_rtype = True

templates_path = ['_templates']
exclude_patterns = []
language = 'ru'

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
