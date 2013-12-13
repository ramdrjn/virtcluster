/**
 * @file _tsmod.c
 * Contains routines for timer handling based on signals.
 * @author RD
 * @date Sat Jan  1 00:42:20 IST 2011
 */

#include "_tsmod.h"

/**
 * Internal registration function for timer based on SIGALRM implementation.
 * @return genErr_t
 * @param  tmrHndlr
 * @param  tObj
 */
genErr_t
bs_tmrSigHndlrReg (bs_timerSignalHandlerType tmrHndlr, bs_tmodCls tObj)
{
  genErr_t retVal = SUCCESS;
  int status;
  struct sigaction initalAct;

  //Unused until support for userData.
  (void) tObj;

  initalAct.sa_handler = tmrHndlr;
  initalAct.sa_flags = 0;
  sigemptyset (&initalAct.sa_mask);

  status = sigaction (SIGALRM, &initalAct, 0);
  if (status == -1)
    retVal = errno2EC (errno);
  return retVal;
}
