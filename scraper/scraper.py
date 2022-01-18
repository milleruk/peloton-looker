import os
import sys
import time
import requests

from db_operations import get_workouts_from_db, write_to_db, upload_to_bq, create_tables, transform_workout_stats

# Load Peloton information and get a session
username = os.environ.get('USERNAME')
pw = os.environ.get('PASSWORD')
s = requests.Session()
base_url = 'https://api.onepeloton.com'
payload = {'username_or_email': username, 'password': pw}


def get_user_data(user_id, workouts_already_fetched, rides_already_fetched):
    ride_list, workout_list, perf_list = [], [], []
    page, last_page, get_more = 0, 0, True

    # The Peloton API is paginated and returns workout in reverse chronological order
    # We only want to fetch pages as long as they contain workouts not yet in the database.
    while page < last_page + 1 and get_more:
        print(f'Retrieving page {page} of workouts for {user_id}')
        workouts, last_page = get_ride_ids(user_id, page)
        # Advance to the next page
        page = page + 1

        for w in workouts:
            if w not in workouts_already_fetched:
                w_info, r_info, ws_info = get_workout(w)
                if not w_info:
                    break
                # The information about the workout is always new, so we add that to our list
                workout_list.append(w_info)
                # We may already have information about the ride from another rider or a past workout
                # on this ride, so we check to make sure we're not adding duplicate information
                if r_info["id"] not in rides_already_fetched:
                    ride_list.append(r_info)
                    rides_already_fetched.add(r_info["id"])
                # Only some workouts have detailed performance
                if ws_info:
                    perf_list.append(ws_info)
            # When we reach a workout that is already in the database, we mark that and stop
            # fetching information about other workouts further in the past, since presumably
            # we already have those as well.
            else:
                # Once we reach a workout that's already in the database, there's no reason
                # to fetch additional pages of workouts from the API
                get_more = False
                break

    write_to_db(workout_list, ride_list, perf_list, user_id)


def get_ride_ids(user_id, page_number=0):

    # Fetch data about 50 workouts from the Peloton API
    page = s.get(f'{base_url}/api/user/{user_id}/workouts?limit=50', params={'page': page_number}).json()
    # Extract the ride_ids (rides are the classes and workouts are an instance of a user taking a ride)
    ride_ids = [r['id'] for r in page["data"]]
    # Notate how many pages of workouts exist for this user
    last_page = page["page_count"]

    return ride_ids, last_page


def get_workout(workout_id):
    print(f'Retrieving information about workout {workout_id} from Peloton')
    # The /workout endpoint returns information about the ride and the workout
    try:
        ride = s.get(f'{base_url}/api/workout/{workout_id}', timeout=10).json()
    # If the request times out, take a break to let the rate limit reset
    except requests.exceptions.ReadTimeout:
        print("Pausing to reset rate limit")
        time.sleep(60)
        ride = s.get(f'{base_url}/api/workout/{workout_id}', timeout=10).json()
        if not ride:
            sys.exit("Too many failures. Quitting.")

    r_cols = ["id", "description", "title", "difficulty_estimate", "overall_estimate", "duration", "fitness_discipline",
              "image_url", "instructor_id", "language", "original_air_time", "overall_rating_avg",
              "overall_rating_count", "series_id"]
    w_cols = ["id", "created_at", "is_total_work_personal_record", "start_time", "status", "total_work", "user_id",
              "v2_total_video_watch_time_seconds", "leaderboard_rank"]

    # Extract the columns (listed above) that we care about for the ride and workout
    ride_info = {k: ride["ride"][k] for k in r_cols if k in ride["ride"]}
    workout_info = {k: ride[k] for k in w_cols if k in ride}

    # The workout doesn't contain a scalar linking it to what ride it was, so add one
    workout_info["ride_id"] = ride_info["id"]

    # Only some rides contain ftp_info
    if "ftp_info" in ride:
        workout_info["ftp"] = ride["ftp_info"]["ftp"]

    # Cycling workouts contain more detailed stats at another API endpoint
    if ride["fitness_discipline"] == "cycling":
        workout_stats_info = get_workout_stats(workout_id)
    else:
        workout_stats_info = []

    return workout_info, ride_info, workout_stats_info


def get_workout_stats(workout_id):
    # The /workout/{id}/performance_graph endpoint returns detailed statistics about performance
    # on cycling workouts. We can set the granularity with the every_n parameter. Here it
    # is set to 1, which returns one set of stats per second. every_n=5 would return one
    # set of stats for every 5 seconds of the ride.
    try:
        workout_perf = s.get(f'{base_url}/api/workout/{workout_id}/performance_graph?every_n=1', timeout=10).json()
    except requests.exceptions.ReadTimeout:
        print("Pausing to reset rate limit")
        time.sleep(60)
        return

    ws_cols = ["seconds_since_pedaling_start", "output", "cadence", "resistance", "speed", "heart_rate"]

    metrics = {}
    retrieved_metrics = workout_perf["metrics"]

    for k in retrieved_metrics:
        metrics[k["slug"]] = k["values"]

    metrics["seconds_since_pedaling_start"] = workout_perf["seconds_since_pedaling_start"]
    for col in ws_cols:
        if col not in metrics:
            metrics[col] = []
    # The stats are returned in key/value pairs like {"cadence": 83}.
    # We cycle through the pairs, flattening them
    # if "metrics" in workout_perf:
    #     for m in workout_perf["metrics"]:
    #         metrics[m["slug"]] = m["values"]

    if "target_performance_metrics" in workout_perf:
        if "target_graph_metrics" in workout_perf["target_performance_metrics"]:
            for t in workout_perf["target_performance_metrics"]["target_graph_metrics"]:
                metrics[f'target_{t["type"]}_upper'] = t["graph_data"]["upper"]
                metrics[f'target_{t["type"]}_lower'] = t["graph_data"]["lower"]
    else:
        print(f"No target performance metrics for workout {workout_id}")

    # This adds an array to our workout performance stats indicating which workout the stats are for
    metrics["workout_id"] = [workout_id] * len(metrics["seconds_since_pedaling_start"])

    return metrics


def get_user_details(user_id):
    # Most of these columns aren't available for anyone other than the user who is logged in
    # but we try anyway.
    u_cols = ["id", "username", "cycling_workout_ftp", "image_url", "first_name", "last_name",
              "created_at", "birthday", "customized_max_heart_rate", "default_max_heart_rate"]

    # The /user endpoint returns data about the user themselves
    user = s.get(base_url + '/api/user/' + user_id).json()

    user_details = {k: user[k] for k in u_cols if k in user}

    return user_details


def get_instructors():

    instructor_metadata = s.get(f'{base_url}/api/instructor?limit=200', timeout=10).json()

    i_cols = ["id", "bio", "short_bio", "username", "quote", "first_name", "last_name",
              "instructor_hero_image_url"]

    instructors = []
    for i in instructor_metadata["data"]:
        instructors.append({k: i[k] for k in i_cols if k in i})

    upload_to_bq(instructors, "instructors", "overwrite")


def main():
    # Login to the Peloton API
    login = s.post(base_url + '/auth/login', json=payload)

    if login.status_code != 200:
        sys.exit("Your login to Peloton failed. Check your credentials and try again.")

    # Check that target tables exist and create any that don't
    create_tables()

    # Grab state from the database to understand what is already fetched
    workouts_already_fetched, rides_already_fetched = get_workouts_from_db()

    # Get the id of the user whose credentials we're using
    user_list = [s.get(base_url + '/api/me').json()['id']]
    # Get the ids of the users that user follows
    friends = s.get(base_url + '/api/user/' + user_list[0] + '/following').json()
    # Create a complete list of users we'll fetch stats for
    user_list = user_list + [f["id"] for f in friends["data"]]

    # Create a container for information about the users themselves
    user_detail_list = []
    for user in user_list:
        print(f'Retrieving workouts for {user} from Peloton')
        get_user_data(user, workouts_already_fetched, rides_already_fetched)
        # After fetching all of the user's workout data, we fetch data about the user themselves
        user_detail_list.append(get_user_details(user))
    # Some light, BigQuery-specific transformation
    transform_workout_stats()
    # If we have any user data, write it to the users table, overwriting all past data in that table
    if user_detail_list:
        upload_to_bq(user_detail_list, "users", "overwrite")

    get_instructors()


main()
