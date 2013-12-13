/**
 * @file smod.c
 * Contains routines for signal handling.
 * @author RD
 * @date Sun Dec 19 22:15:59 IST 2010
 */

#include "_smod.h"

/**
 * The initializer function.
 * @return genErr_t
 * @param  sObjPtr
 * @param  mObj Memory object used in internal memory operations.
 */
genErr_t
bs_smodInit (bs_smodCls * sObjPtr, bs_mmodCls mObj)
{
  void *ptr = NULL;
  genErr_t retVal;

  if(sObjPtr == NULL)
    return INVALID_MEM_LOC;
  *sObjPtr = NULL;

  retVal = bs_allocMem (mObj, sizeof (struct bs_smodClsType), &ptr);
  if (retVal != SUCCESS)
    return retVal;

  (*sObjPtr) = (bs_smodCls) ptr;

  (*sObjPtr)->_validFlag = true;

  return SUCCESS;
}

/**
 * The finalizer destroys the signal object.
 * @return genErr_t
 * @param  sObjPtr
 * @param  mObj Memory object used in internal memory operations.
 */
genErr_t
bs_smodFin (bs_smodCls * sObjPtr, bs_mmodCls mObj)
{
  validateObj (*sObjPtr);

  genErr_t retVal;

  (*sObjPtr)->_validFlag = false;

  retVal = bs_freeMem (mObj, (void *) sObjPtr);
  if (retVal != SUCCESS)
    return retVal;

  return SUCCESS;
}

#ifdef SIG_USER_DATA_CHGS
/**
 * Internal handler. This handler will be used for all the signals.
 * On receipt of a signal the handler is called which uses the signal
 * number to retrieve the registered user handler.
 * This function will be passed a signal number as the argument.
 * -->As part of the real time extensions the signal object will be
 * passed as the userdata for this handler.
 * The user handler function is passed the userdata (that is registered
 * as part of the function registration) when it is invoked.
 * The indent of this function is to have a clean interface for signal
 * handling and assist in diagnostics.
 * @return void
 * @param  signum
 * @param  userData
 */
PRIVATE void
bs_sigHandler (int sigNum, void *userData)
{
  //Pass the signal object as the userdata to this handler. Pass this signal
  //object to the user registered handler.
  //Use the signal number and invoke the user registered signal handler.
  //Currently unsed.
  (void) sigNum;
  sobj = (bs_smodCls) userData;

  if(sobj == NULL)
    assert(0);

  //refer the signal number and get the handler and the userdata.
  sobj->bs_userSignalHandlerType sigHndlr (sigNum, sobj, sobj->userData);
}
#endif

/**
 * Internal signal handler registration function.
 * @return genErr_t
 * @param  sigNum
 * @param  sObj
 */
PRIVATE genErr_t
bs_sigHndlrReg (int sigNum, bs_smodCls sObj)
{
  genErr_t retVal = SUCCESS;
  int status;
  struct sigaction initalAct;

#ifdef SIG_USER_DATA_CHGS
  /*Add the userhandler for the signal along with the user data. */
  //Update the handler and the userdata for the signal number.
  initalAct.sa_handler = bs_sigHandler;
#else
  initalAct.sa_handler = sObj->sigHndlr;
#endif

  initalAct.sa_flags = 0;

  sigemptyset (&initalAct.sa_mask);

  status = sigaction (sigNum, &initalAct, 0);
  if (status == -1)
    retVal = errno2EC (errno);

  return retVal;
}

/**
 * The function registers the user handler(action) with the specified
 * signal number.
 * Currently -> Donot set mask for any signal. Also no provision to
 * specify flags.
 * Currently -> No storage of previous signal state.
 * @return genErr_t
 * @param  sObj
 * @param  sigNum the signal number for which the handler needs to be
 * registered.
 * @param  sigHndlr The handler for the signal number.
 * @param  sigHndlr The handler for the signal number.
 */
genErr_t
bs_registerHandler (bs_smodCls sObj, int sigNum,
                    bs_userSignalHandlerType sigHndlr, void *userData)
{
  genErr_t retVal = SUCCESS;

  if(sObj == NULL)
    return INVALID_MEM_LOC;

  sObj->userData = userData;
  sObj->sigHndlr = sigHndlr;

  retVal = bs_sigHndlrReg (sigNum, sObj);

  return retVal;
}
