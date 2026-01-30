---
title: "Spatial: Shoreline Analysis"
excerpt: "Mapping shoreline change at Atkinson Dam using Landsat imagery and NDWI, with a fully reproducible Python workflow linking spatial change to historic storage levels."
collection: portfolio
layout: single
permalink: /portfolio/shoreline-analysis/
header:
  teaser: /assets/images/portfolio/Shoreline_Analysis_Thumb_16_9_ratio.png
classes: wide-project
---

## Overview

This project examines **shoreline change over time** at **Atkinson Dam, Queensland**, and compares those spatial changes with **historic dam storage levels**. The entire workflow — from raw satellite imagery through to final visualisation — was developed **100% in Python**.

The analysis uses **Landsat satellite imagery** as its primary data source. Water bodies have a distinctive spectral signature: they reflect strongly in the **green band** and very weakly in the **near-infrared (NIR)** band. This contrast can be exploited using the **Normalised Difference Water Index (NDWI)** to objectively identify water pixels.

The NDWI is calculated as:

\[
\text{NDWI} = \frac{\text{Green} - \text{NIR}}{\text{Green} + \text{NIR}}
\]

Resulting values range from **–1 to +1**, where:

- **Positive values** represent water  
- **Negative values** represent non-water surfaces  

Because NDWI is based on a logical spectral relationship rather than visual interpretation, it provides a **consistent, reproducible, and objective** method for mapping water bodies. This makes it particularly useful for shoreline change detection, flood and drought analysis, riverbank erosion studies, and long-term environmental monitoring.

To span the full period of interest, imagery from **two Landsat missions** was required: **Landsat 5** and **Landsat 8**. These satellites differ in both **radiometric resolution** (8-bit vs 16-bit imagery) and **band designations**, requiring careful handling to ensure consistency through time.

---

## Landsat Band Designations

| Band | Landsat 8 | Landsat 5 |
|-----|-----------|-----------|
| Blue | Band 2 | Band 1 |
| Green | Band 3 | Band 2 |
| Red | Band 4 | Band 3 |
| NIR | Band 5 | Band 4 |

---

## Visualisation

- Animated shoreline change over time (GIF / MP4)
- Dam storage comparison chart (megalitres)

*(Visualisations inserted here)*

---

## Data

- **USGS Earth Explorer** — Landsat 5 & Landsat 8  
  https://earthexplorer.usgs.gov/

- **SEQ Water** — Historical Atkinson Dam storage records  
  https://www.seqwater.com.au/historic-dam-levels#source=120

---

## Workflow

1. Download Landsat imagery covering **Atkinson Dam**  
   *(Latitude –27.427261, Longitude 152.447959)*  
   - Years selected: **2006, 2008, 2015, 2017, 2022**  
   - Cloud cover filtered to **< 20%**
   - Full multi-band datasets downloaded for each scene

2. Automatically detect required spectral bands using **USGS filename patterns**

3. Create an **Area of Interest (AOI)** polygon and clip imagery to extent

4. Generate **NDWI rasters** for each year using:  
   \[
   \text{NDWI} = \frac{\text{Green} - \text{NIR}}{\text{Green} + \text{NIR}}
   \]

5. Apply a **conditional (Con) operation** to extract water pixels  
   - NDWI ≥ 0 classified as water  
   - Water pixels assigned a value of 1  
   - Non-water pixels set to NoData

6. Convert water rasters to polygons to extract **lake shorelines**

7. Generate water masks and calculate **dam surface area**

8. Timestamp shoreline geometries for temporal comparison

9. Load **historical dam storage observations** from CSV

10. Create:
    - Animated shoreline change visualisations (GIF & MP4)
    - Storage charts with shoreline observation dates overlaid

---

## Technical Appendix

The Python code was developed to be **reproducible, reusable, and adaptable** to other reservoirs or study areas with minimal modification.

Key features include:

- Automatic detection of correct spectral bands across Landsat missions
- Built-in **QA/QC checks**
- Consistent handling of mixed 8-bit and 16-bit imagery
- Fully scripted workflow from raw imagery to final outputs

Band detection and validation are based on the **USGS Earth Explorer Landsat naming convention**, incorporating:

- Mission
- Processing level
- Path / Row
- Acquisition date
- Processing date
- Collection and Tier
- Band identifiers (B1–B11)

---

## Code

- `Shoreline_Analysis.py`
