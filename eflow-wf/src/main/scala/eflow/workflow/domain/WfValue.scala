package eflow.workflow.domain

import slick.driver.H2Driver.api._
import slick.lifted.Tag

class WfValue(tag: Tag) extends Table[(Long, Long, String, String)](tag, "WF_VALUES")  {
  
      // This is the primary key column:
  def valueId: Rep[Long] = column[Long]("VALUE_ID", O.PrimaryKey)
  def conditionId: Rep[Long] = column[Long]("CONDITION_ID")
  def name: Rep[String] = column[String]("CONDITION_NAME")
  def value: Rep[String] = column[String]("CONDITION_VALUE")
}