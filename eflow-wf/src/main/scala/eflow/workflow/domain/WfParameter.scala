package eflow.workflow.domain

import slick.driver.H2Driver.api._
import slick.lifted.Tag

class WfParameter(tag: Tag) extends Table[(Long, String, Long)](tag, "WF_CONDITION_SUBTYPES") {

  // This is the primary key column:
  def parameterId: Rep[Long] = column[Long]("PARAMETER_ID", O.PrimaryKey)
  def value: Rep[String] = column[String]("PARAMETER_VALUE")
  def conditionId: Rep[Long] = column[Long]("CONDITION_ID")
}