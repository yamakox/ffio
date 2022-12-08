# ffmpeg_frame_io

## Install from GitHub

```bash
pip3 install git+https://github.com/yamakox/ffmpeg_frame_io.git
```

## Install from source code

```bash
pip3 install -e .
```

## Build

```bash
python3 -m venv venv
. venv/bin/activate
pip3 install -r requirements.txt
python3 -m build
```

## Build doc

```bash
python3 -m venv venv
. venv/bin/activate
pip3 install -r requirements.txt
sphinx-apidoc -F -H ffmpeg_frame_io -H yamakox -V v0.1 -o docs src
```

Change conf.py:

```python
  extensions = [
      'sphinx.ext.autodoc',
      'sphinx.ext.viewcode',
      'sphinx.ext.todo',
+     'sphinx.ext.napoleon',
  ]

- html_theme = 'alabaster'
- html_static_path = ['_static']
+ import sphinx_rtd_theme
+ html_theme = "sphinx_rtd_theme"
+ html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
```

Change ffmpeg_frame_io.rst like this:

```rst
  .. automodule:: ffmpeg_frame_io.(any submodules)
     :members:
     :undoc-members:
     :show-inheritance:
+    :noindex:
```

```bash
sphinx-build docs docs/_build
```

## Examples

```bash
cd examples
python3 frame_writer_sample.py
python3 frame_reader_sample.py
```

