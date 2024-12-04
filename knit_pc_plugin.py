#!/usr/bin/python

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
