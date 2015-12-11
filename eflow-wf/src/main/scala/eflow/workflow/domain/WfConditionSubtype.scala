package eflow.workflow.domain

import slick.driver.H2Driver.api._
import slick.lifted.Tag

class WfConditionSubtype(tag: Tag) extends Table[(Int, Int, Long)](tag, "WF_CONDITION_SUBTYPES") {

    // This is the primary key column:
  def conditionSubtypeId: Rep[Int] = column[Int]("CONDITION_SUBTYPE_ID", O.PrimaryKey)
  def subtypeId: Rep[Int] = column[Int]("SUBTYPE_ID")
  def conditionId: Rep[Long] = column[Long]("CONDITION_ID")
}