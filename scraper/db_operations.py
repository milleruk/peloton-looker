import google.api_core.exceptions
import pandas as pd
from google.cloud import bigquery

# Construct a BigQuery client object.
# Make sure to point to your service account credential JSON file in an
# env variable called GOOGLE_APPLICATION_CREDENTIALS
client = bigquery.Client()


def create_tables():
    # TODO: Set the name of your project below
    dataset = 'YOUR-PROJECT.peloton.'
    tables = {"users": [
            bigquery.SchemaField("id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("username", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("cycling_workout_ftp", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("image_url", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("first_name", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("last_name", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("created_at", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("birthday", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("customized_max_heart_rate", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("default_max_heart_rate", "FLOAT", mode="NULLABLE"),
        ],
        "rides": [
            bigquery.SchemaField("id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("description", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("title", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("difficulty_estimate", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("overall_estimate", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("duration", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("fitness_discipline", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("image_url", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("instructor_id", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("language", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("original_air_time", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("overall_rating_avg", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("overall_rating_count", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("series_id", "STRING", mode="NULLABLE")
        ],
        "workouts": [
            bigquery.SchemaField("id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("created_at", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("is_total_work_personal_record", "BOOLEAN", mode="NULLABLE"),
            bigquery.SchemaField("start_time", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("status", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("total_work", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("user_id", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("v2_total_video_watch_time_seconds", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("leaderboard_rank", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("ride_id", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("ftp", "INTEGER", mode="NULLABLE")
        ],
        "instructors": [
            bigquery.SchemaField("id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("bio", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("short_bio", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("username", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("quote", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("first_name", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("last_name", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("instructor_hero_image_url", "STRING", mode="NULLABLE")
        ],
        "workout_stats": [
            bigquery.SchemaField("workout_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("output", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("cadence", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("resistance", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("speed", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("heart_rate", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("target_cadence_upper", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("target_cadence_lower", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("target_resistance_lower", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("target_resistance_upper", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("seconds_since_pedaling_start", "INTEGER", mode="NULLABLE")
        ],
        "workouts_with_stats": [
            bigquery.SchemaField("id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("created_ts", "TIMESTAMP", mode="NULLABLE"),
            bigquery.SchemaField("is_total_work_personal_record", "BOOLEAN", mode="NULLABLE"),
            bigquery.SchemaField("start_ts", "TIMESTAMP", mode="NULLABLE"),
            bigquery.SchemaField("status", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("total_work", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("user_id", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("v2_total_video_watch_time_seconds", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("leaderboard_rank", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("ride_id", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("ftp", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField(
                "stats",
                "RECORD",
                mode="REPEATED",
                fields=[
                    bigquery.SchemaField("output", "INTEGER", mode="NULLABLE"),
                    bigquery.SchemaField("avg_output_2s", "INTEGER", mode="NULLABLE"),
                    bigquery.SchemaField("avg_output_3s", "INTEGER", mode="NULLABLE"),
                    bigquery.SchemaField("cadence", "INTEGER", mode="NULLABLE"),
                    bigquery.SchemaField("avg_cadence_2s", "INTEGER", mode="NULLABLE"),
                    bigquery.SchemaField("avg_cadence_3s", "INTEGER", mode="NULLABLE"),
                    bigquery.SchemaField("resistance", "INTEGER", mode="NULLABLE"),
                    bigquery.SchemaField("avg_resistance_2s", "INTEGER", mode="NULLABLE"),
                    bigquery.SchemaField("avg_resistance_3s", "INTEGER", mode="NULLABLE"),
                    bigquery.SchemaField("speed", "FLOAT", mode="NULLABLE"),
                    bigquery.SchemaField("heart_rate", "INTEGER", mode="NULLABLE"),
                    bigquery.SchemaField("target_cadence_upper", "INTEGER", mode="NULLABLE"),
                    bigquery.SchemaField("target_cadence_lower", "INTEGER", mode="NULLABLE"),
                    bigquery.SchemaField("target_resistance_upper", "INTEGER", mode="NULLABLE"),
                    bigquery.SchemaField("target_resistance_lower", "INTEGER", mode="NULLABLE"),
                    bigquery.SchemaField("seconds_since_pedaling_start", "INTEGER", mode="NULLABLE"),
                    bigquery.SchemaField("seconds_elapsed", "INTEGER", mode="NULLABLE"),
                ]
            )
        ]
    }

    for t, s in tables.items():
        table_id = dataset + t
        try:
            client.get_table(table_id)  # Make an API request.
            print("Table {} already exists.".format(table_id))
        except google.api_core.exceptions.NotFound:
            table = bigquery.Table(table_id, schema=s)
            if t == 'workouts_with_stats':
                table.time_partitioning = bigquery.TimePartitioning(
                    type_=bigquery.TimePartitioningType.DAY,
                    field="created_ts"
                )
                table.clustering_fields = ["user_id"]
            table = client.create_table(table)  # Make an API request.
            print(
                "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
            )


def get_workouts_from_db():
    # This assumes that workouts you've already retrieved are stored in the `peloton.workouts`
    # table in your BigQuery project. If you're using another database or other table/dataset names,
    # you'll need to adjust this accordingly.
    print("Checking database for workouts that have already been retrieved")

    ids_in_db, ride_ids_in_db = set(), set()
    try:
        # Fetch all workout ids and ride_ids already in BigQuery
        query_string = "SELECT id, ride_id FROM `peloton.workouts`"
        workouts_in_db = client.query(query_string).result()
        # Convert the ids fetched to sets
        for row in workouts_in_db:
            ids_in_db.add(row.id)
            ride_ids_in_db.add(row.ride_id)
        print(f'{len(ids_in_db)} workouts have already been retrieved.')
    except google.api_core.exceptions.NotFound:
        print("workouts table doesn't exist yet ")

    return ids_in_db, ride_ids_in_db


def write_to_db(w_list, r_list, p_list, user_id):
    if w_list:
        print(f'Uploading data for {user_id} to BigQuery')
        upload_to_bq(w_list, "workouts")

        if r_list:
            upload_to_bq(r_list, "rides")

        if p_list:
            upload_to_bq(p_list, "workout_stats")

    else:
        print(f'No new data for {user_id} to upload')


def upload_to_bq(data, t_name, disposition="append"):
    # Workout stats is a list of dictionaries of lists (each item in the outer list represents one workout)
    if t_name == "workout_stats":
        df = pd.DataFrame()
        for workout in data:
            df_intermediate = pd.DataFrame.from_dict(workout, orient='index').transpose()
            if df.empty:
                df = df_intermediate
            else:
                 df = pd.concat([df_intermediate], ignore_index=True)
    # Other data is a list of dictionaries and can be converted into a dataframe directly
    else:
        df = pd.DataFrame(data)

    # Configure the load job, appending data to the existing tables and auto-detecting the schema
    # from the dataframes
    job_config = bigquery.LoadJobConfig(
        autodetect=True,
        write_disposition="WRITE_APPEND",
    )

    # For certain jobs we want to overwrite the data, rather than appending
    if disposition == "overwrite":
        job_config.write_disposition = "WRITE_TRUNCATE"

    job = client.load_table_from_dataframe(
        df, f'peloton.{t_name}', job_config=job_config
    )
    job.result()  # Wait for the job to complete.

    table = client.get_table(f'peloton.{t_name}')  # Make an API request.
    print(f'Table peloton.{t_name} now has {table.num_rows} rows')


def transform_workout_stats():
    # BigQuery likes having hierarchical data nested, so as a last step, we nest all the stats about workouts
    # inside the metadata about the workout.
    try:
        query = """INSERT INTO peloton.workouts_with_stats
        WITH
          calculated_stats AS (
          SELECT
            workout_id
            , output
            , AVG(output) OVER (PARTITION BY workout_id ORDER BY seconds_since_pedaling_start 
                                ROWS BETWEEN 1 PRECEDING AND CURRENT ROW) AS avg_output_2s
            , AVG(output) OVER (PARTITION BY workout_id ORDER BY seconds_since_pedaling_start 
                                ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS avg_output_3s
            , cadence
            , AVG(cadence) OVER (PARTITION BY workout_id ORDER BY seconds_since_pedaling_start 
                                ROWS BETWEEN 1 PRECEDING AND CURRENT ROW) AS avg_cadence_2s
            , AVG(cadence) OVER (PARTITION BY workout_id ORDER BY seconds_since_pedaling_start 
                                ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS avg_cadence_3s
            , resistance
            , AVG(resistance) OVER (PARTITION BY workout_id ORDER BY seconds_since_pedaling_start 
                                    ROWS BETWEEN 1 PRECEDING AND CURRENT ROW) AS avg_resistance_2s
            , AVG(resistance) OVER (PARTITION BY workout_id ORDER BY seconds_since_pedaling_start 
                                    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS avg_resistance_3s
            , speed
            , heart_rate
            , target_cadence_upper
            , target_cadence_lower
            , target_resistance_lower
            , target_resistance_upper
            , seconds_since_pedaling_start
            , seconds_since_pedaling_start - LAG(seconds_since_pedaling_start) OVER 
                                    (PARTITION BY workout_id ORDER BY seconds_since_pedaling_start) AS seconds_elapsed
          FROM
            peloton.workout_stats )
        SELECT
          id
          , TIMESTAMP_SECONDS(created_at) AS created_ts
          , is_total_work_personal_record
          , TIMESTAMP_SECONDS(start_time) AS start_ts
          , status
          , total_work
          , user_id
          , v2_total_video_watch_time_seconds
          , leaderboard_rank
          , ride_id
          , ftp
          , ARRAY_AGG( STRUCT( 
              output
              , CAST(ROUND(avg_output_2s, 0) AS INT64)
              , CAST(ROUND(avg_output_3s, 0) AS INT64)
              , cadence
              , CAST(ROUND(avg_cadence_2s, 0) AS INT64)
              , CAST(ROUND(avg_cadence_3s, 0) AS INT64)
              , resistance
              , CAST(ROUND(avg_resistance_2s, 0) AS INT64)
              , CAST(ROUND(avg_resistance_3s, 0) AS INT64)
              , speed
              , heart_rate
              , target_cadence_upper
              , target_cadence_lower
              , target_resistance_lower
              , target_resistance_upper
              , seconds_since_pedaling_start
              , seconds_elapsed )) AS stats
        FROM
          `peloton.workouts` w
        LEFT JOIN
          calculated_stats ws
        ON
          ws.workout_id = w.id
        WHERE id NOT IN (SELECT id FROM peloton.workouts_with_stats)
        GROUP BY
          1,2,3,4,5,6,7,8,9,10,11"""
        client.query(query)
        # Convert the ids fetched to sets
        print("The stats data was transformed")
    except:
        print("The transform query failed")
