# Configuration file for the Sphinx documentation builder.

import os
import sys

# Allows to import modules from the backend directory

sys.path.insert(0, os.path.abspath('../../backend'))

# Django's configuration setup

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
try:
    import django
    from django.conf import settings as dj_settings
    # Usar SQLite en memoria durante el build de docs
    dj_settings.DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
    django.setup()
except Exception:
    pass

# Project information

project = 'Movies Project'
copyright = '2025, Natali Lopez'
author = 'Natali Lopez'
release = '0.0.1'
language = 'en'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',   # Google/NumPy style docstrings
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
]

autosummary_generate = True
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True,
}
napoleon_google_docstring = True
napoleon_numpy_docstring = True

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', {}),
    'django': ('https://docs.djangoproject.com/en/4.2/', {}),
}

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

todo_include_todos = True