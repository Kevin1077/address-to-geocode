import requests

def geocode(address):
    url = "https://nominatim.openstreetmap.org/search"

    query_parameters = {
        "format" : "json",
        "q" : address
    }

    headers = {
        "User-Agent" : "KeralaAddresslearning/1.0"
    }

    try:

        response = requests.get(
            url,
            params=query_parameters,
            headers=headers
        )

        response.raise_for_status()

    except requests.RequestException:
        return None

    data = response.json()

    if len(data) == 0:
        return None

    best_result = max(data, key=lambda result: result["importance"])

    latitude = float(best_result["lat"])
    longitude = float(best_result["lon"])

    return {
        "address" : best_result["display_name"],
        "latitude" : latitude,
        "longitude" : longitude
    }
