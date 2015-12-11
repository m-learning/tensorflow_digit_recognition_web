package eflow.workflow.domain

import slick.driver.H2Driver.api._
import slick.lifted.Tag

class WfCondition(tag: Tag) extends Table[(Long, Int, Int, String, String, Int, Int, Int, String, Double)](tag, "WF_CONDITIONS") {

  // This is the primary key column:
  def conditionId: Rep[Long] = column[Long]("CONDITION_ID", O.PrimaryKey)
  def documentSubtypeId: Rep[Int] = column[Int]("DOCUMENT_SUBTYPE_ID")
  def conditionTypeId: Rep[Int] = column[Int]("CONDITION_TYPE_ID")
  def name: Rep[String] = column[String]("NAME")
  def script: Rep[String] = column[String]("SCRIPT")
  def scriptCondition: Rep[Int] = column[Int]("SCRIPT_CONDITION")
  def targetCondition: Rep[Int] = column[Int]("TARGET_CONDITION")
  def multiTarget: Rep[Int] = column[Int]("MULTI_TARGET")
  def note: Rep[String] = column[String]("NOTE")
  def flowOrder: Rep[Double] = column[Double]("FLOW_ORDER")
}