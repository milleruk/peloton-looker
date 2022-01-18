# The name of this view in Looker is "Instructors"
view: instructors {
  # The sql_table_name parameter indicates the underlying database table
  # to be used for all fields in this view.
  sql_table_name: `solar-1433.peloton.instructors`
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
  # This dimension will be called "Bio" in Explore.

  dimension: bio {
    type: string
    sql: ${TABLE}.bio ;;
  }

  dimension: first_name {
    type: string
    sql: ${TABLE}.first_name ;;
  }

  dimension: instructor_hero_image_url {
    type: string
    sql: ${TABLE}.instructor_hero_image_url ;;
  }

  dimension: last_name {
    type: string
    sql: ${TABLE}.last_name ;;
  }

  dimension: quote {
    type: string
    sql: ${TABLE}.quote ;;
  }

  dimension: short_bio {
    type: string
    sql: ${TABLE}.short_bio ;;
  }

  dimension: username {
    type: string
    sql: ${TABLE}.username ;;
  }

  measure: count {
    type: count
    drill_fields: [id, last_name, first_name, username]
  }
}
