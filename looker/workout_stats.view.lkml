# The name of this view in Looker is "Workout Stats"
view: workout_stats {
  # The sql_table_name parameter indicates the underlying database table
  # to be used for all fields in this view.
  sql_table_name: `peloton.workout_stats`
    ;;

  # This primary key is the unique key for this table in the underlying database.
  # You need to define a primary key in a view in order to join to other views.

  dimension: id_x_time{
    type: string
    sql: CONCAT(${workouts.id}, CAST(${pk2_time} as STRING)) ;;
    primary_key: yes
    hidden: yes
  }

  dimension: cadence {
    type: number
    sql: ${TABLE}.avg_cadence_2s ;;
    description: "This is the average cadence across the last 3 seconds."
  }

  # If you'd prefer to use the 3-second average cadence, change the above to avg_cadence_3s.
  # If you'd prefer to use the instant cadence, change the above to cadence.


  measure: total_strokes {
    type: sum
    sql: ${cadence}/60 ;;
  }

  measure: average_cadence {
    type: average
    sql: ${cadence} ;;
  }

  dimension: heart_rate {
    type: number
    sql: ${TABLE}.heart_rate ;;
  }

  dimension: output {
    type: number
    sql: ${TABLE}.output ;;
  }

  measure: total_output {
    type: sum
    sql: ${output} ;;
    value_format: "0,\" kj\""
  }

  measure: avg_output {
    type: average
    sql: ${output} ;;
    value_format: "0\" W\""
  }

  dimension: resistance {
    type: number
    sql: ${TABLE}.resistance ;;
  }


  measure: avg_resistance {
    type: average
    sql: ${resistance} ;;
  }

  dimension: speed {
    type: number
    sql: ${TABLE}.speed ;;
  }

  measure: avg_speed {
    type: average
    sql: ${speed} ;;
    value_format: "0\" mph\""
  }

  dimension: pk2_time {
    type: number
    sql: ${TABLE}.seconds_since_pedaling_start ;;
    label: "Seconds since start"
  }

  dimension: minutes_since_pedaling_start {
    type: number
    sql: ${pk2_time}/60 ;;
    value_format_name: decimal_2
  }

  measure: count_seconds {
    type: count
    description: "The count of seconds in the dataset"
  }

}
