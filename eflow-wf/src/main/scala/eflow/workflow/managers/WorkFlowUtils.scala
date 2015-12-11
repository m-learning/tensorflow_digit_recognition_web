package eflow.workflow.managers

import eflow.workflow.domain.WfConditionWrapper
import slick.driver.H2Driver.api._
import eflow.workflow.domain.WfParameter
import eflow.workflow.domain.WfValue

/**
 * Utility class to work with flow manager
 */
class WorkFlowUtils {

  def getConditions(conditionId: Long) = {
    
    val conditions = TableQuery[WfConditionWrapper];
    val values = TableQuery[WfValue]
    val parameters = TableQuery[WfParameter]
    val condition = conditions.filter(c => _.conditionId === conditionId).headOption
    
    val acts = values.filter( c => _.conditionId === conditionId)
  }
}