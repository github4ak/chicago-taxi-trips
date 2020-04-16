import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['figure.figsize']=(20,36)
from sklearn.cluster import MiniBatchKMeans, KMeans

""""
Queried in BigQuery and saved as .csv file
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
  trip_start_timestamp <= '2016-01-31'
"""


data = pd.read_csv('../files/2016_Jan_New.csv')
test = pd.read_csv('../files/2016_Jan_New.csv')

# K_clusters = range(1,8)
# kmeans = [KMeans(n_clusters=i) for i in K_clusters]
# pickup_Y_axis = data[['pickup_latitude']]
# pickup_X_axis = data[['pickup_longitude']]
# dropoff_Y_axis = data[['dropoff_latitude']]
# dropoff_X_axis = data[['dropoff_longitude']]
#
# score_pickup = [kmeans[i].fit(pickup_X_axis).score(pickup_Y_axis) for i in range(len(kmeans))]
# score_dropoff = [kmeans[i].fit(dropoff_X_axis).score(dropoff_Y_axis) for i in range(len(kmeans))]
# # Visualize
# plt.plot(K_clusters, score_pickup)
# plt.plot(K_clusters,score_dropoff)
# plt.xlabel('Number of Clusters')
# plt.ylabel('Score')
# plt.title('Elbow Curve')

coord_pickup = np.vstack((data[['pickup_latitude', 'pickup_longitude']].values,
                          test[['pickup_latitude', 'pickup_longitude']].values))

coord_dropoff = np.vstack((data[['dropoff_latitude', 'dropoff_longitude']].values,
                           test[['dropoff_latitude', 'dropoff_longitude']].values))

coords = np.hstack((coord_pickup,coord_dropoff))

sample_ind = np.random.permutation(len(coords))[:500000]

kmeans = MiniBatchKMeans(n_clusters=4, batch_size=10000).fit(coords[sample_ind])
for df in (data,test):
    df.loc[:, 'pickup_dropoff_loc'] = kmeans.predict(df[['pickup_latitude', 'pickup_longitude',
                                                         'dropoff_latitude','dropoff_longitude']]) + 1

kmean4_data = data[['pickup_dropoff_loc']]
kmean4_test = test[['pickup_dropoff_loc']]

data.to_csv('../files/kmean4_data.csv',index=False,columns = ['pickup_dropoff_loc'])
test.to_csv('../files/kmean4_test.csv',index=False,columns = ['pickup_dropoff_loc'])

# plt.figure(figsize=(64,64))
# N = 10
# for i in range(4):
#     plt.subplot(2,2,i+1)
#     tmp_data = data[data.pickup_dropoff_loc==i]
#     drop = plt.scatter(tmp_data['dropoff_longitude'][:N], tmp_data['dropoff_latitude'][:N], s=10, lw=0, alpha=0.5,label='dropoff')
#     pick = plt.scatter(tmp_data['pickup_longitude'][:N], tmp_data['pickup_latitude'][:N], s=10, lw=0, alpha=0.4,label='pickup')
#     plt.xlim([-87.913624596,-87.534902901]);
#     plt.ylim([41.660136051,42.021223593])
#     plt.legend(handles = [pick,drop])
#     plt.title('clusters %d'%i)
# plt.show()


