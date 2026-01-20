---
title: "Tanaka Contours"
excerpt: "Directional contour styling inspired by the Tanaka method, applied to subsurface seismic horizons using Python and ArcGIS Pro."
collection: portfolio
layout: single
permalink: /portfolio/tanaka-contours/
header:
  teaser: /assets/images/portfolio/Tanaka_Contours_Thumb_16_9_ratio.png
---

## Overview

Contour lines have become such a familiar part of our maps that their expressive power is often taken for granted. Modern GIS tools, for all their sophistication, can make contours feel purely functional — yet when handled with care, they remain one of the most visually striking ways to represent terrain.

This insight is hardly new. As early as the 19th century, cartographers experimented with shaded contour techniques to bring landscapes to life. The approach later became widely known as the *Tanaka method*, named after Japanese cartographer Kitiro Tanaka, whose work re-energised the technique. Even the cover of Imhof’s seminal cartographic text features a dramatic stack of shaded contour lines, a reminder of their enduring artistic and analytical potential.

In this project, I apply Tanaka-style illuminated contours to a subsurface seismic horizon from the Bowen Basin in Queensland, Australia. What is shown here is not topography, but a slice through deep time — a Triassic surface derived from seismic interpretation. By combining Python-based contour generation with cartographic refinement in ArcGIS Pro, the project explores how analytical workflows and visual design can work together to make abstract subsurface data more accessible and expressive.


---

## Visualisation

![Tanaka contour terrain map](/assets/images/B85_Seismic_Horizon_Tanaka_Contours.png)

**_This map was designed as a presentation and artistic piece — intentionally minimal, without labels, titles, or annotation — allowing form and illumination to carry the narrative._**


---

## Method

**Data**
- Subsurface seismic horizon (B85), Bowen Basin, Queensland  
- Interpreted Triassic surface represented as a raster

**Workflow**
1. Generate contour lines from the raster surface
2. Split contours at vertices to enable per-segment styling
3. Calculate additional attributes using Python:
   - Azimuth
   - Line width modifier
   - Colour modifier
4. Apply Tanaka-style illumination with lighting from the south-east
5. Refine symbology and layout within ArcGIS Pro


---

## Technical Notes

Contour segments were attributed using Python within ArcGIS Pro (arcpy and math libraries).  Lighting effects were derived from segment azimuth, with values stored as 32-bit float fields to control both line width and tonal variation. Separating contour generation, attribution, and cartographic styling allowed for experimentation while preserving a reproducible analytical workflow.

---

## Technical Appendix

### Contour preprocessing
Once contours were generated, they were split at vertices to allow segment-level attribution and styling.

---

### Azimuth calculation (SE illumination)

**Field**
- Name: `azimuth_se`
- Type: Float (32-bit)
- Expression type: Python 3

**Expression**
```python
azimuth_se = get_azimuth_se(!Shape!)
```

**Code block**
```python
from math import atan2, pi

def get_azimuth_se(shape):
    x1 = shape.firstPoint.X
    y1 = shape.firstPoint.Y
    x2 = shape.lastPoint.X
    y2 = shape.lastPoint.Y

    dx = x1 - x2
    dy = y1 - y2
    
    azimuth = atan2(dx, dy) * 180 / pi
    if azimuth < 0:
        azimuth += 360

    # Adjust for SE illumination (135°)
    azimuth_se = (azimuth - 135 + 360) % 360

    return azimuth_se
```

**Field**
- Name: `color_se`
- Type: Float (32-bit)
- Expression type: Python 3

**Expression**
```python
color_se = get_color_se(!azimuth_se!)
```

**Code block**
```python
def get_color_se(azimuth_se):
    azimuth_se -= 45
    if azimuth_se < 0:
        azimuth_se += 360
       
    return abs(azimuth_se - 180)
```

**Field**
- Name: `width_se`
- Type: Float (32-bit)
- Expression type: Python 3

**Expression**
```python
width_se = get_width_se(!azimuth_se!)
```

**Code block**
```python
def get_width_se(azimuth_se):
    azimuth_se -= 45
    if azimuth_se < 0:
        azimuth_se += 360

    return abs(abs(azimuth_se - 180) - 90)
```

### Symbology configuration
In ArcGIS Pro:
Open layer Symbology

Select Vary symbology by attribute

Set:

Color → color_se (black–white ramp)

Size → width_se

Enable Size range
Minimum: 1 pt
Maximum: 2 pt
