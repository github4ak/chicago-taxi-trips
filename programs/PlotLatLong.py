from google.cloud import bigquery
from google.oauth2 import service_account
import pandas
import matplotlib
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import tkinter

matplotlib.use('TkAgg')
credentials = service_account.Credentials.from_service_account_file(
    "/home/shaurya/Downloads/My Project-d5ff0302208b.json",
    scopes=["https://www.googleapis.com/auth/cloud-platform"]
)

client = bigquery.Client(
    credentials=credentials,
    project=credentials.project_id,
)

taxi_trip_dataset_ref = bigquery.dataset.DatasetReference('bigquery-public-data', 'chicago_taxi_trips')

taxi_trip_dset = client.get_dataset(taxi_trip_dataset_ref)

taxi_trips_table = client.get_table(taxi_trip_dset.table('taxi_trips'))

pickup_query = """
                    SELECT
                       pickup_latitude, pickup_longitude, dropoff_latitude, dropoff_longitude
                    FROM
                      `bigquery-public-data.chicago_taxi_trips.taxi_trips`
                    WHERE
                      pickup_latitude is not NULL AND 
                      pickup_longitude is not NULL AND 
                      dropoff_latitude is not NULL AND
                      dropoff_longitude is not NULL AND
                      trip_start_timestamp >= '2016-01-01' AND 
                      trip_start_timestamp <= '2016-12-31'
                """

pickup_latitudes = []
pickup_longitudes = []

dropoff_latitudes = []
dropoff_longitudes = []

query_job = client.query(pickup_query)

for row in query_job:
    print(row)
    pickup_latitudes.append(row[0])
    pickup_longitudes.append(row[1])
    dropoff_latitudes.append(row[2])
    dropoff_longitudes.append(row[3])

fig, ax = plt.subplots(figsize=(8, 7))
plt.scatter(pickup_longitudes)
plt.scatter(dropoff_latitudes, dropoff_longitudes, color="#bcbd22")
plt.show()
