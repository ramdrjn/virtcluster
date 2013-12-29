/**
 * @file fmod.c
 * Contains File routines.
 * @author RD
 * @date Mon Jan 26 20:06:57 EET 2009
 */

#include "_fmod.h"

/**
 * Init Allocates memory for the fobj.
 * @param fObjPtr Reference where the newly allocated file object will be
 * stored.
 * @param mObj Reference of the memory object that will be used in the
 * memory allocation. If memory is not available then the appropriate
 * \c error-code is returned.
 * @return The \c error-code if any error during allocation of memory else
 * success is returned.
 */
genErr_t
bs_fmodInit (bs_fmodCls *fObjPtr, bs_mmodCls mObj)
{
  void *ptr = NULL;
  genErr_t retVal;

  if(fObjPtr == NULL)
    return INVALID_MEM_LOC;
  *fObjPtr = NULL;

  retVal = bs_allocMem (mObj, sizeof (struct bs_fmodClsType), &ptr);
  if (retVal != SUCCESS)
    return retVal;

  *fObjPtr = (bs_fmodCls) ptr;

  (*fObjPtr)->_validFlag = true;
  (*fObjPtr)->_fd = -1;
  (*fObjPtr)->_fp = NULL;
  (*fObjPtr)->_type = F_BINARY;

  return SUCCESS;
}

/**
 * Finalize the object and close the files on exit.
 * @param fObjPtr Reference of the file object.
 * @param mObj Reference of the memory object.
 * @return The \c error-code if any error during freeing of memory or during
 * file close. Else success is returned.
 */
genErr_t
bs_fmodFin (bs_fmodCls *fObjPtr, bs_mmodCls mObj)
{
  validateObj (*fObjPtr);

  genErr_t retVal;

  if((*fObjPtr)->_type != F_SPECIAL)
    {
      retVal = bs_fClose (*fObjPtr);
      if (retVal != SUCCESS)
        return retVal;
    }

  (*fObjPtr)->_validFlag = false;

  retVal = bs_freeMem (mObj, (void *) fObjPtr);
  if (retVal != SUCCESS)
    return retVal;

  return SUCCESS;
}

/**
 * Create a new file specified by the path name.
 * @param fObj Reference of the file object.
 * @param fPath Path of the file to be created. File name also should be part
 * of the path.
 * @param fPerm Permissions for the file. These will be set when the file is
 * created.
 * @return The \c error-code if any error during the file creation.
 * @note The file descriptor is closed after the file is created. The file
 * needs to be opened for appropriate actions.
 */
genErr_t
bs_fCreate (bs_fmodCls fObj, const char *fPath, mode_t fPerm)
{
  validateObj (fObj);

  int fd;

  fd = creat (fPath, fPerm);
  if (fd == -1)
    return errno2EC (errno);

  close (fd);

  return SUCCESS;
}

/**
 * Open the file with the specified mode and the type.
 * @param fObj Reference of the file object.
 * @param fPath Path of the file to be created. File name also should be part
 * of the path.
 * @param fType Type of the file that will be set after opening the file.
 * @param fMode Mode i.e read mode, write mode etc in which the file will be
 * opened.
 * @return The \c error-code if any error during the file operation.
 */
genErr_t
bs_fOpen (bs_fmodCls fObj, const char *fPath, bs_e_fType fType,
          bs_e_fAMode fMode)
{
  validateObj (fObj);

  switch (fType)
    {
    case F_BINARY:
      {
        int flags;

        switch (fMode)
          {
          case FA_RDWR:
            {
              flags = O_RDWR;
              break;
            }
          case FA_WR:
            {
              flags = O_WRONLY;
              break;
            }
          case FA_APND:
            {
              flags = O_APPEND;
              break;
            }
          case FA_RD:
            {
              flags = O_RDONLY;
              break;
            }
          default:
            {
              flags = 0;
            }
          }

        fObj->_fd = open (fPath, flags);
        if (fObj->_fd == -1)
          return errno2EC (errno);
        break;
      }
    case F_ASCII:
      {
        char *flags;

        switch (fMode)
          {
          case FA_RDWR:
            {
              flags = "r+";
              break;
            }
          case FA_WR:
            {
              flags = "w";
              break;
            }
          case FA_APND:
            {
              flags = "a";
              break;
            }
          case FA_RD:
            {
              flags = "r";
              break;
            }
          default:
            {
              flags = NULL;
            }
          }

        fObj->_fp = fopen (fPath, flags);
        if (fObj->_fp == NULL)
          return errno2EC (errno);
        break;
      }
    case F_SPECIAL:
    default:
      return INVALID_FILETYP;
    }
  fObj->_type = fType;

  return SUCCESS;
}

/**
 * Close the file.
 * @param fObj Reference of the file object.
 * @return The \c error-code if any error during the file operatoin.
 */
genErr_t
bs_fClose (bs_fmodCls fObj)
{
  validateObj (fObj);

  int status = 0;
  genErr_t retVal = SUCCESS;

  switch (fObj->_type)
    {
    case F_BINARY:
      {
        if (fObj->_fd)
          {
            /*EBADF is returned if the fd is already closed. */
            status = close (fObj->_fd);
            if (status == -1)
              retVal = errno2EC (errno);
            fObj->_fd = -1;
          }
        break;
      }
    case F_ASCII:
      {
        if (fObj->_fp)
          {
            status = fclose (fObj->_fp);
            if (status == EOF)
              retVal = errno2EC (errno);
            fObj->_fp = NULL;
          }
        break;
      }
    case F_SPECIAL:
    default:
      retVal = INVALID_FILETYP;
    }
  return retVal;
}

/**
 * Set file object options using fcntl.
 * @param fObj Reference of the file object.
 * @param cmd The option to be set/get.
 * @param argP The arguments to the option command.
 * @return The \c error-code if any error during the file operatoin.
 */
genErr_t
bs_fOpts (bs_fmodCls fObj, int cmd, void *argP)
{
  validateObj (fObj);

  int status = 0;
  int *opt = NULL;
  genErr_t retVal = SUCCESS;

  if(cmd == F_SETFL)
    {
      opt = (int *)argP;
    }

  status = fcntl(fObj->_fd, cmd, *opt);
  if (status == -1)
    retVal = errno2EC (errno);

  return retVal;
}

/**
 * Get the FD from teh object
 * @param fObj Reference of the file object.
 * @return The FD value on success else error code on failure
 */
int
bs_getFD (bs_fmodCls fObj)
{
  int fd = -1;
  validateObj (fObj);

  switch (fObj->_type)
    {
    case F_BINARY:
      {
        fd = fObj->_fd;
        break;
      }
    case F_ASCII:
      {
        fd = fileno(fObj->_fp);
        break;
      }
    case F_SPECIAL:
      {
        fd = fObj->_fd;
        break;
      }
    default:
      fd = -1;
    }
  return fd;
}

/**
 * Returns a fobj for the passed fd. Used in cases of special fd like sockets.
 * This would allow regular file operations to be performed over the fd.
 * @param fd The file descriptor that will be updated to the file object.
 * @param fObjPtr Reference of the file object which will be updated
 * @note bs_fmodInit should be called before the fObjPtr is passed.
 * @return The \c error-code if any error during the file operatoin.
 */
genErr_t
bs_fObjectify (int fd, bs_fmodCls fObjPtr)
{
  validateObj (fObjPtr);

   fObjPtr->_fd = fd;
   if (fd >=2)
     {
       fObjPtr->_type = F_SPECIAL;
     }
   else
     {
       fObjPtr->_type = F_BINARY;
     }

  return SUCCESS;
}

/**
 * Returns a fobj for the passed file pointer.
 * @param fp The file pointer.
 * @param fObjPtr Reference of the file object which will be updated
 * @note bs_fmodInit should be called before the fObjPtr is passed.
 * @return The \c error-code if any error during the file operatoin.
 */
genErr_t
bs_fObjectify_ascii (FILE *fp, bs_fmodCls fObjPtr)
{
  validateObj (fObjPtr);

  fObjPtr->_fp = fp;

  if ((fp == stdin) || (fp == stdout) || (fp == stderr))
    {
      fObjPtr->_type = F_ASCII;
    }
  else
    {
      fObjPtr->_type = F_SPECIAL;
    }

  return SUCCESS;
}

/**
 * Read from a file and store contents in buffer.
 * @param fObj Reference of the file object.
 * @param buffer The memory storage area where the read contents are stored.
 * @param size Request to read this amount of data from channel.
 * @param retCount The amount/size of the data read from the stream.
 * @return The \c error-code if any error during the file creation.
 * @note In the case of the binary file the exact amount of data read is
 * returned in retCount, whereas in the case of the ascii value the passed
 * \c size value is returned as the retCount value.
 */
genErr_t
bs_fRead (bs_fmodCls fObj, void *buffer, int size, int *retCount)
{
  validateObj (fObj);

  genErr_t retVal = SUCCESS;

  switch (fObj->_type)
    {
    case F_BINARY:
      {
        ssize_t count;
        count = read (fObj->_fd, buffer, (size_t) size);
        if (count == -1)
          retVal = errno2EC (errno);
        if (retCount)
          *retCount = (int) count;

        break;
      }
    case F_ASCII:
      {
        size_t count;
        count = fread (buffer, (size_t) size, (size_t) 1, fObj->_fp);
        if (ferror (fObj->_fp))
          {
            retVal = errno2EC (errno);
            clearerr (fObj->_fp);
          }
        /*Note: here the item count is returned instead of the bytes written.
          Hence the initial size is returned so as to keep the API consistant.*/
        if (retCount)
          *retCount = (count) ? size : 0;

        break;
      }
    case F_SPECIAL:
    default:
      retVal = INVALID_FILETYP;
    }
  return retVal;
}

/**
 * Write to a file and taking contents from buffer.
 * @param fObj Reference of the file object.
 * @param buffer The memory location from where data is read for writing.
 * @param size Size of the data that is to be written.
 * @param retCount The actual amount/size of the data that is written to the
 * stream.
 * @return The \c error-code if any error during the file creation.
 * @note In the case of the binary file the exact amount of data written is
 * returned in retCount, whereas in the case of the ascii value the passed
 * \c size value is returned as the retCount value.  That is because in the
 * case of the ascii file the item count is returned instead of the bytes
 * written. Hence the initial size is returned so as to keep the API
 * consistant.
 */
genErr_t
bs_fWrite (bs_fmodCls fObj, const void *buffer, int size, int *retCount)
{
  validateObj (fObj);

  genErr_t retVal = SUCCESS;

  switch (fObj->_type)
    {
    case F_BINARY:
      {
        ssize_t count;
        count = write (fObj->_fd, buffer, (size_t) size);
        if (count == -1)
          retVal = errno2EC (errno);
        else if (retCount)
          *retCount = (int) count;

        break;
      }
    case F_ASCII:
      {
        size_t count;
        count = fwrite (buffer, (size_t) size, (size_t) 1, fObj->_fp);
        if (ferror (fObj->_fp))
          {
            retVal = errno2EC (errno);
            clearerr (fObj->_fp);
          }
        /*Note: here the item count is returned instead of the bytes written.
          Hence the initial size is returned so as to keep the API consistant.*/
        if (retCount)
          *retCount = (count) ? size : 0;

        break;
      }
    case F_SPECIAL:
    default:
      retVal = INVALID_FILETYP;
    }
  return retVal;
}

/**
 * Read a line from a file and store contents in buffer.
 * @param fObj Reference of the file object.
 * @param buffer The memory storage area where the read contents are stored.
 * @param size Request to read this amount of data from channel.
 * @return The \c error-code if any error during the file creation.
 * @note The function is only for ascii files.
 */
genErr_t
bs_fLineRead (bs_fmodCls fObj, void *buffer, int size)
{
  validateObj (fObj);

  genErr_t retStatus = SUCCESS;

  if (fObj->_type == F_ASCII)
    {
      fgets(buffer, size, fObj->_fp);
      if (ferror (fObj->_fp))
        {
          retStatus = errno2EC (errno);
          clearerr (fObj->_fp);
        }
    }
  else
    retStatus = INVALID_FILETYP;

  return retStatus;
}

/**
 * Write a line from a file and store contents in buffer.
 * @param fObj Reference of the file object.
 * @param buffer The memory storage area where the contents are stored.
 * @return The \c error-code if any error during the file operation.
 * @note The function is only for ascii files.
 */
genErr_t
bs_fLineWrite (bs_fmodCls fObj, void *buffer)
{
  validateObj (fObj);
  int retVal = -1;
  genErr_t retStatus = SUCCESS;

  if (fObj->_type == F_ASCII)
    {
      retVal = fputs(buffer, fObj->_fp);
      if (retVal == EOF)
        {
          retStatus = errno2EC (errno);
        }
    }
  else
    retStatus = INVALID_FILETYP;

  return retStatus;
}

/**
 * Variable Read from a file and store contents in buffer.
 * @note Only for ascii files.
 * @param fObj Reference of the file object.
 * @param retCount contains the number of bytes read.
 * @param fmt The format string for the variable arguments.
 * @return The \c error-code if any error during the file creation.
 * @note Buffer specification //??
 */
genErr_t
bs_fReadV (bs_fmodCls fObj, int *retCount, const char *fmt, ...)
{
  validateObj (fObj);

  int retVal = EOF;
  genErr_t retStatus = SUCCESS;

  va_list args;

  va_start (args, fmt);

  if (fObj->_type == F_ASCII)
    {
      retVal = vfscanf (fObj->_fp, fmt, args);
      if (ferror (fObj->_fp))
        {
          retStatus = errno2EC (errno);
          clearerr (fObj->_fp);
        }
    }
  else
    retStatus = INVALID_FILETYP;

  va_end (args);

  if(retCount)
    *retCount = retVal;

  return retStatus;
}

/**
 * Variable Write to a file and taking contents from buffer.
 * @note Only for ascii files.
 * @param fObj Reference of the file object.
 * @param retCount contains the number of bytes written.
 * @param fmt The format string for the variable arguments.
 * @return The \c error-code if any error during the file creation.
 * @note Buffer specification //??
 */
genErr_t
bs_fWriteV (bs_fmodCls fObj, int *retCount, const char *fmt, ...)
{
  validateObj (fObj);

  int retVal = EOF;
  genErr_t retStatus = SUCCESS;

  va_list args;

  va_start (args, fmt);

  if (fObj->_type == F_ASCII)
    {
      retVal = vfprintf (fObj->_fp, fmt, args);
      if (retVal < 0)
        retStatus = errno2EC (errno);
    }
  else
    retVal = INVALID_FILETYP;

  va_end (args);

  if (retCount)
    *retCount = retVal;

  return retStatus;
}

/**
 * Read with support for vectored IO
 * @note Only for binary files.
 * @param fObj Reference of the file object.
 * @param vec The vector of iovec bases and their counts.
 * @param retCount the number of bytes read.
 * @return The \c error-code if any error during the file creation.
 */
genErr_t
bs_fVecRead (bs_fmodCls fObj, vec_io vec, int *retCount)
{
  int retVal = -1;
  genErr_t retStatus = SUCCESS;

  validateObj (fObj);

  if(vec == NULL)
    return INVALID_MEM_LOC;

  if (fObj->_type == F_BINARY)
    {
      retVal = readv(fObj->_fd, vec->ioVecPtr, vec->vecCount);
      if (retVal < 0)
        retStatus = errno2EC (errno);
    }
  else
    retVal = INVALID_FILETYP;

  if (retCount)
    *retCount = retVal;

  return retStatus;
}

/**
 * Vectored IO write.
 * @note Only for binary files.
 * @param fObj Reference of the file object.
 * @param vec vector base.
 * @param retCount the number of bytes written.
 * @return The \c error-code if any error during the file creation.
 */
genErr_t
bs_fVecWrite (bs_fmodCls fObj, vec_io vec, int *retCount)
{
  validateObj (fObj);

  int retVal = -1;
  genErr_t retStatus = SUCCESS;

  if(vec == NULL)
    return INVALID_MEM_LOC;

  if (fObj->_type == F_BINARY)
    {
      retVal = writev(fObj->_fd, vec->ioVecPtr, vec->vecCount);
      if (retVal < 0)
        retStatus = errno2EC (errno);
    }
  else
    retStatus = INVALID_FILETYP;

  if(retCount)
    *retCount = retVal;

  return retStatus;
}

/****************************************************************************/
