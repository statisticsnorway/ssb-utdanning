To release a new version on Pypi, bump the package version with (for example)
```bash
poetry version patch
```
And then do a PR into main with the bump set in pyproject.toml.


Run nox locally with a single mypy run (example)
```bash
poetry run nox --session mypy --python 3.10
```




Rebuild reference.md in the docs-folder locally
```bash
poetry run sphinx-apidoc -T -f -t ./docs/templates -o ./docs ./src
```

Regenerate the _build folder with docs-website locally
```bash
nox -s docs-build
```
