package eflow.workflow.domain

import slick.driver.H2Driver.api._
import slick.lifted.Tag

class WfAction(tag: Tag) extends Table[(Long, Long, Int, Int, Int, Int, Float, Int, Int, String, Double, String)](tag, "WF_ACTIONS") {

  // This is the primary key column:
  def actionId: Rep[Long] = column[Long]("ACTION_ID", O.PrimaryKey)
  def valueId: Rep[Long] = column[Long]("VALUE_ID")
  def actionTypeId: Rep[Int] = column[Int]("ACTION_TYPE_ID")
  def targetId: Rep[Int] = column[Int]("TARGET_ID")
  def targetTypeId: Rep[Int] = column[Int]("TARGET_TYPE_ID")
  def motionTypeId: Rep[Int] = column[Int]("MOTION_TYPE_ID")
  def motionOrder: Rep[Float] = column[Float]("MOTION_ORDER")
  def direction: Rep[Int] = column[Int]("HR_DIRECTION")
  def level: Rep[Int] = column[Int]("HR_LEVEL")
  def name: Rep[String] = column[String]("NAME")
  def flowOrder: Rep[Double] = column[Double]("FLOW_ORDER")
  def note: Rep[String] = column[String]("NOTE")
}