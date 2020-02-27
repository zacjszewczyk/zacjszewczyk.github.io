#!/usr/local/bin/python3

# Imports
from math import sin, fabs # Curve
from random import seed, random, randrange # Randomizing curves
from datetime import datetime # Seeding random number generator

# Class: SVG
# Purpose: Build SVG landscape
class SVG:
    # Method: __init__
    # Purpose: Store output file, outfile, for later reference
    # Parameters:
    # - outfile: Path to output file. (String)
    def __init__(self,outfile):
        self.outfile = outfile
    
    # Method: build
    # Purpose: Build SVG landscape
    # Parameters: none
    # Return: True (Success)
    def build(self):
        # Generator parameters
        offsetY = 160
        layerHeight = 190
        layerWidth = 4000
        baseColor= 131
        layers = 6

        # Store each curve
        paths = []

        # Build the specified number of curves
        for layer in range(1,layers):
          # Seed the random number generator
          seed(datetime.now())

          # Calculate layer anchor and set initial point
          layerAnchorY = layer * (layerHeight / layers) + offsetY
          coord = f"M 0 {layerAnchorY} "

          # Set curve generator variables
          width = 0.0055 - (layer*0.0008) # Curve width. Decrease to widen
          amplitude = 10*randrange(3,6) # Curve amplitude. Increase to make taller.
          initial_y_offset = - 100 # Initial curve y offset. Make more negative to move curve up.
          x_offset = layer * random() # Randomize x offset for each curve
          y_offset = initial_y_offset + layer * randrange(40,60) # Randomize y offset for each curve
          
          # Generate the curves
          for i in range(layerWidth):
              trees = 1.5*layer*fabs(sin(i)) # Trees
              coord += f"H {i} V{ (amplitude*sin(width*i - x_offset) + trees) + y_offset}" # Coordinates
          coord += f"V {layerAnchorY} L 0 {layerAnchorY}" # Anchor
          paths.append(f"""<path d="{coord}" fill="#{baseColor}"/>""") # Store the path

          # Make each curve slightly lighter
          baseColor += 111

        # Create the output file
        open(self.outfile, "w").close()
        fd = open(self.outfile, "a")
        # Write opening SVG code
        fd.write(f"""<svg width="100%" viewBox="0 -100 4000 300" height="300" xmlns="http://www.w3.org/2000/svg" style="position: absolute; top: 0px; left: 0px; overflow: hidden; z-index: -1">""")

        # Append each curve
        for each in paths:
          fd.write(each)
        
        # Cloe and return
        fd.write("</svg>")
        fd.close()
        return True