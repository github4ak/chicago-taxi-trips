from google.cloud import bigquery
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from google.oauth2 import service_account
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

def findPeakHour(query_string):
    count_prt_15mins = []
    query_job = client.query(query_string)
    for row in query_job:
        print(row)
        count_prt_15mins.append(row[0])
    print(len(count_prt_15mins))
    time_array = []
    i = 0
    while i < 24:
        time_array.append(i+0.00)
        time_array.append(i+0.15)
        time_array.append(i + 0.30)
        time_array.append(i + 0.45)
        i = i+1
    # print("lets print time array")
    # print("The time array is ",len(time_array))
    figure( figsize=(10, 10), dpi=80, edgecolor='red')

    plt.scatter((time_array),(count_prt_15mins), alpha=0.5)
    plt.xlabel("Time")
    plt.ylabel("Count of trips of all years")
    plt.show()
    return 0

# query_string = """
#                 SELECT count(1), EXTRACT(Time FROM trip_start_timestamp ) As time, EXTRACT(MONTH FROM trip_start_timestamp) AS month,  EXTRACT(YEAR FROM trip_start_timestamp) AS year,
# From `bigquery-public-data.chicago_taxi_trips.taxi_trips`
# GROUP BY time,year, month
# Order By time,  year, month
#                """

#
# query_string = """
#                 SELECT count(1), EXTRACT(Time FROM trip_start_timestamp ) As time
# From `bigquery-public-data.chicago_taxi_trips.taxi_trips`
# GROUP BY time
# Order By time
#
#                """

##Collect all data points in that time
# query_string = """
#                 SELECT trip_start_timestamp
#                 From `bigquery-public-data.chicago_taxi_trips.taxi_trips`
#                 where EXTRACT(Time FROM trip_start_timestamp )IN (Select EXTRACT(Time FROM trip_start_timestamp ) As time From `bigquery-public-data.chicago_taxi_trips.taxi_trips`
#                 GROUP BY time
#                 Order By time)
#                 Order By EXTRACT(Time FROM trip_start_timestamp )
#                """

query_string = """
                    SELECT trip_start_timestamp
                    From `bigquery-public-data.chicago_taxi_trips.taxi_trips`
                    where EXTRACT(time FROM trip_start_timestamp ) <= (Select EXTRACT(time FROM trip_start_timestamp )As time From `bigquery-public-data.chicago_taxi_trips.taxi_trips`
                    GROUP BY time
                    Order By time)
                    Order By EXTRACT(Time FROM trip_start_timestamp )
                """

findPeakHour(query_string)
