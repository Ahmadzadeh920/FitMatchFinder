
import os
import sys
import django
from pathlib import Path

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'FitFinder'
copyright = '2025, Fatemeh Ahmadzadeh'
author = 'Fatemeh Ahmadzadeh'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',          # For autodocumenting Python modules
    #'sphinxcontrib.django',        # For Django-specific documentation
    'sphinx.ext.viewcode',         # Optional: Add links to source code
    'sphinx.ext.napoleon',         # Optional: For Google-style docstrings
]


templates_path = ['_templates']
exclude_patterns = []

language = 'en'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

#html_theme = 'alabaster'
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']


#sys.path.insert(0, os.path.abspath('..'))  # Add the project root to the Python path
# Add the project root directory to the Python path
project_root = Path(__file__).resolve().parents[2]  # Adjust the number of `parents` based on your directory structure
sys.path.insert(0, str(project_root))
os.environ['DJANGO_SETTINGS_MODULE'] = 'Core.settings.development'  # Replace with your settings module
django.setup()