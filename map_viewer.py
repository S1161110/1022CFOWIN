import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd

# 設定 Streamlit 版面
st.set_page_config(layout="wide")
st.title("Leafmap - 向量 (Vector) + 網格 (Raster)")

# --- 1. 載入 Raster (COG: Cloud Optimized GeoTIFF) ---
cog_url = "https://github.com/opengeos/leafmap/raw/master/examples/data/cog.tif"

# --- 2. 載入 Vector (GeoDataFrame) ---
url = "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"
gdf = gpd.read_file(url)

# --- 3. 建立地圖物件 ---
m = leafmap.Map(center=[0, 0], zoom=2)

# --- 4. 加入圖層 ---
# 加入 Raster (COG)
m.add_raster(
    cog_url,
    palette="terrain",  # 使用地形色系
    layer_name="Global DEM (Raster)"
)

# 加入 Vector (GeoDataFrame)
m.add_gdf(
    gdf,
    layer_name="Countries (Vector)",
    style={"fillOpacity": 0, "color": "black", "weight": 0.5}
)

# --- 5. 顯示圖層控制與地圖 ---
m.add_layer_control()
m.to_streamlit(height=700)
