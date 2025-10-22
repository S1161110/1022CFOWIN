import streamlit as st

# 1. 使用 st.Page() 定義頁面
# st.Page() 會自動尋找相符.py檔案
pages = [
    st.Page("home.py", title="專案首頁", icon="👻"),
    st.Page("map_viewer.py", title="互動地圖瀏覽", icon="🫤"),
#    st.Page("page_about.py", title="關於我們", icon="🫵")
]
# 2. 使用 st.navigation() 建立導覽
with st.sidebar:
    st.title("App導覽")
    # st.navigation() 會回傳被選擇的頁面
    selected_page = st.navigation(pages)
# 3. 執行
selected_page.run()