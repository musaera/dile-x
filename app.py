import streamlit as st
from utils.api import fetch_drone_data
from maps.map_view import render_map
from tables.history_table import show_history
from summary.statistik import show_statistik
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Drone Monitor", layout="wide")
st.title("🚁 Drone Data Visualization")

# Fetch data sekali untuk semua
data = fetch_drone_data()

# Buat Sidebar
with st.sidebar:
    selected=option_menu(
        menu_title="Menu",
        options=["Map", "Statistik", "History"],
        icons=["geo-alt", "bar-chart", "clock-history"],
        default_index=0
    )
    
if selected == "Map":
    render_map()

if selected == "Statistik":
    show_statistik(data)
    
if selected == "History":
    show_history(data)

    
