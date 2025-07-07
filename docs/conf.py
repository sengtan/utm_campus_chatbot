# Configuration file for the Sphinx documentation builder.
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------
project = 'UTM Campus Assistant Chatbot'
copyright = '2025, UTM Campus Assistant Team'
author = 'UTM Campus Assistant Team'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'myst_parser',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_logo = None
html_favicon = None

# -- Options for LaTeX output ------------------------------------------------
latex_elements = {
    'papersize': 'a4paper',
    'pointsize': '10pt',
    'preamble': r'''
\usepackage{charter}
\usepackage[defaultsans]{lato}
\usepackage{inconsolata}
''',
}

latex_documents = [
    ('index', 'utm_campus_assistant.tex', 'UTM Campus Assistant Administrator Manual',
     'UTM Campus Assistant Team', 'manual'),
]

# -- Extension configuration -------------------------------------------------
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False