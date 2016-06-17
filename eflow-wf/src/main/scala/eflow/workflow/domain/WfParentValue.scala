package eflow.workflow.domain

import slick.driver.H2Driver.api._
import slick.lifted.Tag

class WfParentValue(tag: Tag) extends Table[(Int, Int, Int, Int, Int, Int, Int)](tag, "WF_CONDITION_SUBTYPES") {

  // This is the primary key column:
  def parentValidator: Rep[Int] = column[Int]("PARENT_VALIDATOR", O.PrimaryKey)
  def senderOrganization: Rep[Int] = column[Int]("SENDER_ORGANIZARION")
  def oneOf: Rep[Int] = column[Int]("ONE_OF")
  def senderType: Rep[Int] = column[Int]("SENDER_TYPE")
  def directed: Rep[Int] = column[Int]("DIRECTED")
  def level: Rep[Int] = column[Int]("LEVEL")
  def direction: Rep[Int] = column[Int]("DIRECTION")
}