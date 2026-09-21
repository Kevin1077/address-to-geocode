import psycopg
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from database import get_connection
from geocoder import geocode

app = FastAPI()

class AddressRequest(BaseModel):
    name : str
    place : str
    district : str

class AddressResponse(BaseModel):
    id : int
    latitude : float
    longitude : float

@app.post(
"/addresses",
    response_model=AddressResponse,
    status_code=201
)
def create_address(address : AddressRequest):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO addresses(name, place, district)
            VALUES (%s, %s, %s)
            RETURNING id
            """,
            (address.name, address.place, address.district)
        )

        row = cursor.fetchone()
        new_id = row[0]

        address_text = f"{address.place}, {address.district}, Kerala"

        result = geocode(address_text)

        if result is None:
            connection.rollback()
            raise HTTPException(
                status_code=400,
                detail="Cant find corresponding geocode"
            )

        cursor.execute(
            """
            INSERT INTO geolocation(address_id, latitude, longitude)
            VALUES (%s, %s, %s)
            RETURNING id, address_id, latitude, longitude
            """,
            (new_id, result["latitude"], result["longitude"])
        )

        geo_row = cursor.fetchone()
        connection.commit()

        return {
            "id" : new_id,
            "latitude" : geo_row[2],
            "longitude" : geo_row[3]
        }

    except psycopg.Error:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()





