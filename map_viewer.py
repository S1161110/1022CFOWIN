import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd
import requests
import tempfile
import os

# 設定 Streamlit 版面
st.set_page_config(layout="wide")
st.title("Leafmap - 向量 (Vector) + 網格 (Raster)")

# --- 1. 載入 Raster (COG: Cloud Optimized GeoTIFF) ---
cog_url = "https://github.com/opengeos/leafmap/raw/master/examples/data/cog.tif"

# --- 2. 載入 Vector (GeoDataFrame) ---
url = "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"
gdf = None
try:
    # 先嘗試直接讀取 URL（gpd 支援從 zip URL 讀取）
    gdf = gpd.read_file(url)
except Exception as e:
    # 若直接讀取失敗，嘗試下載到暫存檔再讀取，並顯示錯誤訊息
    st.warning(f"直接從 URL 讀取向量資料失敗，嘗試從暫存檔讀取：{e}")
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            r = requests.get(url, stream=True, timeout=30)
            r.raise_for_status()
            zip_path = os.path.join(tmpdir, "ne_countries.zip")
            with open(zip_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
            # geopandas 可以讀取 zip 檔內的 shapefile
            gdf = gpd.read_file(zip_path)
    except Exception as e2:
        st.error(f"無法載入向量資料：{e2}")

if gdf is None or gdf.empty:
    st.error("向量資料未能載入，請確認網路連線或資料來源。")
else:
    # --- 3. 建立地圖物件 ---
    m = leafmap.Map(center=[0, 0], zoom=2)

    # --- 4. 加入圖層 ---
    # 加入 Raster (COG)
    try:
        m.add_raster(
            cog_url,
            palette="terrain",  # 使用地形色系
            layer_name="Global DEM (Raster)"
        )
    except Exception as e:
        st.warning(f"加入 Raster 圖層失敗：{e}")

    # 加入 Vector (GeoDataFrame)
    try:
        m.add_gdf(
            gdf,
            layer_name="Countries (Vector)",
            style={"fillOpacity": 0, "color": "black", "weight": 0.5}
        )
    except Exception as e:
        st.warning(f"加入向量圖層失敗：{e}")

    # --- 5. 顯示圖層控制與地圖 ---
    m.add_layer_control()
    m.to_streamlit(height=700)
