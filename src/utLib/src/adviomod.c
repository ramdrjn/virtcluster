/**
 * @file adviomod.c
 * Contains advanced io routines.
 * @author RD
 * @date Sun Jun  9 20:41:53 IST 2013
 */

#include "_adviomod.h"

/**
 * Init memory for advanced IO object.
 * @param advioPtr ADV IO object pointer.
 * @param mObj memory object that will be used for allocations.
 * @return SUCCESS or other error codes incase of failure.
 */
genErr_t
bs_advioInit (bs_advioCls *advioPtr, bs_mmodCls mObj, t_bool poll)
{
  void *ptr = NULL;
  genErr_t retVal;

  if(advioPtr == NULL)
    return INVALID_MEM_LOC;
  *advioPtr = NULL;

  retVal = bs_allocMem (mObj, sizeof (struct bs_advioClsType), &ptr);
  if (retVal != SUCCESS)
    return retVal;

  *advioPtr = (bs_advioCls) ptr;

  (*advioPtr)->_validFlag = true;
  (*advioPtr)->_pollFD = -1;

  if(true == poll)
    {
      int rc;

      rc = epoll_create1(0);
      if (rc == -1)
        {
          retVal = bs_advioFin (advioPtr, mObj);
          return errno2EC (rc);
        }

      (*advioPtr)->_pollFD = rc;
    }

  return SUCCESS;
}

/**
 * Finalize memory for object.
 * @param advioPtr ADV iO object pointer.
 * @param mObj that will be used for memory operations.
 * @return SUCCESS or other error codes incase of failure.
 */
genErr_t
bs_advioFin (bs_advioCls *advioPtr, bs_mmodCls mObj)
{
  genErr_t retVal;

  validateObj (*advioPtr);

  (*advioPtr)->_validFlag = false;

  if((*advioPtr)->_pollFD != -1)
    {
      int rc;

      rc = close((*advioPtr)->_pollFD);
      if (rc == -1)
        retVal = errno2EC (rc);
    }

  retVal = bs_freeMem (mObj, (void *) advioPtr);
  if (retVal != SUCCESS)
    return retVal;

  return SUCCESS;
}

/**
 * Add fObj to the poll list.
 * @param advioPtr advio object
 * @param fObj The file in the object will be polled.
 * @param udPtr User passed data that will be returned in epoll_wait
 * @param events The events described for poll.
 * @return Success on registration or the error code.
 */
genErr_t
bs_pollAdd (bs_advioCls advioPtr, bs_fmodCls fObj,
            void *udPtr, t_uint32 events)
{
  int rc, fd;
  struct epoll_event event;

  validateObj (advioPtr);

  if(fObj == NULL)
    return INVALID_MEM_LOC;

  fd = bs_getFD(fObj);
  if(fd == -1)
    return INVALID_OBJ;

  event.data.ptr = udPtr;
  event.events = events;

  rc = epoll_ctl(advioPtr->_pollFD, EPOLL_CTL_ADD, fd, &event);
  if (rc == -1)
    return errno2EC (rc);

  return SUCCESS;
}

/**
 * Remove fObj to the poll list.
 * @param advioPtr advio object
 * @param fObj The file in the object will be remoed from the poll list
 * @param udPtr User passed data that will be returned in epoll_wait
 * @param events The events described for poll.
 * @return Success on de-registration or the error code.
 */
genErr_t
bs_pollRem (bs_advioCls advioPtr, bs_fmodCls fObj,
            void *udPtr, t_uint32 events)
{
  int rc, fd;
  struct epoll_event event;

  validateObj (advioPtr);

  if(fObj == NULL)
    return INVALID_MEM_LOC;

  fd = bs_getFD(fObj);
  if(fd == -1)
    return INVALID_OBJ;

  event.data.ptr = udPtr;
  event.events = events;

  rc = epoll_ctl(advioPtr->_pollFD, EPOLL_CTL_DEL, fd, &event);
  if (rc == -1)
    return errno2EC (rc);

  return SUCCESS;
}

/**
 * Modified events for fObj in the poll list.
 * @param advioPtr advio object
 * @param fObj The events for the file in the object will be modified
 * @param udPtr User passed data that will be returned in epoll_wait
 * @param events The events described for poll.
 * @return Success on de-registration or the error code.
 */
genErr_t
bs_pollMod (bs_advioCls advioPtr, bs_fmodCls fObj,
            void *udPtr, t_uint32 events)
{
  int rc, fd;
  struct epoll_event event;

  validateObj (advioPtr);

  if(fObj == NULL)
    return INVALID_MEM_LOC;

  fd = bs_getFD(fObj);
  if(fd == -1)
    return INVALID_OBJ;

  event.data.ptr = udPtr;
  event.events = events;

  rc = epoll_ctl(advioPtr->_pollFD, EPOLL_CTL_MOD, fd, &event);
  if (rc == -1)
    return errno2EC (rc);

  return SUCCESS;
}

/**
 * Poll
 * @param advioPtr advio object
 * @param count The number of events are returned here.
 * @param events The events structure that is populated by epoll_wait
 * @param maxevents The maximum number of events to wait for.
 * @param timeout The timeout beyond which epoll will return on no events.
 * The value is in milliseconds.
 * @return SUCCESS or error code on failure/timeout.
 */
genErr_t
bs_poll (bs_advioCls advioPtr, int *count,
         struct epoll_event *events, int maxevents, int timeout)
{
  int rc;

  validateObj (advioPtr);

  rc = epoll_wait(advioPtr->_pollFD, events, maxevents, timeout);
  *count = rc;

  if(rc == -1)
    return errno2EC (rc);
  else if (rc == 0)
    return TIMEOUT;

  return SUCCESS;
}

/****************************************************************************/
