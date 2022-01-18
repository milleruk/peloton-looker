# The name of this view in Looker is "Users"
view: users {
  # The sql_table_name parameter indicates the underlying database table
  # to be used for all fields in this view.
  sql_table_name: `peloton.users`
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
  # This dimension will be called "Birthday" in Explore.

  dimension: birthday {
    type: number
    sql: ${TABLE}.birthday ;;
  }

  # A measure is a field that uses a SQL aggregate function. Here are defined sum and average
  # measures for this dimension, but you can also add measures of many different aggregates.
  # Click on the type parameter to see all the options in the Quick Help panel on the right.

  measure: total_birthday {
    type: sum
    sql: ${birthday} ;;
  }

  measure: average_birthday {
    type: average
    sql: ${birthday} ;;
  }

  dimension: created_at {
    type: number
    sql: ${TABLE}.created_at ;;
  }

  dimension: cycling_workout_ftp {
    type: number
    sql: ${TABLE}.cycling_workout_ftp ;;
  }

  dimension: first_name {
    type: string
    sql: ${TABLE}.first_name ;;
  }

  dimension: image_url {
    type: string
    sql: ${TABLE}.image_url ;;
  }

  dimension: last_name {
    type: string
    sql: ${TABLE}.last_name ;;
  }

  dimension: username {
    type: string
    sql: ${TABLE}.username ;;
  }

  measure: count {
    type: count
    drill_fields: [id, last_name, first_name, username, workouts.count]
  }
}
