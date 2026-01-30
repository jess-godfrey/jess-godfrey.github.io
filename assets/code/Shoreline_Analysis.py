# ------------------------------------------------------------------
# Atkinson's Dam Shoreline Analysis, Animation and Chart Comparison
# ------------------------------------------------------------------

# ------------------------- Imports---------------------------------

import os
import re
import numpy as np
import rasterio
from rasterio.mask import mask
import geopandas as gpd

# -------------------------- Paths----------------------------------

data_dir = r"C:\Users\JessGodfrey\welldata\Atkinsons_Dam_Analysis" #Update for your filepath
aoi_path = os.path.join(data_dir, "Atkinsons_Dam_AOI.shp") #update for your AOI Shapefile

out_clipped = os.path.join(data_dir, "output", "clipped")
out_ndwi = os.path.join(data_dir, "output", "ndwi")

os.makedirs(out_clipped, exist_ok=True)
os.makedirs(out_ndwi, exist_ok=True)

# -------------------------- QA/QC----------------------------------


all_files = os.listdir(data_dir)

print("\n================ FILE INVENTORY ================")
print(f"Total files in data directory: {len(all_files)}")

tif_files = [f for f in all_files if f.lower().endswith(".tif")]
print(f"Raster (.tif) files found: {len(tif_files)}")

if len(tif_files) == 0:
    raise RuntimeError("No .tif files found — check data directory path")

print("Sample files:")
for f in tif_files[:5]:
    print("  ", f)
print("================================================")

# --------------------- Load AOI & QA/QC-----------------------------

print("\n================ AOI LOAD ================")

aoi = gpd.read_file(aoi_path)
print("AOI loaded successfully")

if aoi.empty:
    raise ValueError("AOI shapefile is empty")

print("AOI head:")
print(aoi.head())

print("AOI CRS (before):", aoi.crs)

# Force AOI to Web Mercator
#aoi = aoi.to_crs("EPSG:3857")
#geometry = aoi.geometry.values

print("AOI CRS (after):", aoi.crs)
print("AOI bounds:", aoi.total_bounds)
print("==========================================")

# ------------------ Sample Raster & QA/QC--------------------------

print("\n=========== SAMPLE RASTER CHECK ===========")

sample_raster = tif_files[0]
sample_path = os.path.join(data_dir, sample_raster)

with rasterio.open(sample_path) as src:
    print("Sample raster:", sample_raster)
    print("Raster CRS:", src.crs)
    print("Raster bounds:", src.bounds)

print("==========================================")

# ------------------- Landsat Band Lookup ---------------------------

###Landsat band lookup###

band_lookup = {
    "05": {"green": "B2", "nir": "B4"},
    "08": {"green": "B3", "nir": "B5"},
    "09": {"green": "B3", "nir": "B5"},
}

# --------------------- Filename Parser -----------------------------

import re

def parse_landsat_filename(fname):
    """
    Parse Landsat Collection filenames like:
    LT05_L1TP_090079_19980314_20170105_01_T1_B2.TIF
    LC08_L1TP_090079_20150408_20200909_02_T1_B3.TIF
    LC09_L1TP_090079_20220718_20220902_02_T1_B5.TIF
    """

    fname = fname.upper()

    pattern = (
        r"^(?P<mission>LT05|LC08|LC09)_"     # Mission
        r"L1TP_"                             # Processing level
        r"\d{6}_"                            # Path/Row
        r"(?P<acq_date>\d{8})_"              # Acquisition date
        r"\d{8}_"                            # Processing date
        r"\d{2}_T1_"                         # Collection + tier
        r"(?P<band>(?:B[1-9]|B1[0-1]))\.TIF$" # Bands B1–B11 only
    )

    match = re.match(pattern, fname)
    if not match:
        return None

    mission = match.group("mission")
    satellite = mission[-2:]             # 05, 08, 09
    acq_date = match.group("acq_date")   # YYYYMMDD
    band = match.group("band")

    return satellite, acq_date, band


#QAQC
# Example Landsat file for testing
fname = "LC08_L1TP_090079_20150408_20200909_02_T1_B3.TIF"  #put your example file here for testing

# QAQC test
parsed = parse_landsat_filename(fname)

if parsed is None:
    print("  → Filename did not match Landsat spectral band pattern")
else:
    satellite, acq_date, band = parsed
    print(f"  Parsed → Landsat {satellite}, Acquisition date {acq_date}, Band {band}")

# -------------- Clip Raster to AOI & Process ----------------------

def clip_raster(src_path, out_path):
    print("\n--- CLIPPING RASTER ---")
    print("Input :", os.path.basename(src_path))
    print("Output:", out_path)

    try:
        with rasterio.open(src_path) as src:
            print("Opened raster OK")
            print("Raster CRS:", src.crs)
            print("Raster bounds:", src.bounds)

            # Reproject AOI to raster CRS
            aoi_proj = aoi.to_crs(src.crs)
            geom = aoi_proj.geometry.values

            print("AOI reprojected to raster CRS")
            print("AOI bounds:", aoi_proj.total_bounds)

            out_img, out_transform = mask(
                src,
                geom,
                crop=True
            )

            out_meta = src.meta.copy()

        out_meta.update({
            "height": out_img.shape[1],
            "width": out_img.shape[2],
            "transform": out_transform
        })

        with rasterio.open(out_path, "w", **out_meta) as dest:
            dest.write(out_img)

        print("✔ Clip successful")

    except Exception as e:
        print("✖ CLIP FAILED")
        print(e)

###Process Landsat bands with QAQC checks###

band_store = {}  # {year: {green: path, nir: path}}

print("\n============= PROCESSING RASTERS =============")

for fname in tif_files:
    print(f"\nScanning file: {fname}")

    parsed = parse_landsat_filename(fname)
    if not parsed:
        print("  → Filename did not match Landsat pattern, skipped")
        continue

    satellite, year, band = parsed
    print(f"  Parsed → Landsat {satellite}, Year {year}, Band {band}")

    if satellite not in band_lookup:
        print("  → Satellite not in lookup table, skipped")
        continue

    for band_type, band_code in band_lookup[satellite].items():
        if band == band_code:
            print("\n==============================")
            print("Raster selected for processing")
            print(f"Satellite : Landsat {satellite}")
            print(f"Year      : {year}")
            print(f"Band type : {band_type}")
            print(f"Band code : {band_code}")
            print("==============================")

            in_path = os.path.join(data_dir, fname)
            out_name = f"Landsat_{satellite}_{year}_Band_{band_code}.tif"
            out_path = os.path.join(out_clipped, out_name)

            clip_raster(in_path, out_path)

            band_store.setdefault(year, {})[band_type] = out_path

print("\n============= BAND STORE SUMMARY =============")
print(band_store)
print("=============================================")

# -------------- Calculate NDWI & Process ----------------------

### NDWI calculation with checks ###

def calculate_ndwi(green_path, nir_path, out_path):
    print("\n--- CALCULATING NDWI ---")
    print("Green:", green_path)
    print("NIR  :", nir_path)

    with rasterio.open(green_path) as g:
        green = g.read(1).astype("float32")
        meta = g.meta.copy()

    with rasterio.open(nir_path) as n:
        nir = n.read(1).astype("float32")

    ndwi = (green - nir) / (green + nir)
    ndwi[np.isinf(ndwi)] = np.nan

    meta.update(dtype="float32", count=1)

    with rasterio.open(out_path, "w", **meta) as dst:
        dst.write(ndwi, 1)

    print("✔ NDWI written:", out_path)

### Generate NDWI outputs ###

print("\n================ NDWI OUTPUTS ================")

for year, bands in band_store.items():
    if "green" not in bands or "nir" not in bands:
        print(f"Skipping {year} — missing bands")
        continue

    out_ndwi_path = os.path.join(out_ndwi, f"{year}_NDWI.tif")
    calculate_ndwi(bands["green"], bands["nir"], out_ndwi_path)

print("=============== PROCESS COMPLETE =============")

# -------------- QAQC NDWI Outputs ----------------------

import matplotlib.pyplot as plt
import rasterio
import numpy as np

def plot_ndwi(ndwi_path, title=None):
    with rasterio.open(ndwi_path) as src:
        ndwi = src.read(1)

    plt.figure(figsize=(6, 6))
    im = plt.imshow(ndwi, cmap="RdYlBu", vmin=-1, vmax=1)
    plt.colorbar(im, label="NDWI")
    plt.title(title or os.path.basename(ndwi_path))
    plt.axis("off")
    plt.show()

for fname in sorted(os.listdir(out_ndwi)):
    if fname.endswith("_NDWI.tif"):
        plot_ndwi(
            os.path.join(out_ndwi, fname),
            title=f"NDWI {fname[:8]}"
        )

# -------------- NDWI to water mask ----------------------

# NDWI ≥ 0 → water (1)
# NDWI < 0 → NoData

def ndwi_to_water_mask(ndwi_path, out_path):
    with rasterio.open(ndwi_path) as src:
        ndwi = src.read(1).astype("float32")
        meta = src.meta.copy()
        nodata = src.nodata

    water = np.where(ndwi >= 0, 1, np.nan)

    meta.update(
        dtype="float32",
        count=1,
        nodata=np.nan
    )

    with rasterio.open(out_path, "w", **meta) as dst:
        dst.write(water, 1)

    print(f"✔ Water mask written: {out_path}")

#Batch Process

out_water = os.path.join(data_dir, "output", "water_mask")
os.makedirs(out_water, exist_ok=True)

for fname in os.listdir(out_ndwi):
    if fname.endswith("_NDWI.tif"):
        date = fname[:8]
        ndwi_path = os.path.join(out_ndwi, fname)
        out_mask = os.path.join(out_water, f"{date}_water.tif")
        ndwi_to_water_mask(ndwi_path, out_mask)


# -------------- Raster to Polygon ----------------------

### Extract Shoreline polygons

from rasterio.features import shapes
from shapely.geometry import shape
import geopandas as gpd

def raster_to_polygon(raster_path, out_shp):
    with rasterio.open(raster_path) as src:
        image = src.read(1)
        transform = src.transform
        crs = src.crs

    mask = ~np.isnan(image)

    geoms = [
        shape(geom)
        for geom, value in shapes(image, mask=mask, transform=transform)
        if value == 1
    ]

    gdf = gpd.GeoDataFrame(
        {"class": ["water"] * len(geoms)},
        geometry=geoms,
        crs=crs
    )

    # Dissolve to single lake polygon
    gdf = gdf.dissolve()

    gdf.to_file(out_shp)
    print(f"✔ Shoreline polygon written: {out_shp}")

###Batch process###

out_poly = os.path.join(data_dir, "output", "shorelines")
os.makedirs(out_poly, exist_ok=True)

for fname in os.listdir(out_water):
    if fname.endswith("_water.tif"):
        date = fname[:8]
        raster_to_polygon(
            os.path.join(out_water, fname),
            os.path.join(out_poly, f"{date}_shoreline.shp")
        )

# -------------- Lake Area Calculation ----------------------

#data is in UTM (EPSG:32656), area is a trustworthy parameter.

import pandas as pd

records = []

for fname in os.listdir(out_poly):
    if fname.endswith(".shp"):
        date = fname[:8]
        gdf = gpd.read_file(os.path.join(out_poly, fname))

        area_m2 = gdf.geometry.area.sum()
        area_km2 = area_m2 / 1e6

        records.append({
            "date": date,
            "area_m2": area_m2,
            "area_km2": area_km2
        })

df_area = pd.DataFrame(records).sort_values("date")
df_area

# -------------- Lake Area QAQC Plot ----------------------

plt.figure(figsize=(8,4))
plt.plot(df_area["date"], df_area["area_km2"], marker="o")
plt.xticks(rotation=45)
plt.ylabel("Water Area (km²)")
plt.title("Atkinsons Dam – Surface Water Area Over Time")
plt.grid(True)
plt.tight_layout()
plt.show()

# ----------- Load Shorelines and Timestamp ----------------

import geopandas as gpd
import os
import pandas as pd

shoreline_dir = os.path.join(data_dir, "output", "shorelines")

shorelines = []

for fname in os.listdir(shoreline_dir):
    if fname.endswith(".shp"):
        date = pd.to_datetime(fname[:8], format="%Y%m%d")
        gdf = gpd.read_file(os.path.join(shoreline_dir, fname))
        gdf["date"] = date
        shorelines.append(gdf)

shorelines_gdf = pd.concat(shorelines, ignore_index=True)
shorelines_gdf = shorelines_gdf.sort_values("date")

# ----------- Load Historic Dam Observations CSV ----------------

#Data - https://www.seqwater.com.au/historic-dam-levels#source=120

csv_path = r"C:\Users\JessGodfrey\welldata\Atkinsons_Dam_Analysis\Atkinson.csv" #Your filepath here

dam_df = pd.read_csv(csv_path, parse_dates=["Date"])

dam_df = dam_df.rename(columns={
    "Last Observation (%)": "pct_full",
    "Last Observation (ML)": "volume_ml"
})

dam_df = dam_df.sort_values("Date")

#Quick QAQC

dam_df[["Date", "pct_full", "volume_ml"]].head()

print(len(shorelines_gdf))
print(shorelines_gdf["date"].min(), shorelines_gdf["date"].max())

# ------------------------------------------------------------------
# Atkinson's Dam Shoreline Animation
# ------------------------------------------------------------------

import os
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML

# Paths

data_dir = r"C:\Users\JessGodfrey\welldata\Atkinsons_Dam_Analysis"
aoi_path = os.path.join(data_dir, "Atkinsons_Dam_AOI.shp")

# Load AOI

aoi_gdf = gpd.read_file(aoi_path)

# Ensure CRS matches shoreline data
if aoi_gdf.crs != shorelines_gdf.crs:
    aoi_gdf = aoi_gdf.to_crs(shorelines_gdf.crs)

# Get fixed extent from AOI (with padding)

xmin, ymin, xmax, ymax = aoi_gdf.total_bounds

pad_x = (xmax - xmin) * 0.05
pad_y = (ymax - ymin) * 0.05

xmin -= pad_x
xmax += pad_x
ymin -= pad_y
ymax += pad_y

# Build animation

fig, ax = plt.subplots(figsize=(7, 7))

def update(frame):
    ax.clear()

    # AOI outline (context)
    aoi_gdf.boundary.plot(
        ax=ax,
        color="black",
        linewidth=1
    )

    # Shoreline for this timestep
    gdf = shorelines_gdf.iloc[[frame]]
    gdf.plot(
        ax=ax,
        color="dodgerblue",
        edgecolor="navy",
        alpha=0.7
    )

    # Title
    date_str = gdf["date"].iloc[0].strftime("%d %b %Y")
    ax.set_title(
        f"Atkinsons Dam – Shoreline Change\n{date_str}",
        fontsize=12,
        weight="bold"
    )

    # Lock map extent
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_aspect("equal")
    ax.set_axis_off()

# IMPORTANT: keep reference alive
ani = FuncAnimation(
    fig,
    update,
    frames=len(shorelines_gdf),
    interval=700
)

# Render animation explicitly in notebook

HTML(ani.to_jshtml())

###---GIF and MP4---###

import os
from matplotlib.animation import PillowWriter, FFMpegWriter

# Save animation

output_dir = os.path.join(data_dir, "output", "animations")
os.makedirs(output_dir, exist_ok=True)

# --- GIF ---
out_gif = os.path.join(
    output_dir,
    "Atkinsons_Dam_Shoreline_Storage_single.gif"
)
ani.save(out_gif, writer=PillowWriter(fps=1))
print("✔ GIF saved at:", out_gif)

# --- MP4 ---
out_mp4 = os.path.join(
    output_dir,
    "Atkinsons_Dam_Shoreline_Storage_single.mp4"
)
writer = FFMpegWriter(fps=1.2, bitrate=1800)
ani.save(out_mp4, writer=writer)
print("✔ MP4 saved at:", out_mp4)

# --------------------------------------------------------------------
# Atkinson's Dam Storage History Chart connected to Shoreline Analysis
# --------------------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# Load CSV

csv_path = r"C:\Users\JessGodfrey\welldata\Atkinsons_Dam_Analysis\Atkinson.csv"
df = pd.read_csv(csv_path)

# Parse date (DD/MM/YYYY)
df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)
df = df.sort_values("Date")


# Shoreline analysis dates

shoreline_dates = pd.to_datetime(
    ["2015-08-04", "2017-05-15", "2022-10-28"] #Update with your dates
)


# Colours (RGB → matplotlib 0–1 scale)

bar_colour = (122/255, 178/255, 178/255)   # bars
highlight_colour = (9/255, 99/255, 126/255)


# Plot

fig, ax = plt.subplots(figsize=(13, 5))

# --- Bars: Volume (ML) ---
ax.bar(
    df["Date"],
    df["Last Observation (ML)"],
    width=10,                  # skinny bars
    color=bar_colour,
    alpha=0.85
)

ax.set_ylabel("Storage (ML)")
ax.set_xlabel("Year")


# Highlight shoreline dates

for d in shoreline_dates:
    # Vertical dashed line
    ax.axvline(
        d,
        linestyle="--",
        linewidth=0.5,
        color="black"
    )

    # Highlight point
    match = df.loc[df["Date"] == d]
    if not match.empty:
        ax.scatter(
            match["Date"],
            match["Last Observation (ML)"],
            s=70,
            facecolor=highlight_colour,
            edgecolor="black",
            linewidth=0.5,
            zorder=5
        )


# Format x-axis (whole years only)

ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))


# Title & grid

ax.set_title(
    "Atkinsons Dam – Storage History\nHighlighted dates correspond to shoreline analysis",
    fontsize=13,
    weight="bold"
)

ax.grid(axis="y", alpha=0.3)


# Save figure

output_path = r"C:\Users\JessGodfrey\welldata\Atkinsons_Dam_Analysis\output\figures"
os.makedirs(output_path, exist_ok=True)

out_png = os.path.join(
    output_path,
    "Atkinsons_Dam_Storage_with_Shoreline_Dates.png"
)

plt.savefig(
    out_png,
    dpi=300,                # high resolution
    bbox_inches="tight",
    facecolor="white"
)

print("✔ Figure saved at:", out_png)

plt.tight_layout()
plt.show()

# ------------------------------------------------------------------
# End of Analysis
# ------------------------------------------------------------------

