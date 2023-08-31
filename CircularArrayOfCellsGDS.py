# Create a Circular Array of cells GDS

# This was written using the following prompt with ChatGPT:

# Use phidl to make an array of unit cells where the cell 
# definition is given by a function that I supply. The array 
# is contained within a circle of radius R. The period of cells 
# in the array is A in the horizontal x direction and B in the 
# vertical y direction.

# Additional comments from ChatGPT:

# First, make sure you have PHIDL installed (pip install phidl).

# Here's an example of how to create the array of unit cells as 
# you described, where the unit cell definition is provided by a 
# function. In this example, let's say you have a function 
# create_unit_cell that defines your unit cell geometry:

# In this example, replace the create_unit_cell function and 
# its contents with your actual unit cell geometry creation logic. 
# The create_array_with_function function calculates the number of 
# cells needed within the circular boundary and places instances 
# of the unit cell at appropriate positions.

# Note that you should adjust the dimensions and the layer numbers 
# in the create_unit_cell function as per your requirements and 
# design rules. Also, you can replace the quickplot function with 
# other export methods if you want to save the layout to a GDS file 
# or visualize it using different tools.

# Alan R. Bleier, Cornell NanoScale Facility, Cornell University
# August 31, 2023

import phidl.geometry as pg
import phidl.routing as pr
from phidl import Device, quickplot

def create_unit_cell(width, height):
    unit_cell = Device()
    # Create your unit cell geometry using PHIDL functions
    # For example:
    rectangle = pg.rectangle(size=(width, height), layer=1)
    unit_cell.add_ref(rectangle)
    return unit_cell

def create_array_with_function(unit_cell_function, A, B, R):
    main_device = Device()

    # Calculate the number of cells in each direction
    num_cells_x = int(2 * R / A) + 1
    num_cells_y = int(2 * R / B) + 1

    for i in range(num_cells_x):
        for j in range(num_cells_y):
            x = -R + i * A
            y = -R + j * B
            if (x ** 2 + y ** 2) <= R ** 2:
                unit_cell = unit_cell_function()
                main_device.add_ref(unit_cell).move((x, y))

    return main_device

# Parameters
A = 10  # Period in x direction
B = 20  # Period in y direction
R = 100  # Radius of the circular boundary

# Create the array of unit cells using the provided function
array_device = create_array_with_function(
    unit_cell_function=lambda: create_unit_cell(width=5, height=10),  # Adjust dimensions as needed
    A=A,
    B=B,
    R=R,
)

# Quickplot to visualize the layout
quickplot(array_device)

# Write the GDS file
array_device.write_gds('device_array.gds')
