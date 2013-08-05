/**
 * @file tskmod.c
 * Contains code for task creation (light weight and heavy process).
 * @author RD
 * @date Sun May 26 16:20:42 IST 2013
 */

#include "_tskmod.h"

/**
 * Init memory for task object.
 * @param tskObjPtr task object pointer.
 * @param mObj memory object that will be used for allocations.
 * @return SUCCESS or other error codes incase of failure.
 */
genErr_t
bs_tskmodInit (bs_tskmodCls *tskObjPtr, bs_mmodCls mObj)
{
  void *ptr = NULL;
  genErr_t retVal;

  if(tskObjPtr == NULL)
    return INVALID_MEM_LOC;
  *tskObjPtr = NULL;

  retVal = bs_allocMem (mObj, sizeof (struct bs_tskmodClsType), &ptr);
  if (retVal != SUCCESS)
    return retVal;

  *tskObjPtr = (bs_tskmodCls) ptr;

  (*tskObjPtr)->_validFlag = true;
  (*tskObjPtr)->_pid = getpid();
  (*tskObjPtr)->_type = TSK_HEAVY;

#ifdef CHILD_LIST
  (*tskObjPtr)->_parent = true;
  (*tskObjPtr)->_child = NULL;
  (*tskObjPtr)->_nextPtr = NULL;
  (*tskObjPtr)->_num_child = 0;
#endif

  return SUCCESS;
}

/**
 * Finalize memory for task object.
 * @param tskObjPtr Task object pointer.
 * @param mObj that will be used for memory operations.
 * @return SUCCESS or other error codes incase of failure.
 */
genErr_t
bs_tskmodFin (bs_tskmodCls *tskObjPtr, bs_mmodCls mObj)
{
  validateObj (*tskObjPtr);

  genErr_t retVal;

  (*tskObjPtr)->_validFlag = false;

  retVal = bs_freeMem (mObj, (void *) tskObjPtr);
  if (retVal != SUCCESS)
    return retVal;

  return SUCCESS;
}

/**
 * Create/Spawn new process.
 * @param tskObjPtr task object pointer
 * @param mObj used to allocate memory for the new process object
 * @param spawnCB handler that will be called after the new process is spawned
 * @param argv the arguments to the spawnCB
 * @return new taskObject that will contain the pid of the new process.
 */
bs_tskmodCls
bs_spawn (bs_tskmodCls tskObjPtr, bs_mmodCls mObj, bs_spawnCBType spawnCB,
          char *argv[])
{
  pid_t pid;
  genErr_t retVal;
  bs_tskmodCls newtskObjPtr;

  validateObj (tskObjPtr);

  retVal = bs_tskmodInit(&newtskObjPtr, mObj);

  if(SUCCESS != retVal)
    {
      return NULL;
    }

  pid = fork();

  if (pid == -1)
    return NULL;

  if (pid != 0)
    {
      /*parent process*/
      /* adjust the new allocated task object */
      newtskObjPtr ->_pid = pid;

#ifdef CHILD_LIST
      newtskObjPtr ->_parent = false;

      /* Add this to the parent't child list */
      if (tskObjPtr->_child == NULL)
        {
          tskObjPtr->_child = newtskObjPtr;
        }
      else
        {
          /*Search until the end of child list and add at end*/
          bs_tskmodCls tPtr = tskObjPtr->_child;
          do
            {
              if((tPtr = tPtr->_nextPtr) == NULL)
                break;
            }while(tPtr);
          tPtr->_nextPtr = newtskObjPtr;
        }
      tskObjPtr->_num_child++;
#endif
    }
  else
    {
      /*Child process*/
      /*Adjust the child pid*/
      newtskObjPtr->_pid = getpid();
      /*Call the spwan callback handler. This might not return
        (exec) may be called.*/
      spawnCB(newtskObjPtr, argv);
    }

  return newtskObjPtr;
}

/**
 * Exec new binary over the existing process.
 * @param tskObjPtr task object pointer
 * @param path binary that will be loaded
 * @param argv the arguments to the binary
 * @param env environment variables to the binary
 * @note Usage of env variable depends on avialbility of __USE_GNU
 * @return Will NOT return if successful else will return the error code
 */
genErr_t
bs_exec (bs_tskmodCls tskObjPtr, char *path, char *argv[], char *env[])
{
  int ret;

  validateObj (tskObjPtr);

#ifdef __USE_GNU
  ret = execvpe(path, argv, env);
#else
  (void)env;
  ret = execvp(path, argv);
#endif

  if (ret == -1)
    return errno2EC (errno);

  return SUCCESS;
}

/**
 * Function that will be called on creation of a LW process.
 * @param argsPtr Contain the user callback on LW process creation and its
 * arguments. The args also contain memory object reference that will be used
 * to free the args memory allocated in bs_spawnLW.
 * @note The error code of free memory is ignored currently.
 * @return return value from the user defined call back handler.
 */
PRIVATE genErr_t
bs_threadFun (void *argsPtr)
{
  bs_mmodCls mObj;
  genErr_t retVal = FAILURE;
  bs_tskArgsType *args = (bs_tskArgsType*)argsPtr;

  mObj = args->mObj;

  if(args->spawnCB)
    retVal = args->spawnCB(args->tskPtr, args->argv);

  bs_freeMem (mObj, (void **)&args);

  return retVal;
}

/**
 * Create/Spawn new light weight process.
 * @param tskObjPtr task object pointer
 * @param mObj used to allocate memory for the new process object
 * @param spawnCB handler that will be called after the new process is spawned
 * @param argv the arguments to the spawnCB
 * @return new taskObject that will contain the pid of the new process.
 */
bs_tskmodCls
bs_spawnLW (bs_tskmodCls tskObjPtr, bs_mmodCls mObj, bs_spawnCBType spawnCB,
            char *argv[])
{
  pthread_t tid;
  genErr_t retVal;
  int ret;
  void *ptr = NULL;
  bs_tskArgsType *args;
  bs_tskmodCls newtskObjPtr;

  validateObj (tskObjPtr);

  if(NULL == spawnCB)
    {
      return NULL;
    }

  retVal = bs_tskmodInit(&newtskObjPtr, mObj);

  if(SUCCESS != retVal)
    {
      return NULL;
    }

  retVal = bs_allocMem (mObj, sizeof (bs_tskArgsType), &ptr);
  if (retVal != SUCCESS)
    return NULL;

  args = (bs_tskArgsType*) ptr;

  args->tskPtr = newtskObjPtr;
  args->spawnCB = spawnCB;
  args->argv = argv;
  args->mObj = mObj;

  ret = pthread_create(&tid, NULL, (void *)&bs_threadFun, (void *)args);
  if (ret != 0)
    return NULL;

  /*parent process*/
  /* adjust the new allocated task object */
  newtskObjPtr->_type = TSK_LIGHT;
  newtskObjPtr->_tid = tid;

#ifdef CHILD_LIST
  newtskObjPtr->_parent = false;

  /* Add this to the parent't child list */
  if (tskObjPtr->_child == NULL)
    {
      tskObjPtr->_child = newtskObjPtr;
    }
  else
    {
      /*Search until the end of child list and add at end*/
      bs_tskmodCls tPtr = tskObjPtr->_child;
      do
        {
          if(tPtr->_nextPtr == NULL)
            break;
          else
            tPtr = tPtr->_nextPtr;
        }while(tPtr);
      tPtr->_nextPtr = newtskObjPtr;
    }
  tskObjPtr->_num_child++;
#endif

  return newtskObjPtr;
}

/**
 * Wait or Join the child process with the main
 * @param tskObjPtr task object pointer
 * @param retP contains the return value of the child process.
 * @return error status on error else success
 */
genErr_t
bs_wait (bs_tskmodCls tskObjPtr, genErr_t *retP)
{
  int ret;

  validateObj (tskObjPtr);

  if(tskObjPtr->_type == TSK_LIGHT)
    {
      ASSERT(tskObjPtr->_tid != 0);
      ret = pthread_join(tskObjPtr->_tid, (void**)&retP);
      if (ret != 0)
        return errno2EC (ret);
    }
  else
    {
      int pRet;

      ASSERT(tskObjPtr->_pid != 0);
      ret = waitpid(tskObjPtr->_pid, &pRet, 0);
      if (ret == -1)
        return errno2EC (errno);

      if(WIFEXITED(pRet))
        *retP = SUCCESS;
      else
        *retP = FAILURE;
    }

  return SUCCESS;
}

/****************************************************************************/
