from google.cloud import bigquery
import matplotlib.pyplot as plt
from google.oauth2 import service_account
import numpy as np
import pandas as pd


credentials = service_account.Credentials.from_service_account_file(
    "/Users/sushmitha/PycharmProjects/dmproject/authentication_key.json",
    scopes=["https://www.googleapis.com/auth/cloud-platform"]
)
client = bigquery.Client(
    credentials=credentials,
    project=credentials.project_id,
)

taxi_trip_dataset_ref = client.dataset('chicago_taxi_trips', project='bigquery-public-data')
taxi_trip_dataset_ref = bigquery.dataset.DatasetReference('bigquery-public-data', 'chicago_taxi_trips')

taxi_trip_dset = client.get_dataset(taxi_trip_dataset_ref)

taxi_trips_table = client.get_table(taxi_trip_dset.table('taxi_trips'))


tip_query_day = """
                SELECT 
                AVG(tips), 
                EXTRACT(MONTH FROM trip_start_timestamp ) As month, 
                EXTRACT(YEAR FROM trip_start_timestamp ) As year,
                From
                 `bigquery-public-data.chicago_taxi_trips.taxi_trips`
                WHERE   Extract(time from trip_start_timestamp) > "06:00:00" and Extract(time from trip_start_timestamp) < "22:00:00"and Extract(time from trip_end_timestamp) < "22:00:00" and Extract(time from trip_end_timestamp) > "06:00:00"
                GROUP BY month, year
                Order By Year, Month
            """

avg_day = []
month = [1,2,3,4,5,6,7,8,9,10,11,12]
year = [2013,2014,2015,2016,2017,2018,2019,2020]
query_job = client.query(tip_query_day)
for row in query_job:
    # print(row)
    avg_day.append(row[0])

tip_query_night = """
                    SELECT AVG(tips), EXTRACT(MONTH FROM trip_start_timestamp ) As month, EXTRACT(YEAR FROM trip_start_timestamp ) As year,
                    From `bigquery-public-data.chicago_taxi_trips.taxi_trips`
                    WHERE (Extract(time from trip_start_timestamp) >= "22:00:00" OR Extract(time from trip_start_timestamp) <= "06:00:00" )and (Extract(time from trip_end_timestamp) < "06:00:00" OR Extract(time from trip_end_timestamp) > "22:00:00")
                    GROUP BY month, year
                    Order By Year, Month

                    """

avg_night = []
query_job = client.query(tip_query_night)
for row in query_job:
    # print(row)
    avg_night.append(row[0])


print(avg_day)
print(avg_night)
for i in range(0,len(year)-1):
    yr = year[i]
    avg_cur_year_day = avg_day[i:i+12]
    avg_cur_year_night = avg_night[i:i+12]
    plt.xlabel("Month")
    plt.ylabel("Avg Tip")

    plt.plot(month,avg_cur_year_day, color="green")
    plt.plot(month,avg_cur_year_night, color = "red")
    plt.suptitle(yr)
    plt.legend(["Y = Avg Tip Per Day", " Y = Avg Tip per Night"])
    plt.show()

