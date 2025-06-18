# utils/geocode_utils.py

import requests

def get_coords_from_place(place):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": place, "format": "json", "limit": 1}
    headers = {"User-Agent": "tdx-parking-service"}

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        if not data:
            return None, "查無地址"

        lat = float(data[0]["lat"])
        lon = float(data[0]["lon"])
        return (lat, lon), None

    except requests.RequestException as e:
        return None, str(e)
