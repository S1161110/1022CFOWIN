import streamlit as st
import leafmap
import geopandas as gpd

st.set_page_config(layout="wide")
st.title("Leafmap + GeoPandas 範例")

# --- 下載並讀取 Natural Earth 向量資料 ---
st.info("正在載入 Natural Earth 國界資料 (110m)...")

try:
    # 官方建議使用 NACISCDN，而非 UNEP 網頁
    url = "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"
    gdf = gpd.read_file(url)
    st.success("✅ 資料載入成功！")
    st.dataframe(gdf.head())
except Exception as e:
    st.error(f"❌ 無法載入資料：{e}")
    st.stop()

# --- 側邊欄：底圖選擇 ---
st.sidebar.title("地圖設定")
basemap_options = ["OpenTopoMap", "Esri.WorldImagery", "CartoDB.DarkMatter"]
basemap = st.sidebar.selectbox("選擇底圖", basemap_options, index=0)

# --- 建立地圖物件 ---
m = leafmap.Map(center=[0, 0], zoom=2)

# 加入底圖
m.add_basemap(basemap)

# 加入國界資料
m.add_gdf(
    gdf,
    layer_name="Natural Earth Countries (110m)",
    style={"fillOpacity": 0, "color": "black", "weight": 0.5},
    highlight=False,
)

# 加入圖層控制與顯示
m.add_layer_control()
m.to_streamlit(height=700)
