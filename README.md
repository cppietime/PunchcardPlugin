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
