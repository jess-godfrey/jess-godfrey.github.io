---
title: "DEM to REM"
excerpt: "Transforming a Digital Elevation Model (DEM) of the Snake River, Wyoming, into a Relative Elevation Model (REM) to highlight subtle fluvial features."
collection: portfolio
layout: single
permalink: /portfolio/DEM_to_REM/
header:
  teaser: /assets/images/portfolio/DEM_to_REM_Thumb_16_9_ratio.png
classes: wide-project
weight: 20
---

## Overview

I tried my hand at creating a Relative Elevation Model (REM) from a Digital Elevation Model (DEM) of the Snake River south of Grand Teton National Park, Wyoming.

Relative Elevation Models (REMs), also called Height Above River (HAR) rasters, are specialised digital terrain maps that remove a terrain's overall slope (like a river's downhill flow) to highlight subtle and localised features. This makes visualisation of past channel paths, floodplains, meanders, and terraces much clearer by setting the riverbed elevation to zero and showing everything else relative to it.

The purpose is to visualise geomorphic features for studies in fluvial geomorphology, flood risk assessment, environmental assessments (habitats), and engineering (roads, dams), revealing patterns hidden in standard Digital Elevation Models (DEMs).

They are also beautiful and works of art on their own.

---

## Visualisation

![Snake River Wyoming REM](/assets/images/Snake_River_Wyoming_DEM_to_REM.png)

*Relative Elevation Model of the Snake River, Wyoming. This was designed as a visualisation for presentations - intentionally minimal.*

---

## Method

**Data**

1m Lidar Data from: [USGS 1m Lidar Explorer](https://apps.nationalmap.gov/lidar-explorer/#/)

Downloading 1m lidar data often results in tens to hundreds of folders to unzip, which takes time away from spatial processing and analysis. Below is a small Python snippet to help bulk unzip zip files:

```python
import os
import zipfile

# Input folder containing the .zip files
zip_folder = r"C:\Users\YourFolder\Zipped"

# Output folder where files will be extracted
output_folder = r"C:\Users\YourFolder\Unzipped"

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Loop through each file in the zip folder
for filename in os.listdir(zip_folder):
    if filename.lower().endswith(".zip"):
        zip_path = os.path.join(zip_folder, filename)

        print(f"Extracting: {filename}")

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(output_folder)

print("All ZIP files have been extracted successfully!")
```

**Workflow**
1. Download the data from the area of interest - 1M DEM from - https://elevation.fsdf.org.au/.  (Then unzipped all using some python code)
2. Mosaic to New Raster 
3. Sample river raster values
4. Click on the symbology layer and change the statistics to custom and change to the min and max sampled values.
5. Create a copy of this new raster.
6. Create new feature class, polyline (with z values) and click along river centre point (if you don't already have the river lines).
7. Generate points along lines > using our new river centre line.
8. Extract Values to points (creating the Z values of the river) use the original TIFF raster as the input for this.
9. Geoprocessing - IDW. Our input is the new points with Z info. The z-value is the RASTERVALU leave everything else and run (make sure it is set to the raster extent in the environments section).  Change to a black and white stretch in symbology panel.
10. Then Project Raster > Bilinear interpolation > Output cell size should be our original DEM.  You can change this to a stretch symbology or leave in the rainbow colours, it is just going to be used for the raster calculation.
Raster Calculator.  Original DEM - reprojected IDW = REM.
