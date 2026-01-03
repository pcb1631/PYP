import os
import sys
sys.path.insert(0, os.path.abspath('../../'))


def path(*args):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), *args)

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'De Gym Management System'
copyright = '2026, Josiah'
author = 'Josiah, Ryan, Adrian, Jian Jun'
release = '0.1'
version ='1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc', 
    'sphinx_simplepdf',
    'sphinx.ext.duration',
    'sphinx.ext.doctest',

]

templates_path = ['_templates']
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']
html_css_files = ['custom.css']

simplepdf_vars = {
    'cover-overlay': 'rgba(150, 26, 26, 0.90)',
    'cover-bg': 'url(APUlogo.png) no-repeat center',
    'bottom-right-content': 'counter(page)',
    'bottom-center-content': '"Asia Pacific University: Programming with Python (102025-SHR)"'
}

html_context = {
    'docs_scope': 'external',
    'cover_logo_title': '',
    'cover_meta_data': 'Asia Pacific University: <br><br>Programming with Python (102025-SHR) <br>Lab 37 Mr Law Wei Liang <br> Group 8',
    'cover_footer': 'Submission date: 9th of January 2026<br>'
                    'Josiah Hoo TP085556<br>'
                    'Adrian Lee TP083977<br>'
                    'Ryan Teoh TP085450<br>'
                    'Chow Jian Jun TP085450<br>',
}