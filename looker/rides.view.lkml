# The name of this view in Looker is "Rides"
view: rides {
  # The sql_table_name parameter indicates the underlying database table
  # to be used for all fields in this view.
  sql_table_name: `peloton.rides`
    ;;
  drill_fields: [id]
  # This primary key is the unique key for this table in the underlying database.
  # You need to define a primary key in a view in order to join to other views.

  dimension: id {
    primary_key: yes
    type: string
    sql: ${TABLE}.id ;;
  }

  # Here's what a typical dimension looks like in LookML.
  # A dimension is a groupable field that can be used to filter query results.
  # This dimension will be called "Description" in Explore.

  dimension: description {
    type: string
    sql: ${TABLE}.description ;;
  }

  dimension: difficulty_estimate {
    type: number
    sql: ${TABLE}.difficulty_estimate ;;
  }

  dimension: duration {
    type: number
    sql: ${TABLE}.duration/60 ;;
    value_format_name: decimal_0
  }


  # A measure is a field that uses a SQL aggregate function. Here are defined sum and average
  # measures for this dimension, but you can also add measures of many different aggregates.
  # Click on the type parameter to see all the options in the Quick Help panel on the right.

  measure: total_duration {
    type: sum
    sql: ${duration} ;;
  }

  measure: average_duration {
    type: average
    sql: ${duration} ;;
  }

  dimension: fitness_discipline {
    type: string
    sql: ${TABLE}.fitness_discipline ;;
  }

  dimension: image_url {
    type: string
    sql: ${TABLE}.image_url ;;
  }

  dimension: instructor_id {
    type: string
    sql: ${TABLE}.instructor_id ;;
  }

  dimension: language {
    type: string
    sql: ${TABLE}.language ;;
  }

  dimension: original_air_time {
    type: number
    sql: ${TABLE}.original_air_time ;;
  }

  dimension: overall_estimate {
    type: number
    sql: ${TABLE}.overall_estimate ;;
  }

  dimension: overall_rating_avg {
    type: number
    sql: ${TABLE}.overall_rating_avg ;;
  }

  dimension: overall_rating_count {
    type: number
    sql: ${TABLE}.overall_rating_count ;;
  }

  dimension: series_id {
    type: string
    sql: ${TABLE}.series_id ;;
  }

  dimension: title {
    type: string
    sql: ${TABLE}.title ;;
  }

  measure: count {
    type: count
    drill_fields: [id, workouts.count]
  }
}
