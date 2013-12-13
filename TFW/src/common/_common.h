#ifndef _COMMON_H_
#define _COMMON_H_
/****************************************************************************
 * 									    *
 *									    *
 ****************************************************************************/

#include "main.h"

bs_mmodCls iMObj;
bs_lmodCls iLObj;
tstCaseParamCls tstCase;
int retVal;

struct tstCaseParamClsType
{
  char *tstCaseDesc;
  char tstCond;
  int tstRetVal;
  char *tstErrMsg;
  char tstFlags;
};

void resetTstParams (tstCaseParamCls * tstCase);
void tstCaseExecute (tstCaseParamCls * tstCase);

/****************************************************************************/
#endif /*_COMMON_H_*/
