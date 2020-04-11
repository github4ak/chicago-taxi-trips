from google.cloud import bigquery
import matplotlib.pyplot as plt
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



def query_func(q_string):
    trip_count = []
    query_job = client.query(q_string)
    for row in query_job:
        #print(row)
        trip_count.append(row[2])
    return trip_count

short_trip_query = """
            SELECT EXTRACT(MONTH FROM trip_start_timestamp) AS month,EXTRACT(YEAR FROM trip_start_timestamp) AS YEAR, count(1) as Count
From `bigquery-public-data.chicago_taxi_trips.taxi_trips`
WHERE trip_miles <= 30
GROUP BY  MONTH,YEAR
ORDER BY YEAR, MONTH

        """

long_trip_query = """
                    SELECT EXTRACT(MONTH FROM trip_start_timestamp) AS month,EXTRACT(YEAR FROM trip_start_timestamp) AS YEAR, count(1) as Count
                    From `bigquery-public-data.chicago_taxi_trips.taxi_trips`
                    WHERE trip_miles > 30
                    GROUP BY  MONTH,YEAR
                    ORDER BY YEAR, MONTH
                  """

month = [1,2,3,4,5,6,7,8,9,10,11,12]
year = [2013,2014,2015,2016,2017,2018,2019]
short_trips_count = query_func(short_trip_query)
long_trips_count =  query_func(long_trip_query)

avg_shorttrip_count = []
avg_longtrip_count = []

for i in range(0,len(year)):
    yr = year[i]
    countof_short_trips = short_trips_count[i:i+12]
    countof_long_trips = long_trips_count[i:i+12]
    avg_shorttrip_count.append(sum(countof_short_trips)/12)
    avg_longtrip_count.append(sum(countof_long_trips)/12)
    # To plot month wise count
    # print(countof_long_trips)
    # plt.xlabel("Month")
    # plt.ylabel("Count of trips")
    #
    # plt.plot( month,countof_short_trips, color="green")
    # plt.plot( month,countof_long_trips, color = "red")
    # plt.suptitle(yr)
    # plt.legend(["Y = Count of Short Trips", " Y = Count of long trips"])
    # plt.show()

# print(avg_shorttrip_count)
# print(avg_longtrip_count)

##CDF of year vs count
for index,count in enumerate(avg_shorttrip_count):
    if index != 0:
        avg_shorttrip_count[index] += avg_shorttrip_count[index-1]+count
for index,count in enumerate(avg_longtrip_count):
    if index != 0:
        avg_longtrip_count[index] += avg_longtrip_count[index-1]+count

# print(len(year),(avg_shorttrip_count))
# print((avg_longtrip_count))

plt.plot(year,avg_shorttrip_count, c="green")
plt.plot(year, avg_longtrip_count, c = "red")
plt.xlabel("Year")
plt.ylabel("Count of trips")
plt.legend(["Y = Count of Short Trips", " Y = Count of long trips"],loc="upper left")
plt.show()