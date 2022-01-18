# The name of this view in Looker is "Workouts"
view: workouts {
  # The sql_table_name parameter indicates the underlying database table
  # to be used for all fields in this view.
  sql_table_name: `peloton.workouts_with_stats`
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
  # This dimension will be called "Created At" in Explore.

  dimension_group: created {
    type: time
    sql: ${TABLE}.created_ts;;
    timeframes: [time, date, week, month]
    datatype: timestamp
  }

  # A measure is a field that uses a SQL aggregate function. Here are defined sum and average
  # measures for this dimension, but you can also add measures of many different aggregates.
  # Click on the type parameter to see all the options in the Quick Help panel on the right.


  dimension: ftp {
    type: number
    sql: ${TABLE}.ftp ;;
  }

  dimension: is_total_work_personal_record {
    type: yesno
    sql: ${TABLE}.is_total_work_personal_record ;;
  }

  dimension: leaderboard_rank {
    type: number
    sql: ${TABLE}.leaderboard_rank ;;
  }

  dimension: ride_id {
    type: string
    # hidden: yes
    sql: ${TABLE}.ride_id ;;
  }

  dimension_group: start_time {
    sql: ${TABLE}.start_ts ;;
    type: time
    timeframes: [time, date, week, month]
    datatype: timestamp
  }

  dimension: status {
    type: string
    sql: ${TABLE}.status ;;
  }

  dimension: total_work {
    type: number
    sql: ${TABLE}.total_work ;;
  }

  dimension: user_id {
    type: string
    # hidden: yes
    sql: ${TABLE}.user_id ;;
  }

  dimension: v2_total_video_watch_time_seconds {
    type: number
    sql: ${TABLE}.v2_total_video_watch_time_seconds ;;
  }

  measure: count {
    type: count_distinct
    sql: ${id} ;;
    drill_fields: [detail*]
  }

  # ----- Sets of fields for drilling ------
  set: detail {
    fields: [
      id,
      rides.id,
      users.last_name,
      users.id,
      users.first_name,
      users.username
    ]
  }
}
