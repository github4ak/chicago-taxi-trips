from google.cloud import bigquery
client = bigquery.Client()
#taxi_trip_dataset_ref = client.dataset('chicago_taxi_trips', project='bigquery-public-data')
taxi_trip_dataset_ref = bigquery.dataset.DatasetReference('bigquery-public-data', 'chicago_taxi_trips')
#print(type(taxi_trip_dataset_ref))

taxi_trip_dset = client.get_dataset(taxi_trip_dataset_ref)

#print(type(taxi_trip_dataset_ref))

#print(client.list_tables(taxi_trip_dset))

#Below command gives the table name for the dataset
#print([x.table_id for x in client.list_tables(taxi_trip_dset)])

#Using this table name we can query table from big query api
taxi_trips_table = client.get_table(taxi_trip_dset.table('taxi_trips'))
#print(taxi_trips_table)

#Methods which we can apply on the class
#print(dir(taxi_trips_table))

#print([command for command in dir(taxi_trips_table) if  not command.startswith('_')])

#print(taxi_trips_table.schema)

# for schema_col in taxi_trips_table.schema:
#     print(schema_col)

# For getting taxi trip id
schema_subset_txi_id = [col for col in taxi_trips_table.schema if col.name in ('taxi_id')]

#print(schema_subset_txi_id)

# results = [x for x in client.list_rows(taxi_trips_table, start_index=0, selected_fields=schema_subset_txi_id, max_results=10)]
# results_taxi_id = [x for x in client.list_rows(taxi_trips_table, start_index=0, selected_fields=schema_subset_txi_id, max_results=10)]

# print(results)
#
# for i in results_taxi_id:
#     print(dict(i))

######Info about pickup location
pickup_location = [col for col in taxi_trips_table.schema if col.name in ('pickup_location')]
#
# # print(type(pickup_location))
#
#
# pickup_location_res = [x for x in client.list_rows(taxi_trips_table, start_index = 0, selected_fields=pickup_location, max_results=100)]
# print(pickup_location_res)
#

query1 = """SELECT
  EXTRACT(DAYOFWEEK FROM trip_start_timestamp) AS day,
  FORMAT('%3.2f', MAX(fare)) AS maximum_fare,
  FORMAT('%3.2f', MIN(fare)) AS minimum_fare,
  FORMAT('%3.2f', AVG(fare)) AS avg_fare,
  FORMAT('%3.2f', STDDEV(fare)) AS std_dev_fare,
  COUNT(1) AS rides
FROM
  `bigquery-public-data.chicago_taxi_trips.taxi_trips`
WHERE
  trip_seconds >= 600
GROUP BY
  day
ORDER BY
  day
        """

query_job = client.query(query1)

print("The query data:")
for row in query_job:
    # Row values can be accessed by field name or index.
    print(row)
