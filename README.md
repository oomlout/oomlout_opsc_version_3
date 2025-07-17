# Oomlout OPSC Version 3

This repository contains small examples and utilities for generating OpenSCAD models from Python.
The `opsc.py` module provides helper functions built on top of the **SolidPython** library.
It converts simple dictionaries describing objects into complete OpenSCAD models and can
optionally call the `openscad` command line tools to produce other file formats.

## Dependencies

- Python 3
- [SolidPython](https://github.com/SolidCode/SolidPython) (provides the `solid` module)
- [OpenSCAD](https://openscad.org/) command line tools must be available in your `PATH` to
  create STL, DXF, PNG or SVG outputs.

## Example usage

The `opsc_working.py` script demonstrates a basic workflow. The snippet below shows the
same logic in condensed form:

```python
import opsc

objects = [
    {
        'shape': 'pulley_gt2',
        'type': 'positive',
        'number_of_teeth': 20,
        'depth': 2
    }
]

# Generates outputs/my_object.scad and, because save_type="all", also PNG, STL,
# SVG and DXF files using OpenSCAD
opsc.opsc_make_object('outputs/my_object.scad', objects, save_type="all")
```

Running this command will create the specified `.scad` file and, when `save_type` is set
 to `"all"`, the helper will invoke OpenSCAD to render PNG, STL, SVG and DXF versions.

## Output files

All generated files are placed in the path supplied to `opsc_make_object`. When using the
example above the `outputs/` folder will contain files such as:

- `my_object.scad`
- `my_object.png`
- `my_object.stl`
- `my_object.svg`
- `my_object.dxf`
- `my_object_flat.*` (when laser mode is active)

These artefacts can then be used for 3D printing or laser cutting.
