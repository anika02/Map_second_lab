import folium
import geopy
from geopy.geocoders import Nominatim
import haversine


def input_from_file(file_name, year):
    """str -> list/bool
    Returns the list of lists(film, year, where) of the movies of a certain year

    >>> input_from_file('','2015')
    False
    >>> input_from_file('','')
    False
    """
    if not file_name or not year:
        return False
    f = open(file_name, encoding='utf-8', errors='ignore')
    data = f.readline()
    while not data.startswith("=============="):
        data = f.readline()

    # знаходимось на початку списку
    lst = []
    i = 0
    for line in f:
        if line.startswith("--------------------------------------------------------------------------------"):
            break  # кінець списку
        if line.split('(')[1][:4] == year:
            if line.strip()[-1] == ')':
                help_lst = [line.strip().split('(')[0].strip(), line.split(
                    '(')[1][:4], ")".join(line.split(')')[-2:]).split('}')[-1].strip()]
            else:
                help_lst = [line.strip().split('(')[0].strip(), line.split(
                    '(')[1][:4], line.split(')')[-1].split('}')[-1].strip()]
            if help_lst not in lst:
                lst.append(help_lst)
                i += 1
            if i == 20000:
                break  # обмеження на кількість фільмів
    f.close()
    return lst


location_user = [49.817545, 24.023932]
loc_1 = input().split('.')
loc_2 = input().split('.')
loc_1 = int(loc_1[0]) + int(loc_1[1])/(10 ^ (len(loc_1[1])))
loc_2 = int(loc_2[0]) + int(loc_2[1])/(10 ^ (len(loc_2[1])))

lst = input_from_file("C:\sec_semester\locations.list", '1916')
print(len(lst))
map_1 = folium.Map(location=[loc_1, loc_2], zoom_start=50)
lst = lst[:50]

geolocator = Nominatim(user_agent="specify_your_app_name_here", timeout= 3)
result_lst = []
for i in lst:
    try:
        result_lst.append([i[0], geolocator.geocode(i[2]).latitude, geolocator.geocode(
            i[2]).longitude])
    except:
        pass
result_lst.sort(key=lambda x: haversine.haversine((loc_1, loc_2),(x[1], x[2])))#(x[1]-loc_1)**2 + (x[2]-loc_2)**2)
result_lst = result_lst[:10]


fg = folium.FeatureGroup(name="first_map")
for name, lt, ln in result_lst:
    fg.add_child(folium.Marker(location= [lt, ln], popup= name, icon=folium.Icon()))
map_1.add_child(fg)
map_1.save('Map_1.html')

# data = pandas.read_csv("Stan_1900.csv", error_bad_lines=False)
# lat = data['lat']
# lon = data['lon']
# map = folium.Map(location=[48.314775, 25.082925], zoom_start=10)
# fg = folium.FeatureGroup(name="Kosiv map")
# for lt, ln in zip(lat, lon):
#     fg.add_child(folium.Marker(
#         location=[lt, ln], popup="1900 рік", icon=folium.Icon()))
# map.add_child(fg)
# map.save('Map_5.html')

# lst = input_from_file("C:\sec_semester\locations.list", '1962')
# print(len(lst))
