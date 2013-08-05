/**
 * @file base_ifc.c
 * Contains datastructure implementations.
 * @author RD
 * @date Tue Feb 22 18:20:59 IST 2011
 */

#include "_dsbase.h"

/**
 * Initialize object. The base init function is invoked and register data
 * structure. Memory is allocated here for the object.
 * @param stPtr Object reference.
 * @param mObj Reference of the memory object that will be used in the
 * memory allocation. If memory is not available then the appropriate
 * \c error-code is returned.
 * @return The \c error-code if any error during allocation of memory else
 * success is returned.
 */
genErr_t
ds_st_init (ds_stack * stPtr, bs_mmodCls mObj)
{
  genErr_t retVal;
  void *ptr = NULL;

  if(stPtr == NULL)
    return INVALID_MEM_LOC;
  *stPtr = NULL;

  retVal = bs_allocMem (mObj, sizeof (struct ds_stackType), &ptr);
  if (retVal != SUCCESS)
    return retVal;
  (*stPtr) = (ds_stack) ptr;

  return ds_dsBaseInit (&((*stPtr)->base), DS_STACK);
}

/**
 * Finalize the object. The base finalize function is invoked.
 * Memory will be freed for the object inside this.
 * @param stPtr Reference of the object.
 * @param mObj Reference of the memory object that will be used for the memory
 * operations.
 * @return The \c error-code if any error during memory operations else
 * success is returned.
 */
genErr_t
ds_st_fin (ds_stack * stPtr, bs_mmodCls mObj)
{
  genErr_t retVal;

  if(stPtr == NULL)
    return INVALID_MEM_LOC;

  retVal = ds_dsBaseFin (&((*stPtr)->base));
  if (retVal != SUCCESS)
    return retVal;

  retVal = bs_freeMem (mObj, (void *) stPtr);

  return retVal;
}

/**
 * Return empty status.
 * @param stPtr
 * @return The value \c True is returned if the ds is non-empty, Else \c false
 * is returned.
 */
t_bool
ds_st_is_empty (ds_stack stPtr)
{
  return ds_isEmpty (&stPtr->base);
}

/**
 * Return the count.
 * @param stPtr
 * @return number of elements in the data structure.
 */
unsigned short
ds_st_get_count (ds_stack stPtr)
{
  return ds_getCount (&stPtr->base);
}

/**
 * Set the element limit.
 * @param stPtr
 * @return The limit value that will be set for the data structure.
 */
genErr_t
ds_st_limit (ds_stack stPtr, unsigned short element_limit)
{
  return ds_setElementLimit (&stPtr->base, element_limit);
}

/**
 * Insert the packet.
 * The packet container needs to be initialised with data before this.
 * @param stPtr
 * @param data The packet container.
 * @return The \c error-code if any error during memory operations else
 * success is returned.
 */
genErr_t
ds_st_insert (ds_stack stPtr, ds_packetContainer * data)
{
  return ds_insert (&stPtr->base, data, 0, DS_RIGHT);
}

/**
 * Remove packet.
 * The packet container that is removed is returned. Memory for this packet
 * container needs to be freed elsewhere.
 * @param stPtr
 * @return The packet container is returned.
 */
ds_packetContainer *
ds_st_remove (ds_stack stPtr)
{
  return ds_remove (&stPtr->base, 0, DS_TAIL);
}

/**
 * Clear the data structure.
 * The packet container is freed using the memory object. If the memory object
 * is NULL then the packet container memory is not freed.
 * container needs to be freed elsewhere.
 * @param stPtr
 * @param mObj The memory object reference that will be used for freeing the
 * packet containers in the data structure.
 * @return The \c error-code if any error during memory operations else
 * success is returned.
 */
genErr_t
ds_st_clear (ds_stack stPtr, bs_mmodCls mObj)
{
  return ds_clear (&stPtr->base, mObj);
}

/**
 * Traverse the data structure.
 * The callback function returns either a node or null. If a node is returned
 * the traversal function stops. Additional arguments to the call back
 * handler can be passed as the CBHArgs.
 * @param stPtr
 * @param CBHandle The call back function that would be called inside traverse.
 * @param CBHArgs The arguments to the call back handler.
 * @return Node that is returned by the call back function.
 */
ds_packetContainer *
ds_st_traverse (ds_stack stPtr, CBHandleType CBHandle, void *CBHArgs)
{
  return ds_traverse (&stPtr->base, CBHandle, CBHArgs, 0, DS_LEFT);
}

/**
 * Initialize object. The base init function is invoked and register data
 * structure. Memory is allocated here for the object.
 * @param quPtr Object reference.
 * @param mObj Reference of the memory object that will be used in the
 * memory allocation. If memory is not available then the appropriate
 * \c error-code is returned.
 * @return The \c error-code if any error during allocation of memory else
 * success is returned.
 */
genErr_t
ds_qu_init (ds_queue * quPtr, bs_mmodCls mObj)
{
  genErr_t retVal;
  void *ptr = NULL;

  if(quPtr == NULL)
    return INVALID_MEM_LOC;
  *quPtr = NULL;

  retVal = bs_allocMem (mObj, sizeof (struct ds_queueType), &ptr);
  if (retVal != SUCCESS)
    return retVal;

  (*quPtr) = (ds_queue) ptr;

  return ds_dsBaseInit (&((*quPtr)->base), DS_QUEUE);
}

/**
 * Finalize the object. The base finalize function is invoked.
 * Memory will be freed for the object inside this.
 * @param quPtr Reference of the object.
 * @param mObj Reference of the memory object that will be used for the memory
 * operations.
 * @return The \c error-code if any error during memory operations else
 * success is returned.
 */
genErr_t
ds_qu_fin (ds_queue * quPtr, bs_mmodCls mObj)
{
  genErr_t retVal;

  if(quPtr == NULL)
    return INVALID_MEM_LOC;

  retVal = ds_dsBaseFin (&((*quPtr)->base));
  if (retVal != SUCCESS)
    return retVal;

  retVal = bs_freeMem (mObj, (void *) quPtr);

  return retVal;
}

/**
 * Return empty status.
 * @param quPtr
 * @return The value \c True is returned if the ds is non-empty, Else \c false
 * is returned.
 */
t_bool
ds_qu_is_empty (ds_queue quPtr)
{
  return ds_isEmpty (&quPtr->base);
}

/**
 * Return the count.
 * @param quPtr
 * @return number of elements in the data structure.
 */
unsigned short
ds_qu_get_count (ds_queue quPtr)
{
  return ds_getCount (&quPtr->base);
}

/**
 * Set the element limit.
 * @param quPtr
 * @return The limit value that will be set for the data structure.
 */
genErr_t
ds_qu_limit (ds_queue quPtr, unsigned short element_limit)
{
  return ds_setElementLimit (&quPtr->base, element_limit);
}

/**
 * Insert the packet.
 * The packet container needs to be initialised with data before this.
 * @param quPtr
 * @param data The packet container.
 * @return The \c error-code if any error during memory operations else
 * success is returned.
 */
genErr_t
ds_qu_insert (ds_queue quPtr, ds_packetContainer * data)
{
  return ds_insert (&quPtr->base, data, 0, DS_RIGHT);
}

/**
 * Remove packet.
 * The packet container that is removed is returned. Memory for this packet
 * container needs to be freed elsewhere.
 * @param quPtr
 * @return The packet container is returned.
 */
ds_packetContainer *
ds_qu_remove (ds_queue quPtr)
{
  return ds_remove (&quPtr->base, 0, DS_HEAD);
}

/**
 * Clear the data structure.
 * The packet container is freed using the memory object. If the memory object
 * is NULL then the packet container memory is not freed.
 * container needs to be freed elsewhere.
 * @param quPtr
 * @param mObj The memory object reference that will be used for freeing the
 * packet containers in the data structure.
 * @return The \c error-code if any error during memory operations else
 * success is returned.
 */
genErr_t
ds_qu_clear (ds_queue quPtr, bs_mmodCls mObj)
{
  return ds_clear (&quPtr->base, mObj);
}

/**
 * Traverse the data structure.
 * The callback function returns either a node or null. If a node is returned
 * the traversal function stops. Additional arguments to the call back
 * handler can be passed as the CBHArgs.
 * @param quPtr
 * @param CBHandle The call back function that would be called inside traverse.
 * @param CBHArgs The arguments to the call back handler.
 * @return Node that is returned by the call back function.
 */
ds_packetContainer *
ds_qu_traverse (ds_queue quPtr, CBHandleType CBHandle, void *CBHArgs)
{
  return ds_traverse (&quPtr->base, CBHandle, CBHArgs, 0, DS_RIGHT);
}

/**
 * Initialize object. The base init function is invoked and register data
 * structure. Memory is allocated here for the object.
 * @param cqPtr Object reference.
 * @param mObj Reference of the memory object that will be used in the
 * memory allocation. If memory is not available then the appropriate
 * \c error-code is returned.
 * @return The \c error-code if any error during allocation of memory else
 * success is returned.
 */
genErr_t
ds_cq_init (ds_cqueue * cqPtr, bs_mmodCls mObj)
{
  genErr_t retVal;
  void *ptr = NULL;

  if(cqPtr == NULL)
    return INVALID_MEM_LOC;
  *cqPtr = NULL;

  retVal = bs_allocMem (mObj, sizeof (struct ds_cqueueType), &ptr);
  if (retVal != SUCCESS)
    return retVal;
  (*cqPtr) = (ds_cqueue) ptr;

  return ds_dsBaseInit (&((*cqPtr)->base), DS_CDLIST);
}

/**
 * Finalize the object. The base finalize function is invoked.
 * Memory will be freed for the object inside this.
 * @param cqPtr Reference of the object.
 * @param mObj Reference of the memory object that will be used for the memory
 * operations.
 * @return The \c error-code if any error during memory operations else
 * success is returned.
 */
genErr_t
ds_cq_fin (ds_cqueue * cqPtr, bs_mmodCls mObj)
{
  genErr_t retVal;

  if(cqPtr == NULL)
    return INVALID_MEM_LOC;

  retVal = ds_dsBaseFin (&((*cqPtr)->base));
  if (retVal != SUCCESS)
    return retVal;

  retVal = bs_freeMem (mObj, (void *) cqPtr);

  return retVal;
}

/**
 * Return empty status.
 * @param cqPtr
 * @return The value \c True is returned if the ds is non-empty, Else \c false
 * is returned.
 */
t_bool
ds_cq_is_empty (ds_cqueue cqPtr)
{
  return ds_isEmpty (&cqPtr->base);
}

/**
 * Return the count.
 * @param cqPtr
 * @return number of elements in the data structure.
 */
unsigned short
ds_cq_get_count (ds_cqueue cqPtr)
{
  return ds_getCount (&cqPtr->base);
}

/**
 * Set the element limit.
 * @param cqPtr
 * @return The limit value that will be set for the data structure.
 */
genErr_t
ds_cq_limit (ds_cqueue cqPtr, unsigned short element_limit)
{
  return ds_setElementLimit (&cqPtr->base, element_limit);
}

/**
 * Insert the packet.
 * The packet container needs to be initialised with data before this.
 * @param cqPtr
 * @param data The packet container.
 * @param node The packet container node selected for insertion.
 * @param dir The direction of insertion.
 * @return The \c error-code if any error during memory operations else
 * success is returned.
 */
genErr_t
ds_cq_insert (ds_cqueue cqPtr, ds_packetContainer * data)
{
  return ds_insert (&cqPtr->base, data, 0, DS_RIGHT);
}

/**
 * Remove packet.
 * The packet container that is removed is returned. Memory for this packet
 * container needs to be freed elsewhere.
 * @param cqPtr
 * @param node. The node that needs to be removed.
 * @return The packet container is returned.
 */
ds_packetContainer *
ds_cq_remove (ds_cqueue cqPtr)
{
  return ds_remove (&cqPtr->base, 0, DS_HEAD);
}

/**
 * Clear the data structure.
 * The packet container is freed using the memory object. If the memory object
 * is NULL then the packet container memory is not freed.
 * container needs to be freed elsewhere.
 * @param cqPtr
 * @param mObj The memory object reference that will be used for freeing the
 * packet containers in the data structure.
 * @return The \c error-code if any error during memory operations else
 * success is returned.
 */
genErr_t
ds_cq_clear (ds_cqueue cqPtr, bs_mmodCls mObj)
{
  return ds_clear (&cqPtr->base, mObj);
}

/**
 * Traverse the data structure.
 * The callback function returns either a node or null. If a node is returned
 * the traversal function stops. Additional arguments to the call back
 * hancqer can be passed as the CBHArgs.
 * @param cqPtr
 * @param CBHancqe The call back function that would be called inside traverse.
 * @param CBHArgs The arguments to the call back hancqer.
 * @param node The node from which traversal starts.
 * @param dir The of traversal.
 * @return Node that is returned by the call back function.
 */
ds_packetContainer *
ds_cq_traverse (ds_cqueue cqPtr, CBHandleType CBHandle, void *CBHArgs)
{
  return ds_traverse (&cqPtr->base, CBHandle, CBHArgs, 0, DS_RIGHT);
}

/**
 * Initialize object. The base init function is invoked and register data
 * structure. Memory is allocated here for the object.
 * @param slPtr Object reference.
 * @param mObj Reference of the memory object that will be used in the
 * memory allocation. If memory is not available then the appropriate
 * \c error-code is returned.
 * @return The \c error-code if any error during allocation of memory else
 * success is returned.
 */
genErr_t
ds_sl_init (ds_slist * slPtr, bs_mmodCls mObj)
{
  genErr_t retVal;
  void *ptr = NULL;

  if(slPtr == NULL)
    return INVALID_MEM_LOC;
  *slPtr = NULL;

  retVal = bs_allocMem (mObj, sizeof (struct ds_slistType), &ptr);
  if (retVal != SUCCESS)
    return retVal;
  (*slPtr) = (ds_slist) ptr;

  return ds_dsBaseInit (&((*slPtr)->base), DS_SLIST);
}

/**
 * Finalize the object. The base finalize function is invoked.
 * Memory will be freed for the object inside this.
 * @param slPtr Reference of the object.
 * @param mObj Reference of the memory object that will be used for the memory
 * operations.
 * @return The \c error-code if any error during memory operations else
 * success is returned.
 */
genErr_t
ds_sl_fin (ds_slist * slPtr, bs_mmodCls mObj)
{
  genErr_t retVal;

  if(slPtr == NULL)
    return INVALID_MEM_LOC;

  retVal = ds_dsBaseFin (&((*slPtr)->base));
  if (retVal != SUCCESS)
    return retVal;

  retVal = bs_freeMem (mObj, (void *) slPtr);

  return retVal;
}

/**
 * Return empty status.
 * @param slPtr
 * @return The value \c True is returned if the ds is non-empty, Else \c false
 * is returned.
 */
t_bool
ds_sl_is_empty (ds_slist slPtr)
{
  return ds_isEmpty (&slPtr->base);
}

/**
 * Return the count.
 * @param slPtr
 * @return number of elements in the data structure.
 */
unsigned short
ds_sl_get_count (ds_slist slPtr)
{
  return ds_getCount (&slPtr->base);
}

/**
 * Set the element limit.
 * @param slPtr
 * @return The limit value that will be set for the data structure.
 */
genErr_t
ds_sl_limit (ds_slist slPtr, unsigned short element_limit)
{
  return ds_setElementLimit (&slPtr->base, element_limit);
}

/**
 * Insert the packet.
 * The packet container needs to be initialised with data before this.
 * @param slPtr
 * @param data The packet container.
 * @param node The packet container node selected for insertion.
 * @param dir The direction of insertion.
 * @return The \c error-code if any error during memory operations else
 * success is returned.
 */
genErr_t
ds_sl_insert (ds_slist slPtr, ds_packetContainer * data,
              ds_packetContainer * node)
{
  return ds_insert (&slPtr->base, data, node, DS_RIGHT);
}

/**
 * Remove packet.
 * The packet container that is removed is returned. Memory for this packet
 * container needs to be freed elsewhere.
 * @param slPtr
 * @param node. The node that needs to be removed.
 * @return The packet container is returned.
 */
ds_packetContainer *
ds_sl_remove (ds_slist slPtr, ds_packetContainer * node, ds_e_headTail htail)
{
  return ds_remove (&slPtr->base, node, htail);
}

/**
 * Clear the data structure.
 * The packet container is freed using the memory object. If the memory object
 * is NULL then the packet container memory is not freed.
 * container needs to be freed elsewhere.
 * @param slPtr
 * @param mObj The memory object reference that will be used for freeing the
 * packet containers in the data structure.
 * @return The \c error-code if any error during memory operations else
 * success is returned.
 */
genErr_t
ds_sl_clear (ds_slist slPtr, bs_mmodCls mObj)
{
  return ds_clear (&slPtr->base, mObj);
}

/**
 * Traverse the data structure.
 * The callback function returns either a node or null. If a node is returned
 * the traversal function stops. Additional arguments to the call back
 * handler can be passed as the CBHArgs.
 * @param slPtr
 * @param CBHandle The call back function that would be called inside traverse.
 * @param CBHArgs The arguments to the call back handler.
 * @param node The node from which traversal starts.
 * @return Node that is returned by the call back function.
 */
ds_packetContainer *
ds_sl_traverse (ds_slist slPtr, CBHandleType CBHandle, void *CBHArgs,
                ds_packetContainer * node)
{
  return ds_traverse (&slPtr->base, CBHandle, CBHArgs, node, DS_RIGHT);
}

/**
 * Search the data structure.
 * @param slPtr
 * @param CBHandle The call back function that would be called for search.
 * The search call back function would check the passed's key and compare
 * with the elements inside the data structure.
 * @return Node that is returned by the call back function.
 */
ds_packetContainer *
ds_sl_search (ds_slist slPtr, int key, CBHandleType CBHandle)
{
  return ds_search (&slPtr->base, key, CBHandle);
}

/**
 * Initialize object. The base init function is invoked and register data
 * structure. Memory is allocated here for the object.
 * @param clPtr Object reference.
 * @param mObj Reference of the memory object that will be used in the
 * memory allocation. If memory is not available then the appropriate
 * \c error-code is returned.
 * @return The \c error-code if any error during allocation of memory else
 * success is returned.
 */
genErr_t
ds_cl_init (ds_clist * clPtr, bs_mmodCls mObj)
{
  genErr_t retVal;
  void *ptr = NULL;

  if(clPtr == NULL)
    return INVALID_MEM_LOC;
  *clPtr = NULL;

  retVal = bs_allocMem (mObj, sizeof (struct ds_clistType), &ptr);
  if (retVal != SUCCESS)
    return retVal;
  (*clPtr) = (ds_clist) ptr;

  return ds_dsBaseInit (&((*clPtr)->base), DS_DLIST);
}

/**
 * Finalize the object. The base finalize function is invoked.
 * Memory will be freed for the object inside this.
 * @param clPtr Reference of the object.
 * @param mObj Reference of the memory object that will be used for the memory
 * operations.
 * @return The \c error-code if any error during memory operations else
 * success is returned.
 */
genErr_t
ds_cl_fin (ds_clist * clPtr, bs_mmodCls mObj)
{
  genErr_t retVal;

  if(clPtr == NULL)
    return INVALID_MEM_LOC;

  retVal = ds_dsBaseFin (&((*clPtr)->base));
  if (retVal != SUCCESS)
    return retVal;

  retVal = bs_freeMem (mObj, (void *) clPtr);

  return retVal;
}

/**
 * Return empty status.
 * @param clPtr
 * @return The value \c True is returned if the ds is non-empty, Else \c false
 * is returned.
 */
t_bool
ds_cl_is_empty (ds_clist clPtr)
{
  return ds_isEmpty (&clPtr->base);
}

/**
 * Return the count.
 * @param clPtr
 * @return number of elements in the data structure.
 */
unsigned short
ds_cl_get_count (ds_clist clPtr)
{
  return ds_getCount (&clPtr->base);
}

/**
 * Set the element limit.
 * @param clPtr
 * @return The limit value that will be set for the data structure.
 */
genErr_t
ds_cl_limit (ds_clist clPtr, unsigned short element_limit)
{
  return ds_setElementLimit (&clPtr->base, element_limit);
}

/**
 * Insert the packet.
 * The packet container needs to be initialised with data before this.
 * @param clPtr
 * @param data The packet container.
 * @param node The packet container node selected for insertion.
 * @param dir The direction of insertion.
 * @return The \c error-code if any error during memory operations else
 * success is returned.
 */
genErr_t
ds_cl_insert (ds_clist clPtr, ds_packetContainer * data,
              ds_packetContainer * node)
{
  return ds_insert (&clPtr->base, data, node, DS_RIGHT);
}

/**
 * Remove packet.
 * The packet container that is removed is returned. Memory for this packet
 * container needs to be freed elsewhere.
 * @param clPtr
 * @param node. The node that needs to be removed.
 * @return The packet container is returned.
 */
ds_packetContainer *
ds_cl_remove (ds_clist clPtr, ds_packetContainer * node, ds_e_headTail htail)
{
  return ds_remove (&clPtr->base, node, htail);
}

/**
 * Clear the data structure.
 * The packet container is freed using the memory object. If the memory object
 * is NULL then the packet container memory is not freed.
 * container needs to be freed elsewhere.
 * @param clPtr
 * @param mObj The memory object reference that will be used for freeing the
 * packet containers in the data structure.
 * @return The \c error-code if any error during memory operations else
 * success is returned.
 */
genErr_t
ds_cl_clear (ds_clist clPtr, bs_mmodCls mObj)
{
  return ds_clear (&clPtr->base, mObj);
}

/**
 * Traverse the data structure.
 * The callback function returns either a node or null. If a node is returned
 * the traversal function stops. Additional arguments to the call back
 * hancler can be passed as the CBHArgs.
 * @param clPtr
 * @param CBHancle The call back function that would be called inside traverse.
 * @param CBHArgs The arguments to the call back hancler.
 * @param node The node from which traversal starts.
 * @param dir The of traversal.
 * @return Node that is returned by the call back function.
 */
ds_packetContainer *
ds_cl_traverse (ds_clist clPtr, CBHandleType CBHandle, void *CBHArgs,
                ds_packetContainer * node)
{
  return ds_traverse (&clPtr->base, CBHandle, CBHArgs, node, DS_RIGHT);
}

/**
 * Search the data structure.
 * @param clPtr
 * @param CBHancle The call back function that would be called for search.
 * The search call back function would check the passed's key and compare
 * with the elements inside the data structure.
 * @return Node that is returned by the call back function.
 */
ds_packetContainer *
ds_cl_search (ds_clist clPtr, int key, CBHandleType CBHandle)
{
  return ds_search (&clPtr->base, key, CBHandle);
}

/**
 * Initialize object. The base init function is invoked and register data
 * structure. Memory is allocated here for the object.
 * @param dlPtr Object reference.
 * @param mObj Reference of the memory object that will be used in the
 * memory allocation. If memory is not available then the appropriate
 * \c error-code is returned.
 * @return The \c error-code if any error during allocation of memory else
 * success is returned.
 */
genErr_t
ds_dl_init (ds_dlist * dlPtr, bs_mmodCls mObj)
{
  genErr_t retVal;
  void *ptr = NULL;

  if(dlPtr == NULL)
    return INVALID_MEM_LOC;
  *dlPtr = NULL;

  retVal = bs_allocMem (mObj, sizeof (struct ds_dlistType), &ptr);
  if (retVal != SUCCESS)
    return retVal;
  (*dlPtr) = (ds_dlist) ptr;

  return ds_dsBaseInit (&((*dlPtr)->base), DS_DLIST);
}

/**
 * Finalize the object. The base finalize function is invoked.
 * Memory will be freed for the object inside this.
 * @param dlPtr Reference of the object.
 * @param mObj Reference of the memory object that will be used for the memory
 * operations.
 * @return The \c error-code if any error during memory operations else
 * success is returned.
 */
genErr_t
ds_dl_fin (ds_dlist * dlPtr, bs_mmodCls mObj)
{
  genErr_t retVal;

  if(dlPtr == NULL)
    return INVALID_MEM_LOC;

  retVal = ds_dsBaseFin (&((*dlPtr)->base));
  if (retVal != SUCCESS)
    return retVal;

  retVal = bs_freeMem (mObj, (void *) dlPtr);

  return retVal;
}

/**
 * Return empty status.
 * @param dlPtr
 * @return The value \c True is returned if the ds is non-empty, Else \c false
 * is returned.
 */
t_bool
ds_dl_is_empty (ds_dlist dlPtr)
{
  return ds_isEmpty (&dlPtr->base);
}

/**
 * Return the count.
 * @param dlPtr
 * @return number of elements in the data structure.
 */
unsigned short
ds_dl_get_count (ds_dlist dlPtr)
{
  return ds_getCount (&dlPtr->base);
}

/**
 * Set the element limit.
 * @param dlPtr
 * @return The limit value that will be set for the data structure.
 */
genErr_t
ds_dl_limit (ds_dlist dlPtr, unsigned short element_limit)
{
  return ds_setElementLimit (&dlPtr->base, element_limit);
}

/**
 * Insert the packet.
 * The packet container needs to be initialised with data before this.
 * @param dlPtr
 * @param data The packet container.
 * @param node The packet container node selected for insertion.
 * @param dir The direction of insertion.
 * @return The \c error-code if any error during memory operations else
 * success is returned.
 */
genErr_t
ds_dl_insert (ds_dlist dlPtr, ds_packetContainer * data,
              ds_packetContainer * node, ds_e_direction dir)
{
  return ds_insert (&dlPtr->base, data, node, dir);
}

/**
 * Remove packet.
 * The packet container that is removed is returned. Memory for this packet
 * container needs to be freed elsewhere.
 * @param dlPtr
 * @param node. The node that needs to be removed.
 * @return The packet container is returned.
 */
ds_packetContainer *
ds_dl_remove (ds_dlist dlPtr, ds_packetContainer * node, ds_e_headTail htail)
{
  return ds_remove (&dlPtr->base, node, htail);
}

/**
 * Clear the data structure.
 * The packet container is freed using the memory object. If the memory object
 * is NULL then the packet container memory is not freed.
 * container needs to be freed elsewhere.
 * @param dlPtr
 * @param mObj The memory object reference that will be used for freeing the
 * packet containers in the data structure.
 * @return The \c error-code if any error during memory operations else
 * success is returned.
 */
genErr_t
ds_dl_clear (ds_dlist dlPtr, bs_mmodCls mObj)
{
  return ds_clear (&dlPtr->base, mObj);
}

/**
 * Traverse the data structure.
 * The callback function returns either a node or null. If a node is returned
 * the traversal function stops. Additional arguments to the call back
 * handler can be passed as the CBHArgs.
 * @param dlPtr
 * @param CBHandle The call back function that would be called inside traverse.
 * @param CBHArgs The arguments to the call back handler.
 * @param node The node from which traversal starts.
 * @param dir The of traversal.
 * @return Node that is returned by the call back function.
 */
ds_packetContainer *
ds_dl_traverse (ds_dlist dlPtr, CBHandleType CBHandle, void *CBHArgs,
                ds_packetContainer * node, ds_e_direction dir)
{
  return ds_traverse (&dlPtr->base, CBHandle, CBHArgs, node, dir);
}

/**
 * Search the data structure.
 * @param dlPtr
 * @param CBHandle The call back function that would be called for search.
 * The search call back function would check the passed's key and compare
 * with the elements inside the data structure.
 * @return Node that is returned by the call back function.
 */
ds_packetContainer *
ds_dl_search (ds_dlist dlPtr, int key, CBHandleType CBHandle)
{
  return ds_search (&dlPtr->base, key, CBHandle);
}

/**
 * Initialize object. The base init function is invoked and register data
 * structure. Memory is allocated here for the object.
 * @param cdPtr Object reference.
 * @param mObj Reference of the memory object that will be used in the
 * memory allocation. If memory is not available then the appropriate
 * \c error-code is returned.
 * @return The \c error-code if any error during allocation of memory else
 * success is returned.
 */
genErr_t
ds_cd_init (ds_cdlist * cdPtr, bs_mmodCls mObj)
{
  genErr_t retVal;
  void *ptr = NULL;

  if(cdPtr == NULL)
    return INVALID_MEM_LOC;
  *cdPtr = NULL;

  retVal = bs_allocMem (mObj, sizeof (struct ds_cdlistType), &ptr);
  if (retVal != SUCCESS)
    return retVal;
  (*cdPtr) = (ds_cdlist) ptr;

  return ds_dsBaseInit (&((*cdPtr)->base), DS_CQUEUE);
}

/**
 * Finalize the object. The base finalize function is invoked.
 * Memory will be freed for the object inside this.
 * @param cdPtr Reference of the object.
 * @param mObj Reference of the memory object that will be used for the memory
 * operations.
 * @return The \c error-code if any error during memory operations else
 * success is returned.
 */
genErr_t
ds_cd_fin (ds_cdlist * cdPtr, bs_mmodCls mObj)
{
  genErr_t retVal;

  if(cdPtr == NULL)
    return INVALID_MEM_LOC;

  retVal = ds_dsBaseFin (&((*cdPtr)->base));
  if (retVal != SUCCESS)
    return retVal;

  retVal = bs_freeMem (mObj, (void *) cdPtr);

  return retVal;
}

/**
 * Return empty status.
 * @param cdPtr
 * @return The value \c True is returned if the ds is non-empty, Else \c false
 * is returned.
 */
t_bool
ds_cd_is_empty (ds_cdlist cdPtr)
{
  return ds_isEmpty (&cdPtr->base);
}

/**
 * Return the count.
 * @param cdPtr
 * @return number of elements in the data structure.
 */
unsigned short
ds_cd_get_count (ds_cdlist cdPtr)
{
  return ds_getCount (&cdPtr->base);
}

/**
 * Set the element limit.
 * @param cdPtr
 * @return The limit value that will be set for the data structure.
 */
genErr_t
ds_cd_limit (ds_cdlist cdPtr, unsigned short element_limit)
{
  return ds_setElementLimit (&cdPtr->base, element_limit);
}

/**
 * Insert the packet.
 * The packet container needs to be initialised with data before this.
 * @param cdPtr
 * @param data The packet container.
 * @param node The packet container node selected for insertion.
 * @param dir The direction of insertion.
 * @return The \c error-code if any error during memory operations else
 * success is returned.
 */
genErr_t
ds_cd_insert (ds_cdlist cdPtr, ds_packetContainer * data,
              ds_packetContainer * node, ds_e_direction dir)
{
  return ds_insert (&cdPtr->base, data, node, dir);
}

/**
 * Remove packet.
 * The packet container that is removed is returned. Memory for this packet
 * container needs to be freed elsewhere.
 * @param cdPtr
 * @return The packet container is returned.
 */
ds_packetContainer *
ds_cd_remove (ds_cdlist cdPtr, ds_packetContainer * node, ds_e_headTail htail)
{
  return ds_remove (&cdPtr->base, node, htail);
}

/**
 * Clear the data structure.
 * The packet container is freed using the memory object. If the memory object
 * is NULL then the packet container memory is not freed.
 * container needs to be freed elsewhere.
 * @param cdPtr
 * @param mObj The memory object reference that will be used for freeing the
 * packet containers in the data structure.
 * @return The \c error-code if any error during memory operations else
 * success is returned.
 */
genErr_t
ds_cd_clear (ds_cdlist cdPtr, bs_mmodCls mObj)
{
  return ds_clear (&cdPtr->base, mObj);
}

/**
 * Traverse the data structure.
 * The callback function returns either a node or null. If a node is returned
 * the traversal function stops. Additional arguments to the call back
 * hancder can be passed as the CBHArgs.
 * @param cdPtr
 * @param CBHandle The call back function that would be called inside traverse.
 * @param CBHArgs The arguments to the call back hancder.
 * @return Node that is returned by the call back function.
 */
ds_packetContainer *
ds_cd_traverse (ds_cdlist cdPtr, CBHandleType CBHandle, void *CBHArgs,
                ds_packetContainer * node, ds_e_direction dir)
{
  return ds_traverse (&cdPtr->base, CBHandle, CBHArgs, node, dir);
}

/**
 * Search the data structure.
 * @param cdPtr
 * @param CBHandle The call back function that would be called for search.
 * The search call back function would check the passed's key and compare
 * with the elements inside the data structure.
 * @return Node that is returned by the call back function.
 */
ds_packetContainer *
ds_cd_search (ds_cdlist cdPtr, int key, CBHandleType CBHandle)
{
  return ds_search (&cdPtr->base, key, CBHandle);
}

/*Non linear ds*/

/**
 * Initialize object. The base init function is invoked and register data
 * structure. Memory is allocated here for the object.
 * @param cdPtr Object reference.
 * @param mObj Reference of the memory object that will be used in the
 * memory allocation. If memory is not available then the appropriate
 * \c error-code is returned.
 * @return The \c error-code if any error during allocation of memory else
 * success is returned.
 */
genErr_t
ds_bst_init (ds_bst * bstPtr, bs_mmodCls mObj)
{
  genErr_t retVal;
  void *ptr = NULL;

  if(bstPtr == NULL)
    return INVALID_MEM_LOC;
  *bstPtr = NULL;

  retVal = bs_allocMem (mObj, sizeof (struct ds_bstType), &ptr);
  if (retVal != SUCCESS)
    return retVal;
  (*bstPtr) = (ds_bst) ptr;

  return ds_dsBaseInit (&((*bstPtr)->base), DS_BST);
}

/**
 * Finalize the object. The base finalize function is invoked.
 * Memory will be freed for the object inside this.
 * @param bstPtr Reference of the object.
 * @param mObj Reference of the memory object that will be used for the memory
 * operations.
 * @return The \c error-code if any error during memory operations else
 * success is returned.
 */
genErr_t
ds_bst_fin (ds_bst * bstPtr, bs_mmodCls mObj)
{
  genErr_t retVal;

  if(bstPtr == NULL)
    return INVALID_MEM_LOC;

  retVal = ds_dsBaseFin (&((*bstPtr)->base));
  if (retVal != SUCCESS)
    return retVal;

  retVal = bs_freeMem (mObj, (void *) bstPtr);

  return retVal;
}

/**
 * Return empty status.
 * @param bstPtr
 * @return The value \c True is returned if the ds is non-empty, Else \c false
 * is returned.
 */
t_bool
ds_bst_is_empty (ds_bst bstPtr)
{
  return ds_isEmpty (&bstPtr->base);
}

/**
 * Return the count.
 * @param bstPtr
 * @return number of elements in the data structure.
 */
unsigned short
ds_bst_get_count (ds_bst bstPtr)
{
  return ds_getCount (&bstPtr->base);
}

/**
 * Set the element limit.
 * @param bstPtr
 * @return The limit value that will be set for the data structure.
 */
genErr_t
ds_bst_limit (ds_bst bstPtr, unsigned short element_limit)
{
  return ds_setElementLimit (&bstPtr->base, element_limit);
}

/**
 * Insert the packet.
 * The packet container needs to be initialised with data before this.
 * @param bstPtr
 * @param data The packet container.
 * @param node The packet container node selected for insertion.
 * @return The \c error-code if any error during memory operations else
 * success is returned.
 */
genErr_t
ds_bst_insert (ds_bst bstPtr, ds_packetContainer * data)
{
  return ds_insertT (&bstPtr->base, data);
}

/**
 * Remove packet.
 * The packet container that is removed is returned. Memory for this packet
 * container needs to be freed elsewhere.
 * @param bstPtr
 * @return The packet container is returned.
 */
ds_packetContainer *
ds_bst_remove (ds_bst bstPtr, ds_packetContainer * node)
{
  return ds_removeT (&bstPtr->base, node);
}

/**
 * Clear the data structure.
 * The packet container is freed using the memory object. If the memory object
 * is NULL then the packet container memory is not freed.
 * container needs to be freed elsewhere.
 * @param bstPtr
 * @param node The node from which the clear operation should be done.
 * @param mObj The memory object reference that will be used for freeing the
 * packet containers in the data structure.
 * @return The \c error-code if any error during memory operations else
 * success is returned.
 */
genErr_t
ds_bst_clear (ds_bst bstPtr, ds_packetContainer *node, bs_mmodCls mObj)
{
  return ds_clearT (&bstPtr->base, node, mObj);
}

/**
 * Traverse the data structure.
 * The callback function returns either a node or null. If a node is returned
 * the traversal function stops. Additional arguments to the call back
 * handler can be passed as the CBHArgs.
 * @param bstPtr
 * @param CBHandle The call back function that would be called inside traverse.
 * @param CBHArgs The arguments to the call back hanbster.
 * @param dir is the traversal order (i.e inorder, post order or pre-order).
 * @return Node that is returned by the call back function.
 */
ds_packetContainer *
ds_bst_traverse (ds_bst bstPtr, CBHandleType CBHandle, void *CBHArgs,
                 ds_packetContainer * node, ds_e_trav_dir dir)
{
  return ds_traverseT (&bstPtr->base, CBHandle, CBHArgs, node, dir);
}

/**
 * Search the data structure.
 * @param bstPtr
 * @param CBHandle The call back function that would be called for search.
 * The search call back function would check the passed's key and compare
 * with the elements inside the data structure.
 * @return Node that is returned by the call back function.
 */
ds_packetContainer *
ds_bst_search (ds_bst bstPtr, int key, CBHandleType CBHandle, ds_e_trav_dir dir)
{
  return ds_searchT (&bstPtr->base, key, CBHandle, dir);
}

/**
 * Initialize object. The base init function is invoked and register data
 * structure. Memory is allocated here for the object.
 * @param cdPtr Object reference.
 * @param mObj Reference of the memory object that will be used in the
 * memory allocation. If memory is not available then the appropriate
 * \c error-code is returned.
 * @return The \c error-code if any error during allocation of memory else
 * success is returned.
 */
genErr_t
ds_avl_init (ds_avl * avlPtr, bs_mmodCls mObj)
{
  genErr_t retVal;
  void *ptr = NULL;

  if(avlPtr == NULL)
    return INVALID_MEM_LOC;
  *avlPtr = NULL;

  retVal = bs_allocMem (mObj, sizeof (struct ds_avlType), &ptr);
  if (retVal != SUCCESS)
    return retVal;
  (*avlPtr) = (ds_avl) ptr;

  return ds_dsBaseInit (&((*avlPtr)->base), DS_AVL);
}

/**
 * Finalize the object. The base finalize function is invoked.
 * Memory will be freed for the object inside this.
 * @param avlPtr Reference of the object.
 * @param mObj Reference of the memory object that will be used for the memory
 * operations.
 * @return The \c error-code if any error during memory operations else
 * success is returned.
 */
genErr_t
ds_avl_fin (ds_avl * avlPtr, bs_mmodCls mObj)
{
  genErr_t retVal;

  if(avlPtr == NULL)
    return INVALID_MEM_LOC;

  retVal = ds_dsBaseFin (&((*avlPtr)->base));
  if (retVal != SUCCESS)
    return retVal;

  retVal = bs_freeMem (mObj, (void *) avlPtr);

  return retVal;
}

/**
 * Return empty status.
 * @param avlPtr
 * @return The value \c True is returned if the ds is non-empty, Else \c false
 * is returned.
 */
t_bool
ds_avl_is_empty (ds_avl avlPtr)
{
  return ds_isEmpty (&avlPtr->base);
}

/**
 * Return the count.
 * @param avlPtr
 * @return number of elements in the data structure.
 */
unsigned short
ds_avl_get_count (ds_avl avlPtr)
{
  return ds_getCount (&avlPtr->base);
}

/**
 * Set the element limit.
 * @param avlPtr
 * @return The limit value that will be set for the data structure.
 */
genErr_t
ds_avl_limit (ds_avl avlPtr, unsigned short element_limit)
{
  return ds_setElementLimit (&avlPtr->base, element_limit);
}

/**
 * Insert the packet.
 * The packet container needs to be initialised with data before this.
 * @param avlPtr
 * @param data The packet container.
 * @param node The packet container node selected for insertion.
 * @return The \c error-code if any error during memory operations else
 * success is returned.
 */
genErr_t
ds_avl_insert (ds_avl avlPtr, ds_packetContainer * data)
{
  return ds_insertT (&avlPtr->base, data);
}

/**
 * Remove packet.
 * The packet container that is removed is returned. Memory for this packet
 * container needs to be freed elsewhere.
 * @param avlPtr
 * @return The packet container is returned.
 */
ds_packetContainer *
ds_avl_remove (ds_avl avlPtr, ds_packetContainer * node)
{
  return ds_removeT (&avlPtr->base, node);
}

/**
 * Clear the data structure.
 * The packet container is freed using the memory object. If the memory object
 * is NULL then the packet container memory is not freed.
 * container needs to be freed elsewhere.
 * @param avlPtr
 * @param node The node from which the clear operation should be done.
 * @param mObj The memory object reference that will be used for freeing the
 * packet containers in the data structure.
 * @return The \c error-code if any error during memory operations else
 * success is returned.
 */
genErr_t
ds_avl_clear (ds_avl avlPtr, ds_packetContainer *node, bs_mmodCls mObj)
{
  return ds_clearT (&avlPtr->base, node, mObj);
}

/**
 * Traverse the data structure.
 * The callback function returns either a node or null. If a node is returned
 * the traversal function stops. Additional arguments to the call back
 * handler can be passed as the CBHArgs.
 * @param avlPtr
 * @param CBHandle The call back function that would be called inside traverse.
 * @param CBHArgs The arguments to the call back hanavler.
 * @param dir is the traversal order (i.e inorder, post order or pre-order).
 * @return Node that is returned by the call back function.
 */
ds_packetContainer *
ds_avl_traverse (ds_avl avlPtr, CBHandleType CBHandle, void *CBHArgs,
                 ds_packetContainer * node, ds_e_trav_dir dir)
{
  return ds_traverseT (&avlPtr->base, CBHandle, CBHArgs, node, dir);
}

/**
 * Search the data structure.
 * @param avlPtr
 * @param CBHandle The call back function that would be called for search.
 * The search call back function would check the passed's key and compare
 * with the elements inside the data structure.
 * @return Node that is returned by the call back function.
 */
ds_packetContainer *
ds_avl_search (ds_avl avlPtr, int key, CBHandleType CBHandle, ds_e_trav_dir dir)
{
  return ds_searchT (&avlPtr->base, key, CBHandle, dir);
}

/*debugging*/

/**
 * print tree.
 * @param bstPtr
 * @param pchar
 * @param indent
 * @return Node that is returned by the call back function.
 */
void ds_prettyPrint (ds_bst bstPtr, char pchar, int indent)
{
  ds_prettyPrintT (&bstPtr->base,  NULL, pchar, indent);
}

/****************************************************************************/
