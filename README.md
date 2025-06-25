# VectorIO
OVITO extension to read/write [vectors](https://www.ovito.org/docs/current/reference/pipelines/visual_elements/vectors.html) with all attached properties from/to a [compressed numpy file](https://numpy.org/doc/2.1/reference/generated/numpy.savez_compressed.html#numpy.savez_compressed) or a CSV file. 

The configuration of the [visual element](https://www.ovito.org/docs/current/reference/pipelines/visual_elements/vectors.html) is not exported.

## Example
The vectors created in ``examples/example.ovito`` can be exported using the [export file dialog](https://www.ovito.org/manual/usage/export.html) selecting the "Vector file writer" format.

The resulting ``.npz`` file matches ``examples/example.npz``. This file can be opened in OVITO Pro GUI. This reconstructs the vectors with all their properties. CSV files cannot be imported back into OVITO Pro.

Both import and export are also available from Python:

```Python
from ovito.io import import_file, export_file

# import npz file
pipeline = import_file("examples/example.npz")

from VectorIO import VectorFileWriter

# export npz file
export_file(data, "examples/example.npz", format=VectorFileWriter, key=data.vectors["example_vectors"])
```

## Installation
- From the OVITO Pro using the [extensions GUI](https://www.ovito.org/docs/current/advanced_topics/python_extensions.html#topics-python-extensions)
- OVITO Pro [integrated Python interpreter](https://docs.ovito.org/python/introduction/installation.html#ovito-pro-integrated-interpreter):
  ```
  ovitos -m pip install --user git+https://github.com/ovito-org/VectorIO
  ``` 
  The `--user` option is recommended and [installs the package in the user's site directory](https://pip.pypa.io/en/stable/user_guide/#user-installs).

- Other Python interpreters or Conda environments:
  ```
  pip install git+https://github.com/ovito-org/VectorIO
  ```

## Technical information / dependencies
- Tested on OVITO version 3.12.0

## Contact
Daniel Utt (utt@ovito.org)
