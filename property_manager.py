import requests

url = "http://127.0.0.1:8003/addresses"

address_data = {
    "name" : input("Enter your name\n"),
    "place" : input("Enter a place in Kerala\n"),
    "district" : input("Enter the district\n")
}

try:

    response = requests.post(url, json=address_data)
    response.raise_for_status()

    print("Request successful")
    print(response.json())

except requests.exceptions.HTTPError:
    print("Error returned from address service")
    error_data = response.json()
    print(error_data["detail"])

except requests.exceptions.ConnectionError:
    print("Error in connecting to address service")