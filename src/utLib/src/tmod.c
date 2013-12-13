/**
 * @file tmod.c
 * Contains routines for timer handling.
 * @author RD
 * @date Sun Dec 26 19:25:02 IST 2010
 */

#include "_tmod.h"
#include "_tsmod.h"

/**
 * The initializer function.
 * @return genErr_t
 * @param  tObjPtr
 * @param  mObj Memory object used in internal memory operations.
 */
genErr_t
bs_tmodInit (bs_tmodCls * tObjPtr, bs_mmodCls mObj)
{
  void *ptr = NULL;
  genErr_t retVal;

  if(tObjPtr == NULL)
    return INVALID_MEM_LOC;
  *tObjPtr = NULL;

  retVal = bs_allocMem (mObj, sizeof (struct bs_tmodClsType), &ptr);
  if (retVal != SUCCESS)
    return retVal;

  (*tObjPtr) = (bs_tmodCls) ptr;

  (*tObjPtr)->_validFlag = true;

  return SUCCESS;
}

/**
 * The finalizer destroys the object.
 * @return genErr_t
 * @param tObjPtr
 * @note error code due to failure in setitimer is ignored currently.
 * @param mObj Memory object.
 */
genErr_t
bs_tmodFin (bs_tmodCls * tObjPtr, bs_mmodCls mObj)
{
  genErr_t retVal;

  int status = 0;
  struct itimerval timerVal;

  validateObj (*tObjPtr);

  SET_ZERO(timerVal);

  status = setitimer (ITIMER_REAL, &timerVal, 0);
  if (status == -1)
    retVal = errno2EC (errno);

  (*tObjPtr)->_validFlag = false;

  retVal = bs_freeMem (mObj, (void *) tObjPtr);
  if (retVal != SUCCESS)
    return retVal;

  return SUCCESS;
}

#ifdef SIG_USER_DATA_CHGS
/**
 * Internal timer context. This will be registered as the timer handler.
 * The function calls the registered user handler. This also passes the
 * userdata to the handler.
 * @return void
 * @param  signum
 * @param  userData Userdata will contain timer object reference.
 */
PRIVATE void
bs_timerCntxt (int signum, void *userData)
{
  (void) signum;
  //tmod=(bs_tmodCls)userData;
  //tmod->(bs_timerHandlerType)tmrHndlr(tmod, tmod->userData);
}
#endif

/**
 * The function registers a user specified handler with a timer interval.
 * The time interval is specified in resolution of micro seconds.
 * @return genErar_t
 * @param tObj
 * @param usec Timer value in micro seconds.
 * @param tmrHndlr Timer handler function that will be invoked on the
 * expiration of the timer
 * @param userData User specified data that will be passed to the handler on
 * expiration of the timer.
 */
genErr_t
bs_registerTimerHandler (bs_tmodCls tObj, int usec,
                         bs_timerHandlerType tmrHndlr, void *userData)
{
  genErr_t retVal = SUCCESS;
  int status = 0;
  struct itimerval timerVal;

  if(tObj == NULL)
    return INVALID_MEM_LOC;

  tObj->userData = userData;
  tObj->tmrHndlr = tmrHndlr;

  //Set both the initial and the period timers to the usec value.
  timerVal.it_interval.tv_usec = usec;
  timerVal.it_value.tv_usec = usec;
  timerVal.it_interval.tv_sec = 0;
  timerVal.it_value.tv_sec = 0;

  status = setitimer (ITIMER_REAL, &timerVal, 0);
  if (status == -1)
    retVal = errno2EC (errno);

#ifdef SIG_USER_DATA_CHGS
  retVal = bs_tmrSigHndlrReg (bs_timerCntxt, tObj);
#else
  retVal = bs_tmrSigHndlrReg (tmrHndlr, tObj);
#endif

  if (status == -1)
    retVal = errno2EC (errno);

  return retVal;
}
