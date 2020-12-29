
import folium

map_1 = folium.Map(location=[45.372, -121.6972], zoom_start=12, tiles='Stamen Terrain')

tooltip = "Click me!"

folium.Marker([45.3288, -121.6625], popup="<i>Mt. Hood Meadows</i>", tooltip=tooltip).add_to(map_1)
folium.Marker([45.3311, -121.7113], popup="<b>Timberline Lodge</b>", tooltip=tooltip).add_to(map_1)

f = map_1._repr_html_()

print(f)

