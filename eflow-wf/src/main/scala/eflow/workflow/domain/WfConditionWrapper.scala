package eflow.workflow.domain

import slick.driver.H2Driver.api._
import slick.lifted.Tag

class WfConditionWrapper(tag: Tag) extends Table[(Long, String, Int, String, Int, Int, Int, Int, Int, Double, String)](tag, "WF_CONDITIONS") {

  // This is the primary key column:
  def conditionId: Rep[Long] = column[Long]("CONDITION_ID", O.PrimaryKey, O.AutoInc)
  def fieldName: Rep[String] = column[String]("FIELD_NAME")
  def documentSubtypeId: Rep[Int] = column[Int]("DOCUMENT_SUBTYPE_ID")
  def name: Rep[String] = column[String]("NAME")
  def allValues: Rep[Int] = column[Int]("ALL_VALUES")
  def conditionType: Rep[Int] = column[Int]("CONDITION_TYPE")
  def scriptCondition: Rep[Int] = column[Int]("SCRIPT_CONDITION")
  def targetCondition: Rep[Int] = column[Int]("TARGET_CONDITION")
  def multiTarget: Rep[Int] = column[Int]("MULTI_TARGET")
  def flowOrder: Rep[Double] = column[Double]("FLOW_ORDER")
  def script: Rep[String] = column[String]("SCRIPT")
}