/**
 * @file lmod.c
 * Contains log routines.
 * @author RD
 * @date Mon Jan 26 20:06:57 EET 2009
 */

#include "_lmod.h"

/**
 * Init Allocates memory for the object based on the memory object.
 * During init, specify syslog requirement. Also specify the verbosity
 * requirements for the log. Additionally the file object for the log file
 * can also be specified.
 * @param lObjPtr Reference where the newly allocated log object will be
 * stored.
 * @param syslog Flag to indicate syslog logging will be enabled or not.
 * @param quite Flag to stop logging dynamically.
 * @param verbose Verbosity level for the log.
 * @param fileObj File object that will used for the log file.
 * @param mObj Reference of the memory object that will be used in the
 * memory allocation. If memory is not available then the appropriate
 * \c error-code is returned.
 * @return The \c error-code if any error during allocation of memory else
 * success is returned.
 */
genErr_t
bs_lmodInit (bs_lmodCls * lObjPtr, int syslog, int quite, int verbose,
             bs_fmodCls fileObj, bs_mmodCls mObj)
{
  void *ptr = NULL;
  genErr_t retVal;

  if(lObjPtr == NULL)
    return INVALID_MEM_LOC;
  *lObjPtr = NULL;

  retVal = bs_allocMem (mObj, sizeof (struct bs_lmodClsType), &ptr);
  if (retVal != SUCCESS)
    return retVal;
  (*lObjPtr) = (bs_lmodCls) ptr;

  (*lObjPtr)->_validFlag = true;
  (*lObjPtr)->_syslogFlag = syslog;
  (*lObjPtr)->_quiteFlag = quite;
  (*lObjPtr)->_verboseFlag = verbose;
  (*lObjPtr)->_filePtr = fileObj;
  SET_ZERO ((*lObjPtr)->_buffer);

  return SUCCESS;
}

/**
 * Finalize the object. Application needs to close the file ptr.
 * Memory will be freed for the object inside this.
 * @param lObjPtr Reference of the log object.
 * @param mObj Reference of the memory object that will be used for the memory
 * operations.
 * @return The \c error-code if any error during memory operations else
 * success is returned.
 */
genErr_t
bs_lmodFin (bs_lmodCls * lObjPtr, bs_mmodCls mObj)
{
  validateObj (*lObjPtr);

  genErr_t retVal;

  (*lObjPtr)->_validFlag = false;

  retVal = bs_freeMem (mObj, (void *) lObjPtr);
  if (retVal != SUCCESS)
    return retVal;

  return SUCCESS;
}

/**
 * Set the verbose mode of the log object.
 * @param lObj log object whose verbose level needs to be altered.
 * @return None.
 */
void
bs_setVerbose (bs_lmodCls lObj)
{
  validateObj (lObj);

  lObj->_verboseFlag = true;
}

/**
 * UnSet the verbose mode of the log object.
 * @param lObj log object whose verbose level needs to be altered.
 * @return None.
 */
void
bs_unsetVerbose (bs_lmodCls lObj)
{
  validateObj (lObj);

  lObj->_verboseFlag = false;
}

/**
 * Set the quite mode of the log object.
 * @param lObj log object whose quite level needs to be altered.
 * @return None.
 */
void
bs_setQuite (bs_lmodCls lObj)
{
  validateObj (lObj);

  lObj->_quiteFlag = true;
}

/**
 * UnSet the quite mode of the log object.
 * @param lObj log object whose quite level needs to be altered.
 * @return None.
 */
void
bs_unsetQuite (bs_lmodCls lObj)
{
  validateObj (lObj);

  lObj->_quiteFlag = false;
}

/**
 * Internal function to report the log level and status of the log object.
 * @param lObj log object.
 * @param logLevel the log level for the message.
 * @return None.
 */
PRIVATE inline t_bool
_checkLogLevel (bs_lmodCls lObj, bs_e_logLvl logLevel)
{
  t_bool printMsg;

  //No print if the quite flag is set.
  printMsg = (lObj->_quiteFlag == true) ? false : true;

  switch (logLevel)
    {
    case LVL_ERROR:
      {
        printMsg = true;
        break;
      }
    case LVL_INFO:
      {
        if ((!printMsg) && (lObj->_verboseFlag == true))
          printMsg = true;
        break;
      }
    case LVL_DEBUG:
      {
        printMsg = (lObj->_verboseFlag == true) ? true : false;
        break;
      }
    default:
      printMsg = false;
    }

  return printMsg;
}

/**
 * Map the library log levels with that of the syslog.
 * @param logLevel the log level for the message.
 * @return Retuns the log level of syslog.
 */
PRIVATE inline int
_retSyslogLvl (bs_e_logLvl logLevel)
{
  if (logLevel == LVL_ERROR)
    return LOG_ERR;
  else if (logLevel == LVL_INFO)
    return LOG_INFO;

  return LOG_DEBUG;
}

/**
 * Internal log function that actually logs the message.
 * @param lObj The log object.
 * @param logLevel the log level for the message.
 * @param mode The mode specifies whether to only print or log the message.
 * @return None
 */
PRIVATE inline void
_log (bs_lmodCls lObj, bs_e_logLvl logLevel, bs_e_logMode mode)
{
  if (mode != FO_LOG)
    {
      if (logLevel == LVL_ERROR)
        fprintf (stderr, "%s", lObj->_buffer);
      else
        fprintf (stdout, "%s", lObj->_buffer);
    }

  if ((mode == PF_LOG) || (mode == FO_LOG))
    {
      int cnt;
      if (lObj->_syslogFlag)
        syslog (_retSyslogLvl (logLevel), "%s", lObj->_buffer);
      if (lObj->_filePtr)
        bs_fWrite (lObj->_filePtr, lObj->_buffer, LOG_BUFFER_SIZE, &cnt);
    }
}

/**
 * Log the message.
 * @param lObj The log object.
 * @param lvl the log level for the message.
 * @param mode The mode specifies whether to only print or log the message.
 * @param fmt Format for the variable arguments. This is followed by the
 * variable arguments.
 * @return None
 */
void
bs_log (bs_lmodCls lObj, bs_e_logLvl lvl, bs_e_logMode mode,
        const char *fmt, ...)
{
  validateObj (lObj);

  va_list arguments;

  va_start (arguments, fmt);

  if (_checkLogLevel (lObj, lvl))
    {
      SET_ZERO (lObj->_buffer);

      vsnprintf (lObj->_buffer, LOG_BUFFER_SIZE, fmt, arguments);

      _log (lObj, lvl, mode);
    }

  va_end (arguments);
}

/****************************************************************************/
