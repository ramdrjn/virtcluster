/**
 * @file mmod.c
 * Contains Memory routines.
 * @author RD
 * @date Mon Jan 26 20:06:57 EET 2009
 */

#include "_mmod.h"

/**
 * Init routine that creates the memory object.
 * @param memObjPtr Reference where the newly allocated memory object's
 * details are stored. If memory is not available then the appropriate
 * \c error-code is returned.
 * @return The \c error-string if any error during allocation of memory else
 * success is returned.
 */
genErr_t
bs_mmodInit (bs_mmodCls * memObjPtr)
{
  if(memObjPtr == NULL)
    return INVALID_MEM_LOC;
  *memObjPtr = NULL;

  *memObjPtr = malloc (sizeof (struct bs_mmodClsType));
  if (!*memObjPtr)
    return ((errno) ? errno2EC (errno) : MEM_ALLOC_FAIL);

  (*memObjPtr)->_validFlag = true;

  return SUCCESS;
}

/**
 * Finalize the memory object before exit.
 * @param memObjPtr Reference to the memory object that needs to be destroyed.
 * @return The \c error-string if any error during finalization of the
 * memory object.
 */
genErr_t
bs_mmodFin (bs_mmodCls * memObjPtr)
{
  validateObj ((*memObjPtr));

  (*memObjPtr)->_validFlag = false;

  free (*memObjPtr);
  return SUCCESS;
}

/**
 * Allocate new memory of size and store its address in the location pointed.
 * @param mObj Memory object.
 * @param size Requested size of memory.
 * @param mem Reference to the location that needs to hold the allocated
 * memory address.
 * @return The \c error-string if any error during the allocation.
 */
genErr_t
bs_allocMem (bs_mmodCls mObj, size_t size, void **mem)
{
  validateObj (mObj);

  if(mem == NULL)
    return INVALID_MEM_LOC;
  *mem = NULL;

  *mem = calloc (1, size);
  if (!*mem)
    return ((errno) ? errno2EC (errno) : MEM_ALLOC_FAIL);
  return SUCCESS;
}

/**
 * Free the memory in the location pointed mem.
 * @note the memory location would be freed and set to NULL.
 * @param memObj Memory object.
 * @param mem Reference to the allocated memory that needs to be freed.
 * @return The \c error-string if any error else SUCCESS.
 */
genErr_t
bs_freeMem (bs_mmodCls memObj, void **mem)
{
  validateObj (memObj);

  if(mem == NULL)
    return INVALID_MEM_LOC;

  free (*mem);

  *mem= NULL;

  return SUCCESS;
}

/****************************************************************************/
