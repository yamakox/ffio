# ffio

## Build

```bash
poetry build
```

## Build docs

```bash
poetry install --with dev
eval $(poetry env activate)
FFIO_VERSION=$(python3 -c "from importlib.metadata import version; import ffio; print(version('ffio'))")
sphinx-apidoc -F -H ffio -V v$FFIO_VERSION -o docs src
```

Change docs/conf.py:

```diff
  extensions = [
      'sphinx.ext.autodoc',
      'sphinx.ext.viewcode',
      'sphinx.ext.todo',
+     'sphinx_rtd_theme',
+     'sphinx.ext.napoleon',
  ]

- html_theme = 'alabaster'
- html_static_path = ['_static']
+ html_theme = 'sphinx_rtd_theme'
```

Change docs/ffio.rst like this if you want to avoid Sphinx's warning:

```diff
- Submodules
- ----------

  .. automodule:: ffio.frame_reader
+    :noindex:

  .. automodule:: ffio.frame_writer
+    :noindex:

- Module contents
- ---------------
- 
- .. automodule:: ffio
-    :members:
-    :show-inheritance:
-    :undoc-members:
```

```bash
sphinx-build docs docs/_build
```
