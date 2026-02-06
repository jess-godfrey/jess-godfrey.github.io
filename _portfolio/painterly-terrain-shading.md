---
title: "Painterly Terrain Shading"
excerpt: "An exploration of layer blending and relief shading techniques to create expressive, painterly terrain from satellite imagery."
collection: portfolio
layout: single
permalink: /portfolio/painterly-terrain-shading/
header:
  teaser: /assets/images/portfolio/The_Grand_Canyon_Thumb_16_9_ratio.png
classes: wide-project
weight: 26
---

## Overview

This project explores advanced cartographic shading and layer-blending techniques to transform satellite imagery into a more expressive, painterly visual style. By carefully combining elevation data, hillshading, and imagery — and duplicating layers with adjusted colour ramps — the terrain gains depth, contrast, and a heightened sense of form.

The result is imagery that feels less photographic and more illustrative, while still preserving geographic accuracy. Subtle blending choices allow landforms to “pop” and guide the eye across the landscape, enhancing both visual impact and terrain readability.

---

## Visualisation

![Grand Canyon](/assets/images/The_Grand_Canyon_smaller_v1.png)

*Postcard style visualisation of The Grand Canyon showcasing the painterly style*

![Blue Mountains National Park](/assets/images/Blue_Mountains_National_Park_smaller_v1.png)

*Postcard style visualisation of The Blue Mountains National Park showcasing the painterly style*

---

## Method

**Data**

30-metre SRTM DEM from: [SRTM Tile Downloader](https://dwtkns.com/srtm30m/)
*Requires a NASA Earth Explorer login*

**Workflow**

1. Define the area of interest (AOI) — In this case both the Grand Canyon and the Blue Mountains National Park

2. Export the digital elevation model (DEM) for the AOI
   *(export raster → 32-bit float → clip to current display extent)*.

3. Convert the DEM to Hillshade.

4. Using World Imagery as your basemap, stack your hillshade raster above this layer and select a blend mode of 'Luminosity'.

5. Above your hillshade layer, stack your DEM, in the 'Symbology' tab change your stretch symbology type to standard deviation to help smooth out the raster, select an fitting colour ramp and select a blend mode of 'Soft Light'.  This layer helps to give a sense of depth to the terrain.

6. Duplicate your DEM layer to really make the colours pop.  
   
