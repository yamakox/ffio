# ffio

## Build

```bash
python3 -m venv venv
. venv/bin/activate
pip3 install -r requirements.txt
python3 -m build
```

## Build docs

```bash
python3 -m venv venv
. venv/bin/activate
pip3 install -r requirements.txt
sphinx-apidoc -F -H ffio -V v0.2 -o docs src
```

Change docs/conf.py:

```diff
  extensions = [
      'sphinx.ext.autodoc',
      'sphinx.ext.viewcode',
      'sphinx.ext.todo',
+     'sphinx.ext.napoleon',
  ]

- html_theme = 'alabaster'
- html_static_path = ['_static']
+ import sphinx_rtd_theme
+ html_theme = 'sphinx_rtd_theme'
+ html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
```

Change docs/ffio.rst like this if you want to avoid Sphinx's warning:

```diff
  .. automodule:: ffio.(any submodules)
     :members:
     :undoc-members:
     :show-inheritance:
+    :noindex:
```

```bash
sphinx-build docs docs/_build
```
