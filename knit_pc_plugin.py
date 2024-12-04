#!/usr/bin/python

"""
A utility for generating punch card patterns for knitting machines.
The generated files can be fed to a utility such as
https://brendaabell.com/knittingtools/pcgenerator/ to generate an SVG file
that can be printed out.


How to install:
Copy and paste this file into Gimp's plugin directory. If you need to locate
this directory, open Gimp, select Filters > Python-Fu > Console, and enter
the following, then hit Enter:  
gimp.plug_in_directory  
This will show the directory where you must place this file.


How to use:
In order to use this tool, your image must be in Indexed mode. To convert
your image to Indexed, select Image > Mode > Indexed. Currently, this tool
only supports two colors, so I recommend selecting "Use black and white (1-bit)
palette". This option will always result in black as the background color and
white as the foreground color.


Then, you simply draw your pattern onto the image. By default, foreground color
pixels represents holes punches, and background color pixels represent
non-punched cells.


In order to export your design as a punch card .txt file, ensure the layer
with your design pixels is selected. If your design is split across multiple
layers, you can combine them to a single layer by selecting Layer > New from
Visible.


With your design in the active layer, select Layer > Export Punchcard. This
will open a dialog box with the following options:

Output path: The path where your punchcard file will be saved. A *.txt file
is recommended.

Convert half-width: If this option is selected, a column of blank cells will
be inserted to the left of each output column, effectively doubling the width
of the resulting pattern. Select this option if you are designing a 12-stitch
repeat design where only ever 2nd column is read, such as for a bulky gauge
machine.

Foreground color: By default, foreground pixels map to punched holes. You may
invert this so that foreground pixels are non-punched, and background pixels
are punched. For example, in the recommended 1-bit palette, white pixels will
produce hole punches by default, but if you change the selection from Punch to
Blank, black pixels will produce hole punches instead.

Row interleaving: By default, each row will be output as-is.  
In Flat mode, each row will be split into two rows, one of which will be
inverted. Whether the inverted row comes before or after the normal row
alternates. For example, a 4-row design will produce the following pattern:  
 - Row 4
 - Row 4 inverse
 - Row 3 inverse
 - Row 3
 - Row 2
 - Row 2 inverse
 - Row 1 Inverse
 - Row 1
Select this option to generate a design for 2-color double-bed jacquard, tuck,
or slip worked flat.  
In Round mode, each row is split similarly to Flat mode; however, the inverted
row will always be directly above the normal row. For example:  
 - Row 4 inverse
 - Row 4
 - Row 3 inverse
 - Row 3
 - Row 2 inverse
 - Row 2
 - Row 1 Inverse
 - Row 1
Select this option to generate a 2-color slip design worked in the round on
the double-bed.

Press OK to generate the punchcard file.

Copyright 2024 Yaakov Schectman

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

__author__ = 'Yaakov Schectman'
__copyright__ = '2024'
__credits__ = []
__license__ = 'MIT'
__version__ = '0.0.1'
__maintainer__ = 'Yaakov Schectman'
__email__ = 'yaakov.schectman@gmail.com'
__status__ = 'Prototype'

from gimpfu import *

def write_row(file, row, half_width, blank='-', hole='X'):
    for cell in row:
        if half_width:
            file.write(blank)
        file.write(hole if cell else blank)
    file.write('\n')

def knitpc(timg, tdrawable, output_path, half_width, fg, inverse_rows):
    if not isinstance(tdrawable, gimp.Layer):
        pdb.gimp_message('Knitting Punchcard plugin should be used on a Layer.')
        return
    layer = tdrawable
    width, height = layer.width, layer.height
    pixels = layer.get_pixel_rgn(0, 0, width, height)
    grid = [[bool(ord(pixels[x, y])) != bool(fg) for x in range(width)] for y in range(height)]
    with open(output_path, 'w') as file:
        for i, row in enumerate(grid):
            if inverse_rows == 0:
                write_row(file, row, half_width)
            elif inverse_rows == 1:
                if (height - 1- i) % 2 == 0:
                    # Remember, the bottom row is printed second!!!
                    write_row(file, [not x for x in row], half_width)
                    write_row(file, row, half_width)
                else:
                    write_row(file, row, half_width)
                    write_row(file, [not x for x in row], half_width)
            elif inverse_rows == 2:
                write_row(file, [not x for x in row], half_width)
                write_row(file, row, half_width)

register(
    'knit_pc_plugin',
    'Convert image to a punch card pattern',
    'Convert image to a punch card pattern',
    'Yaakov Schectman',
    'Yaakov Schectman',
    '2024',
    '<Image>/Layer/Export Punchcard',
    'INDEXED*',
    [
        (PF_FILENAME, 'output_path', 'Output Path', '.'),
        (PF_TOGGLE, 'half_width', 'Convert half-width', False),
        (PF_RADIO, 'fg', 'Foreground color:', 0, (('Punch', 0), ('Blank', 1))),
        (PF_RADIO, 'inverse_rows', 'Row interleaving', 0, (('None', 0), ('Flat', 1), ('Round', 2))),
    ],
    [],
    knitpc
)

main()
