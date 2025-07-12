
from pyspark.sql import SparkSession, types
from math import radians, sin, cos, sqrt, atan2
from pyspark.sql import functions as F
from pyspark.sql.types import DoubleType

spark = SparkSession.builder.appName('GHCN Extracter').getOrCreate()

ghcn_path = '/courses/datasets/ghcn-splits'
ghcn_stations = '/courses/datasets/ghcn-more/ghcnd-stations.txt'
season_schedule_file = '/user/kba89/.sparkStaging/2018_season_schedule.csv'  # Your 2018 season schedule file
output = 'ghcn-subset'

observation_schema = types.StructType([
    types.StructField('station', types.StringType(), False),
    types.StructField('date', types.StringType(), False),
    types.StructField('observation', types.StringType(), False),
    types.StructField('value', types.IntegerType(), False),
    types.StructField('mflag', types.StringType(), False),
    types.StructField('qflag', types.StringType(), False),
    types.StructField('sflag', types.StringType(), False),
    types.StructField('obstime', types.StringType(), False),
])

station_schema = types.StructType([
    types.StructField('station', types.StringType(), False),
    types.StructField('latitude', types.FloatType(), False),
    types.StructField('longitude', types.FloatType(), False),
    types.StructField('elevation', types.FloatType(), False),
    types.StructField('name', types.StringType(), False),
])

season_schedule_schema = types.StructType([
    types.StructField('Round', types.StringType(), False),
    types.StructField('Race Name', types.StringType(), False),
    types.StructField('Circuit ID', types.StringType(), False),
    types.StructField('Circuit Name', types.StringType(), False),
    types.StructField('Locality', types.StringType(), False),
    types.StructField('Country', types.StringType(), False),
    types.StructField('Latitude', types.FloatType(), False),
    types.StructField('Longitude', types.FloatType(), False),
    types.StructField('Date', types.DateType(), False),
    types.StructField('Time', types.TimestampType(), False),
])


def station_data(line):
    return [line[0:11].strip(), float(line[12:20]), float(line[21:30]), float(line[31:37]), line[41:71].strip()]

def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    R = 6371
    distance = R * c
    return distance

def main():
        sc = spark.sparkContext

        ## Stations data...
        stations_rdd = sc.textFile(ghcn_stations).map(station_data)
        stations = spark.createDataFrame(stations_rdd, schema=station_schema).hint('broadcast')

        schedule_df = spark.read.csv(season_schedule_file, header=True, schema=season_schedule_schema)
        schedule_df = schedule_df.select('Round', 'Locality', 'Country', 'Latitude', 'Longitude', 'Date')

        schedule_df = schedule_df.withColumnRenamed('Latitude', 'sched_lat').withColumnRenamed('Longitude', 'sched_lon')
        stations = stations.withColumnRenamed('latitude', 'stations_lat').withColumnRenamed('longitude', 'stations_lon')
        schedule_df = schedule_df.withColumnRenamed('Date', 'schedule_date')

        joined = schedule_df.crossJoin(stations)
        joined = joined.withColumn(
            'distance',
            F.udf(lambda lat1, lon1, lat2, lon2: haversine(lat1, lon1, lat2, lon2), DoubleType())(
                joined['sched_lat'], joined['sched_lon'], joined['stations_lat'], joined['stations_lon']
            )
        )
        filtered_stations = joined.filter(
            (F.abs(joined['sched_lat'] - joined['stations_lat']) <= 0.7) &
            (F.abs(joined['sched_lon'] - joined['stations_lon']) <= 0.7)
        )
        closest_stations = filtered_stations.groupBy('sched_lat', 'sched_lon').agg(
            F.min('distance').alias('min_distance')
        )
        closest_stations = closest_stations.join(filtered_stations,
                                                 (closest_stations['sched_lat'] == filtered_stations['sched_lat']) &
                                                 (closest_stations['sched_lon'] == filtered_stations['sched_lon']) &
                                                 (closest_stations['min_distance'] == filtered_stations['distance'])
                                                  ).drop('min_distance')
        closest_stations = closest_stations.withColumn('schedule_date', F.to_date('schedule_date'))
        closest_stations = closest_stations.withColumnRenamed('station', 'closest_station')
        closest_stations = closest_stations.select('Round','Locality', 'Country', 'schedule_date','closest_station')
        closest_stations = closest_stations.cache()
        closest_stations.show(22)

        closest_stations = closest_stations.coalesce(1)
        closest_stations = closest_stations.orderBy('Round')
        closest_stations.write.csv(output + '/2018_closest_stations', mode='overwrite', header=True, compression='gzip')



        # ## Observations data...
        # obs = spark.read.csv(ghcn_path, header=None, schema=observation_schema)
        #
        # ## Filter observations to match year and valid data
        # obs = obs.filter((obs['date'] == 2018))
        # obs = obs.filter(functions.isnull(obs['qflag']))
        # obs = obs.drop(obs['mflag']).drop(obs['qflag']).drop(obs['sflag']).drop(obs['obstime'])
        # obs = obs.filter(obs['observation'].isin('TMAX', 'TMIN', 'PRCP', 'WND', 'HMD', 'PRES'))
        #
        # # Parse the date string into a real date object
        # obs = obs.withColumn('newdate', functions.to_date(obs['date'], 'yyyyMMdd'))
        # obs = obs.drop('date').withColumnRenamed('newdate', 'date')
        # obs.show(20)
        # obs = obs.join(closest_stations.hint("broadcast"), (obs['station'] == closest_stations['closest_station'] )& (obs['date'] == closest_stations['schedule_date']))
        # #obs = obs.filter(obs['date'] == obs['schedule_date']).drop('date')
        # obs = obs.drop('date')
        # obs = obs.cache()
        # ## Calculate Mean Weather Data
        # mean_weather = obs.groupBy('Locality', 'Country', 'schedule_date', 'Round', 'observation').agg(
        #     functions.mean('value').alias('mean_value')
        # )
        # mean_weather = mean_weather.withColumn('year', functions.lit(2022))
        # # # Debug: Show the first few rows of the mean weather data
        # # print("Mean Weather Data:")
        # # mean_weather.show(5)
        #
        # # Save Results
        # mean_weather = mean_weather.coalesce(1)

main()