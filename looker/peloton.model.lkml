# TODO: Define the database connection to be used for this model.
connection: "your-connection-name"

# include all the views
include: "/views/**/*.view"

datagroup: peloton_default_datagroup {
  # sql_trigger: SELECT MAX(id) FROM etl_log;;
  max_cache_age: "1 hour"
}

persist_with: peloton_default_datagroup

explore: workouts {
  join: rides {
    type: left_outer
    sql_on: ${workouts.ride_id} = ${rides.id} ;;
    relationship: many_to_one
  }
  join: instructors {
    sql_on: ${rides.instructor_id} = ${instructors.id} ;;
    relationship: many_to_one
  }
  join: users {
    type: left_outer
    sql_on: ${workouts.user_id} = ${users.id} ;;
    relationship: many_to_one
  }
  join: workout_stats {
    type: left_outer
    sql: LEFT JOIN UNNEST(workouts.stats) as workout_stats;;
    relationship: one_to_many
  }
}
