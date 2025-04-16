import folium
from streamlit_folium import st_folium
from utils.api import fetch_drone_data
import openrouteservice  # ← NEW
from openrouteservice import convert

# Masukkan API Key kamu di sini
ORS_API_KEY = "5b3ce3597851110001cf624842dc0de4e0234d01af6f869af936cd8a"

def get_route(client, start_coords, end_coords):
    try:
        route = client.directions(
            coordinates=[start_coords, end_coords],
            profile='foot-walking',  # 'driving-car' atau 'cycling-regular' juga bisa
            format='geojson'
        )
        return route['features'][0]['geometry']['coordinates']
    except Exception as e:
        print(f"Gagal mendapatkan rute: {e}")
        return []

def render_map():
    data = fetch_drone_data()
    default_location = [-6.2, 106.816666]
    m = folium.Map(location=default_location, zoom_start=12)

    # Lokasi pengguna (misalnya koordinat operator)
    user_location = (-6.200, 106.816)  # ← Kamu bisa ganti dengan lokasi dinamis nanti
    folium.Marker(user_location, tooltip="📍 Kamu di sini", icon=folium.Icon(color="green")).add_to(m)

    if data:
        client = openrouteservice.Client(key=ORS_API_KEY)

        for item in data:
            lat = item.get("latitude")
            lon = item.get("longitude")
            jumlah = item.get("jumlah_orang")
            waktu = item.get("timestamp", {}).get("$date", "")

            folium.Marker(
                location=[lat, lon],
                tooltip="Klik lihat detail",
                popup=f"""
                <b>Jumlah Orang:</b> {jumlah}<br>
                <b>Lokasi:</b> ({lat}, {lon})<br>
                <b>Waktu:</b> {waktu}
                """,
                icon=folium.Icon(color="red", icon="info-sign")
            ).add_to(m)

            folium.CircleMarker(
                location=[lat, lon],
                radius=jumlah * 2,
                color="blue",
                fill=True,
                fill_color="blue",
                fill_opacity=0.5,
                popup=f"{jumlah} orang",
            ).add_to(m)

        # Ambil lokasi terakhir untuk rute
        last = data[-1]
        end_coords = (last["longitude"], last["latitude"])
        start_coords = (user_location[1], user_location[0])  # (lon, lat)

        route_coords = get_route(client, start_coords, end_coords)
        if route_coords:
            route_latlon = [(coord[1], coord[0]) for coord in route_coords]
            folium.PolyLine(
                locations=route_latlon,
                color="orange",
                weight=5,
                popup="Rute Terpendek",
            ).add_to(m)

        m.location = [last["latitude"], last["longitude"]]
    else:
        folium.Marker(default_location, tooltip="Tidak ada data").add_to(m)

    st_folium(m, width=700, height=500)
