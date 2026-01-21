---
title: "DEM to REM"
excerpt: "Transforming a Digital Elevation Model (DEM) of the Snake River, Wyoming, into a Relative Elevation Model (REM) to highlight subtle fluvial features."
collection: portfolio
layout: single
permalink: /portfolio/DEM_to_REM/
header:
  teaser: /assets/images/portfolio/DEM_to_REM_Thumb_16_9_ratio.png
classes: wide-project
---

## Overview

I tried my hand at creating a Relative Elevation Model (REM) from a Digital Elevation Model (DEM) of the Snake River south of Grand Teton National Park, Wyoming.

Relative Elevation Models (REMs), also called Height Above River (HAR) rasters, are specialised digital terrain maps that remove a terrain's overall slope (like a river's downhill flow) to highlight subtle and localised features. This makes visualisation of past channel paths, floodplains, meanders, and terraces much clearer by setting the riverbed elevation to zero and showing everything else relative to it.

The purpose is to visualise geomorphic features for studies in fluvial geomorphology, flood risk assessment, environmental assessments (habitats), and engineering (roads, dams), revealing patterns hidden in standard Digital Elevation Models (DEMs).

They are also beautiful and works of art on their own.

---

![Snake River Wyoming REM](/assets/images/Snake_River_Wyoming_DEM_to_REM.png)

*Relative Elevation Model of the Snake River, Wyoming.*

---

### Data source

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
