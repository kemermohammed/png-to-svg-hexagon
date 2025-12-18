# png-to-svg-hexagon

# Hexagonal Wallpaper Generator

## Overview
This project converts a raster image (PNG/JPG) into a scalable SVG wallpaper
using hexagonal or triangular sampling.

## Algorithm
1. Load the input image using Pillow
2. Iterate over an hexagonal grid
3. Sample the average color of pixels for each cell
4. Generate SVG polygons (hexagons or triangles)
5. Export the result as a scalable SVG file

## Usage
```bash
python generate.py input.png output.svg [hex_size] [mode]
