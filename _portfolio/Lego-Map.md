---
title: "Lego-Style Map"
excerpt: "A LEGO-style elevation map that reinterprets real-world terrain through creative cartographic design."
collection: portfolio
layout: single
permalink: /portfolio/lego-map/
header:
  teaser: /assets/images/portfolio/Lego_Map_Thumb_16_9_ratio.png
classes: wide-project
weight: 25
---

## Overview

Everybody loves LEGO®, and this project started with a simple question:
what would a real-world landscape look like if it were built from LEGO bricks?

Using ArcGIS Pro, I explored how elevation data could be stylised into a block-based, LEGO-like terrain model. Beyond being visually playful, this approach offers an accessible way to engage people—especially younger audiences—with spatial data, topography, and cartographic concepts.

To test the idea, I created a LEGO-style elevation model of Mount Warning (Wollumbin) in northern New South Wales. Rising approximately 1,159 metres above sea level, Mount Warning is the prominent central remnant of an ancient shield volcano. At its peak, the original volcano is estimated to have stood more than 1,900 metres high, making it an ideal subject for a compact yet expressive elevation model.

---

## Visualisation

![Mount Warning Lego Map](/assets/images/Mount_Warning_Lego_Map.png)

*LEGO-style elevation model of Mount Warning (Wollumbin), New South Wales, Australia*

---

## Method

**Data**

30-metre SRTM DEM from: [SRTM Tile Downloader](https://dwtkns.com/srtm30m/)
*Requires a NASA Earth Explorer login*

**Workflow**

1. Define the Area of Interest (AOI) — Mount Warning, NSW

2. Export the DEM for the AOI
*(Export Raster → 32-bit float → Clip to current display extent)*

3. Convert the DEM to an integer raster

4. Generate a square tessellation
*(Cell size adjusted to suit the scale of the landscape)*

5. Convert tessellation polygons to points
*(Feature to Point — “Inside” unchecked)*

6. Extract elevation values to points using the integer DEM

7. Perform a spatial join between tessellation squares and elevation points
*(Assigning representative elevation values to each square)*

8. Apply graduated colour symbology based on elevation values

9. Adjust the number of classes to balance visual clarity and terrain variation

10. Enhance the tessellation squares by:

- Adding a secondary fill layer

- Applying offset and move effects

- Using semi-transparent black shading to create a “stacked brick” illusion

11. Style the point features using matching graduated colour classes

12. Add subtle offsets and outlines to point symbols to reinforce depth

13. Refine symbology across all classes until the LEGO effect emerges

The result is a stylised elevation model that reads immediately as terrain, while clearly referencing the visual language of LEGO bricks.

---

## Outcome

This project demonstrates how traditional elevation data can be reinterpreted through creative cartographic styling. While playful in appearance, the workflow is grounded in standard GIS processes and could be adapted for education, visual storytelling, or exploratory map design.

It also highlights how small symbology choices—offsets, shadows, and class breaks—can dramatically change how spatial data is perceived and understood.
