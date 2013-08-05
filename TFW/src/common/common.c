/****************************************************************************
 *                                                                          *
 *                                                                          *
 ****************************************************************************/

#include "_common.h"

/****************************************************************************
 * Initialises some data structures for internal usage.                     *
 ****************************************************************************/
void
init (void)
{
  if (bs_mmodInit (&iMObj) != SUCCESS)
    exit (0);
  if (bs_lmodInit (&iLObj, 0, 0, 0, NULL, iMObj) != SUCCESS)
    {
      bs_mmodFin (&iMObj);
      exit (0);
    }

  hdr ("Initializing..");
}

/****************************************************************************
 * Finalise data structures before exiting from the program.                *
 ****************************************************************************/
void
fin (void)
{
  hdr ("Finalizing..");

  blank ();

  bs_lmodFin (&iLObj, iMObj);
  bs_mmodFin (&iMObj);
}

/****************************************************************************
 * Halt the test case executions.                                           *
 ****************************************************************************/
static void
haltFun (void)
{
  err ("%s", "Aborting test case. Exiting ..");
  exit (0);
}

/****************************************************************************
 * Reset the test cases parameters for reuse.                               *
 ****************************************************************************/
void
resetTstParams (tstCaseParamCls * tstCase)
{
  tstCase->tstCaseDesc = NULL;
  tstCase->tstCond = 0;
  tstCase->tstRetVal = 0;
  tstCase->tstErrMsg = NULL;
  tstCase->tstFlags = 0;
}

/****************************************************************************
 * Execute the test case.                                                   *
 ****************************************************************************/
void
tstCaseExecute (tstCaseParamCls * tstCase)
{
  int cond;

  cond = tstCase->tstCond;

  if (cond > 0)
    {
      inf ("%s := %s", tstCase->tstCaseDesc, "Passed");
    }
  else
    {
      inf ("%s := %s", tstCase->tstCaseDesc, "Failed");
      res ("%d", tstCase->tstRetVal);
      if (tstCase->tstErrMsg)
        {
          err ("%s", tstCase->tstErrMsg);
        }
    }

  if (tstCase->tstFlags & HALT_ON_ERROR)
    {
      haltFun ();
    }
}

/****************************************************************************
 * Test case template.                                                      *
 ****************************************************************************/
void
EXEC_TSTCASE (tstCaseParamCls * tstcp, char *desc, int cond, int retval,
              char *errmsg, int flags)
{
  resetTstParams (tstcp);
  tstcp->tstCaseDesc = desc;
  tstcp->tstCond = cond;
  tstcp->tstRetVal = retval;
  tstcp->tstErrMsg = errmsg;
  tstcp->tstFlags = flags;
  tstCaseExecute (tstcp);
}

/****************************************************************************
 * Shell command execution function.                                        *
 ****************************************************************************/
void
EXEC_SH (tstCaseParamCls * tstcp, const char *cmd, char *desc, int flags)
{
  int retVal = -1;
  char errmsg[50];

  retVal = system (cmd);
  if (retVal == -1)
    {
      sprintf (errmsg, "Command execution failed: %s",
               ec2ES (errno2EC (errno)));
    }
  else if (WIFEXITED (retVal))
    {
      /*Get the return status of the command. */
      retVal = WEXITSTATUS (retVal);
      if (retVal != 0)
        sprintf (errmsg, "Command failed: %s", ec2ES (errno2EC (errno)));
    }
  else
    {
      sprintf (errmsg, "Command failed");
      retVal = -1;
    }

  EXEC_TSTCASE (tstcp, desc, (retVal == 0), retVal, errmsg, flags);
}

/****************************************************************************/
