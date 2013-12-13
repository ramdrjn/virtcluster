/**
 * @file dsbase.c
 * Contains base implementations for the data structures.
 * @author RD
 * @date Sun Jan 16 22:23:41 IST 2011
 */

#include "_dsbase.h"

/*Internal prototypes*/
PRIVATE inline void ds_setCircular (ds_dsBase * dsPtr);
PRIVATE inline void ds_clearCircular (ds_dsBase * dsPtr);
PRIVATE inline t_bool ds_getCircular (ds_dsBase * dsPtr);
PRIVATE inline ds_packetContainer *ds_getHeadPtr (ds_dsBase * dsPtr);
PRIVATE inline ds_packetContainer *ds_getTailPtr (ds_dsBase * dsPtr);
PRIVATE inline genErr_t ds_setHeadPtr (ds_dsBase * dsPtr,
                                       ds_packetContainer * headPtr);
PRIVATE inline genErr_t ds_setTailPtr (ds_dsBase * dsPtr,
                                       ds_packetContainer * tailPtr);
PRIVATE inline genErr_t ds_incCount (ds_dsBase * dsPtr);
PRIVATE inline genErr_t ds_decCount (ds_dsBase * dsPtr);
PRIVATE inline genErr_t ds_registerType (ds_dsBase * dsPtr, ds_e_dsType type);
PRIVATE inline ds_packetContainer *ds_searchCBFunc (void *arg,
                                                    ds_packetContainer *
                                                    node);
PRIVATE inline ds_packetContainer *ds_doDLRotate (ds_packetContainer * node,
                                                  ds_packetContainer *
                                                  sucNode);
PRIVATE inline ds_packetContainer *ds_doDRRotate (ds_packetContainer * node,
                                                  ds_packetContainer *
                                                  sucNode);
PRIVATE inline ds_packetContainer *ds_doLRotate (ds_packetContainer * node,
                                                 ds_packetContainer *
                                                 sucNode);
PRIVATE inline ds_packetContainer *ds_doRRotate (ds_packetContainer * node,
                                                 ds_packetContainer *
                                                 sucNode);
PRIVATE inline genErr_t ds_adjustBalance (ds_dsBase * dsPtr,
                                          ds_packetContainer * node,
                                          int balanceVal, ds_e_opType opType);
PRIVATE inline ds_packetContainer *processNodeT (ds_dsBase * dsPtr, CBHandleType CBHandle, void *CBHArgs, ds_packetContainer * node);
PRIVATE inline ds_packetContainer * ds_searchCBFuncT (void *arg, ds_packetContainer * node);

/**
 * Initialize the base. Also register the type of the data structure.
 * @note NO memory allocation is done here.
 * @param dsPtr base object reference.
 * @param type Type of the datastructure.
 * @return The \c error-code else success is returned.
 */
inline genErr_t
ds_dsBaseInit (ds_dsBase * dsPtr, ds_e_dsType type)
{
  dsPtr->_validFlag = true;

  dsPtr->elementLimit = MAX_DS_VALUES;

  ds_registerType (dsPtr, type);

  return SUCCESS;
}

/**
 * Finalize the base object. The valid flag is unset.
 * @note No memory will be freed here.
 * @param dsPtr Reference of the object.
 * @return The \c error-code else success is returned.
 */
inline genErr_t
ds_dsBaseFin (ds_dsBase * dsPtr)
{
  validateObj (dsPtr);

  dsPtr->_validFlag = false;

  return SUCCESS;
}

/**
 * Return empty status.
 * @param dsPtr
 * @return \c true if the ds is non-empty, else \c false.
 */
inline t_bool
ds_isEmpty (ds_dsBase * dsPtr)
{
  validateObj (dsPtr);
  return ((dsPtr->count == 0) ? true : false);
}

/**
 * Return the total number of elements in the DS.
 * @param dsPtr
 * @return The number of elements in the DS.
 */
inline unsigned short
ds_getCount (ds_dsBase * dsPtr)
{
  validateObj (dsPtr);
  return dsPtr->count;
}

/**
 * Increment the number of elements in the DS.
 * @param dsPtr
 * @return The \c error-code else success is returned.
 */
PRIVATE inline genErr_t
ds_incCount (ds_dsBase * dsPtr)
{
  dsPtr->count += 1;

  return SUCCESS;
}

/**
 * Decrement the number of elements in the DS.
 * @param dsPtr
 * @return The \c error-code else success is returned.
 */
PRIVATE inline genErr_t
ds_decCount (ds_dsBase * dsPtr)
{
  dsPtr->count -= 1;

  if (dsPtr->count == 0)
    {
      ds_setHeadPtr (dsPtr, NULL);
      ds_setTailPtr (dsPtr, NULL);
    }

  return SUCCESS;
}

/**
 * Set the circular flag.
 * @param dsPtr
 * @return Nothing
 */
PRIVATE inline void
ds_setCircular (ds_dsBase * dsPtr)
{
  dsPtr->circular = true;
}

/**
 * Clear the circular flag.
 * @param dsPtr
 * @return Nothing
 */
PRIVATE inline void
ds_clearCircular (ds_dsBase * dsPtr)
{
  dsPtr->circular = false;
}

/**
 * Get the circular flag.
 * @param dsPtr
 * @return Circular flag status
 */
PRIVATE inline t_bool
ds_getCircular (ds_dsBase * dsPtr)
{
  return dsPtr->circular;
}

/**
 * Get the head pointer.
 * @param dsPtr
 * @return The packet container that is the head pointer for the DS.
 */
PRIVATE inline ds_packetContainer *
ds_getHeadPtr (ds_dsBase * dsPtr)
{
  return dsPtr->headPtr;
}

/**
 * Get the tail pointer.
 * @param dsPtr
 * @return The packet container that is the tail pointer for the DS.
 */
PRIVATE inline ds_packetContainer *
ds_getTailPtr (ds_dsBase * dsPtr)
{
  return dsPtr->tailPtr;
}

/**
 * Set the head pointer.
 * @param dsPtr
 * @param headPtr
 * @return Sets the packet container as the head pointer for the DS.
 */
PRIVATE inline genErr_t
ds_setHeadPtr (ds_dsBase * dsPtr, ds_packetContainer * headPtr)
{
  dsPtr->headPtr = headPtr;
  return SUCCESS;
}

/**
 * Set the tail pointer.
 * @param dsPtr
 * @param tailPtr
 * @return Sets the packet container as the tail pointer for the DS.
 */
PRIVATE inline genErr_t
ds_setTailPtr (ds_dsBase * dsPtr, ds_packetContainer * tailPtr)
{
  dsPtr->tailPtr = tailPtr;
  return SUCCESS;
}

/**
 * Register the type of the data structure.
 * @param dsPtr
 * @param ds_e_dsType
 * @return The \c error-code if any error during memory operations else
 * success is returned.
 */
PRIVATE inline genErr_t
ds_registerType (ds_dsBase * dsPtr, ds_e_dsType type)
{
  dsPtr->type = type;

  if ((type == DS_CQUEUE) || (type == DS_CLIST) || (type == DS_CDLIST))
    ds_setCircular (dsPtr);
  else
    ds_clearCircular (dsPtr);

  return SUCCESS;
}

/**
 * Insert the packet container node into the DS.
 * @param dsPtr
 * @param data The data that needs to be inserted.
 * @param node The node after which the insertion is done. If this is Null
 * then the data is pushed to the last <tail> of the ds.
 * @param dir Left or right insertion to the node.
 * @return The \c error-code if any error during memory operations else
 * success is returned.
 */
inline genErr_t
ds_insert (ds_dsBase * dsPtr, ds_packetContainer * data,
           ds_packetContainer * node, ds_e_direction dir)
{
  ds_packetContainer *tnxt = NULL;

  validateObj (dsPtr);

  if (data == NULL)
    return INVALID_MEM_LOC;

  (dir != DS_LEFT) ? true : (dir != DS_RIGHT) ? true : assert (0);

  if (ds_getCount (dsPtr) == dsPtr->elementLimit)
    return DATASTRUCT_FULL;

  if (ds_isEmpty (dsPtr) == true)
    {
      ds_setHeadPtr (dsPtr, data);
      ds_setTailPtr (dsPtr, data);
      if (ds_getCircular (dsPtr) == true)
        {
          ds_setNextPtr (data, data);
          ds_setPrevPtr (data, data);
        }
      else
        {
          ds_setNextPtr (data, NULL);
          ds_setPrevPtr (data, NULL);
        }
    }
  else
    {
      if (node == NULL)
        node = ds_getTailPtr (dsPtr);

      if (node == NULL)
        assert (0);

      if (dir == DS_LEFT)
        {
          //Prev left
          tnxt = ds_getPrevPtr (node);
          ds_setPrevPtr (node, data);
          ds_setNextPtr (data, node);
          ds_setPrevPtr (data, tnxt);
          if (tnxt != NULL)
            ds_setNextPtr (tnxt, data);
          if (node == ds_getHeadPtr (dsPtr))
            ds_setHeadPtr (dsPtr, data);
        }
      else
        {
          //Next right.
          tnxt = ds_getNextPtr (node);
          ds_setNextPtr (node, data);
          ds_setPrevPtr (data, node);
          ds_setNextPtr (data, tnxt);
          if (tnxt != NULL)
            ds_setPrevPtr (tnxt, data);
          if (node == ds_getTailPtr (dsPtr))
            ds_setTailPtr (dsPtr, data);
        }
    }

  ds_incCount (dsPtr);

  return SUCCESS;
}

/**
 * Remove the packet container node from the DS. Memory is not freed for the
 * packet container.
 * @param dsPtr
 * @param node The node which will be removed.
 * @param htail Implies whether to remove the head or the tail.
 * @return The node is returned else NULL in case of error.
 */
inline ds_packetContainer *
ds_remove (ds_dsBase * dsPtr, ds_packetContainer * node, ds_e_headTail htail)
{
  ds_packetContainer *tnxt = NULL;
  ds_packetContainer *tprev = NULL;

  validateObj (dsPtr);

  if (ds_isEmpty (dsPtr) == true)
    return NULL;

  if (node == NULL)
    {
      if (htail == DS_HEAD)
        node = ds_getHeadPtr (dsPtr);
      else if (htail == DS_TAIL)
        node = ds_getTailPtr (dsPtr);
      else
        assert (0);
    }

  if (node == NULL)
    assert (0);

  tnxt = ds_getNextPtr (node);
  tprev = ds_getPrevPtr (node);
  if (tnxt != NULL)
    ds_setPrevPtr (tnxt, tprev);
  if (tprev != NULL)
    ds_setNextPtr (tprev, tnxt);
  if (node == ds_getTailPtr (dsPtr))
    ds_setTailPtr (dsPtr, tprev);
  if (node == ds_getHeadPtr (dsPtr))
    ds_setHeadPtr (dsPtr, tnxt);

  ds_decCount (dsPtr);

  return node;
}

/**
 * Clear removes the node starting from the head.
 * The mObj should be a valid object. This would be the one that would be used
 * for the object finish. The mObj for the data struct creation might be
 * different from the mObj for the packet containers.
 * @note If flexibility is required then the remove function needs to
 * register.
 * @param dsPtr
 * @param mObj The memory object that will be used for packet container finish.
 * @return The \c error-code if any error during memory operations else
 * success is returned.
 */
inline genErr_t
ds_clear (ds_dsBase * dsPtr, bs_mmodCls mObj)
{
  ds_packetContainer *tData = NULL;

  validateObj (dsPtr);

  while (!ds_isEmpty (dsPtr))
    {
      tData = ds_remove (dsPtr, 0, DS_HEAD);
      if (mObj != NULL)
        {
          ds_packetContainerFin (tData);
          bs_freeMem (mObj, (void **) &tData);
        }
    }

  return SUCCESS;
}

/**
 * Traverse the data structure.
 * @param dsPtr
 * @param CBHandle The call back function that would be called inside traverse.
 * @param CBHArgs The arguments to the call back handler.
 * @param travNode The node from which traversal will start. If this is NULL
 * the traversal will start from either the head or the tail, depending on dir.
 * @param dir Direction of traversal.
 * @return Node that is returned by the call back function.
 */
inline ds_packetContainer *
ds_traverse (ds_dsBase * dsPtr, CBHandleType CBHandle, void *CBHArgs,
             ds_packetContainer * travNode, ds_e_direction dir)
{
  ds_packetContainer *resNode = NULL;
  ds_packetContainer *sentinel = NULL;

  validateObj (dsPtr);

  resNode = NULL;

  if (CBHandle == NULL)
    assert (0);

  if (travNode == NULL)
    {
      if (dir == DS_RIGHT)
        travNode = ds_getHeadPtr (dsPtr);
      else if (dir == DS_LEFT)
        travNode = ds_getTailPtr (dsPtr);
      else
        assert (0);
    }

  if (ds_getCircular (dsPtr) == true)
    sentinel = travNode;

  do
    {
      /*If the handler wants to return valid node then it should
        return it. It also means to abort the traverse.
        If a NULL is returned it implies that we need to continue. */
      resNode = CBHandle (CBHArgs, travNode);
      if (resNode != NULL)	//Found a valid node hence break.
        break;
      if (dir == DS_RIGHT)
        travNode = ds_getNextPtr (travNode);
      else
        travNode = ds_getPrevPtr (travNode);
    }
  while (travNode != sentinel);

  return resNode;
}

/**
 * Search the data structure with the provided key.
 * @note Provide a search handler else use the default internal handler.
 * @param dsPtr
 * @param Key The key will be used as the criteria for search.
 * @param CBHandle
 * @return The node that matches the key.
 */
inline ds_packetContainer *
ds_search (ds_dsBase * dsPtr, int key, CBHandleType CBHandle)
{
  validateObj (dsPtr);

  if (CBHandle == NULL)
    CBHandle = &ds_searchCBFunc;
  return ds_traverse (dsPtr, CBHandle, (void *) &key, NULL, DS_RIGHT);
}

/**
 * Internal search call back function.
 * @param arg In case of this CB for search this is the key value.
 * @param Node
 * @return Node that matches the key.
 */
PRIVATE inline ds_packetContainer *
ds_searchCBFunc (void *arg, ds_packetContainer * node)
{
  int *key = (int *) arg;

  if (node != NULL)
    {
      int nodeKey;

      nodeKey = ds_getKey (node);
      if (nodeKey == *key)
        return node;
    }
  return NULL;
}

/**
 * Function to set the maximum elements limit that can be held by the
 * data structure.
 * @param dsPtr base object reference.
 * @param elementLimit Maximum number of elements that can be accomdated in the
 * data structure. This is less than MAX_DS_VALUES. This value is first checked
 * and then MAX_DS_VALUES during add operation.
 * @return The \c error-code if any error during operations else
 * success is returned.
 */
inline genErr_t
ds_setElementLimit (ds_dsBase * dsPtr, unsigned short elementLimit)
{
  validateObj (dsPtr);

  if (elementLimit >= MAX_DS_VALUES)
    return INVALID_OPTIONS;

  dsPtr->elementLimit = elementLimit;

  return SUCCESS;
}

/**
 * Tree insert function.
 * @param dsPtr base object reference.
 * @param data The data (packet container) that needs to be inserted.
 * @return The \c error-code if any error during operations else
 * success is returned.
 */
inline genErr_t
ds_insertT (ds_dsBase * dsPtr, ds_packetContainer * data)
{
  ds_packetContainer *tNode = NULL;
  ds_packetContainer *insNode = NULL;

  validateObj (dsPtr);

  if (data == NULL)
    return INVALID_MEM_LOC;

  if (ds_isEmpty (dsPtr) == true)
    {
      ds_setHeadPtr (dsPtr, data);
      ds_setParent (data, NULL);
    }
  else
    {
      int dKey, insKey, balanceFactor;
      ds_e_direction position;

      if (ds_getCount (dsPtr) == dsPtr->elementLimit)
        return DATASTRUCT_FULL;

      insNode = ds_getHeadPtr (dsPtr);
      if (insNode == NULL)
        assert (0);

      do
        {
          dKey = ds_getKey (data);
          insKey = ds_getKey (insNode);
          if (dKey < insKey)
            {
              tNode = ds_getPrevPtr (insNode);
              if (tNode == NULL)
                {
                  position = DS_LEFT;
                  break;
                }
            }
          else if (dKey > insKey)
            {
              tNode = ds_getNextPtr (insNode);
              if (tNode == NULL)
                {
                  position = DS_RIGHT;
                  break;
                }
            }
          else
            {
              return DUPLICATE_DATA;
            }
          insNode = tNode;
        }
      while (insNode != NULL);

      ds_setParent (data, insNode);
      if (position == DS_LEFT)
        {
          //Prev left
          balanceFactor = -1;
          ds_setPrevPtr (insNode, data);
        }
      else
        {
          //Next right.
          balanceFactor = +1;
          ds_setNextPtr (insNode, data);
        }

      if (dsPtr->type == DS_AVL)
        {
          //Perform balance here using parent node only for AVL tree..
          ds_adjustBalance (dsPtr, insNode, balanceFactor, DS_INS);
        }
    }
  ds_incCount (dsPtr);
  return SUCCESS;
}

/**
 * Adjust balance.
 * @param dsPtr base object reference.
 * @param node The node (packet container) from where the balancing starts.
 * @param balanceVal The balance factor after the insertion.
 * @param opType
 * @return The \c error-code if any error during operations else
 * success is returned.
 */
PRIVATE inline genErr_t
ds_adjustBalance (ds_dsBase * dsPtr, ds_packetContainer * node,
                  int balanceVal, ds_e_opType opType)
{
  ds_packetContainer *tnext = NULL;
  ds_packetContainer *tprev = NULL;
  ds_packetContainer *nodeParent = NULL;

  while (node != NULL)
    {
      if (node == ds_getHeadPtr (dsPtr))
        return SUCCESS;

      ds_adjustNodeBalance (node, balanceVal);
      balanceVal = ds_getBalance (node);
      tnext = ds_getNextPtr (node);
      tprev = ds_getPrevPtr (node);

      if (balanceVal == 2)
        {
          //Right heavy
          if (tnext == NULL)
            assert (0);

          if (ds_getBalance (tnext) < 0)
            node = ds_doDLRotate (node, tnext);
          else
            node = ds_doLRotate (node, tnext);

          /*If case of insertion. In this case stop balancing if a node is
            balanced. In case of deletion proceed until the root. */
          if (opType == DS_INS)
            break;
        }
      else if (balanceVal == -2)
        {
          //Left heavy
          if (tprev == NULL)
            assert (0);

          if (ds_getBalance (tprev) > 0)
            node = ds_doDRRotate (node, tprev);
          else
            node = ds_doRRotate (node, tprev);

          /*If case of insertion. In this case stop balancing if a node is
            balanced. In case of deletion proceed until the root. */
          if (opType == DS_INS)
            break;

        }
      else
        {
          //Balanced node.
          if (balanceVal == 0)
            {
              //Insertion
              if (opType == DS_INS)
                break;
            }
        }

      //Continue to check the parent.
      nodeParent = ds_getParent (node);
      if (nodeParent != NULL)
        {
          if (ds_getNextPtr (nodeParent) == node)
            {
              if (opType == DS_INS)
                balanceVal = +1;
              else
                balanceVal = -1;
            }
          else if (ds_getPrevPtr (nodeParent) == node)
            {
              if (opType == DS_INS)
                balanceVal = -1;
              else
                balanceVal = +1;
            }
          else
            assert (0);
        }
      node = nodeParent;
    }
  //Close all the blocks
  return SUCCESS;
}

/**
 * Rotation routines.
 * Succesor becomes the new Root (update parent to succesor link and
 * succesor to parent.
 * Node takes ownership of Sucessors Right child as its Left child.
 * Update the Sucessors Right child for the new parent.
 * Sucessor takes ownership of Node as its Right child.
 * Restore balance for the Node and the Sucessor.
 * Return the succesor as the new root. Use this for further rotations.
 * @param dsPtr base object reference.
 * @param node The node (packet container) from where the balancing starts.
 * @param sucNode
 * @param opType
 * @return Returns the successor as new root.
 */
PRIVATE inline ds_packetContainer *
ds_doRRotate (ds_packetContainer * node, ds_packetContainer * sucNode)
{
  ds_packetContainer *tparent = NULL;
  ds_packetContainer *childNode = NULL;

  tparent = ds_getParent (node);
  //Update the parent's link and the update succesor's parent
  if (tparent != NULL)
    {
      if (ds_getPrevPtr (tparent) == node)
        ds_setPrevPtr (tparent, sucNode);
      else if (ds_getNextPtr (tparent) == node)
        ds_setNextPtr (tparent, sucNode);
      else
        assert (0);
    }
  ds_setParent (sucNode, tparent);
  childNode = ds_getNextPtr (sucNode);
  if (childNode != NULL)
    {
      ds_setParent (childNode, node);
    }
  ds_setPrevPtr (node, childNode);
  ds_setNextPtr (sucNode, node);
  ds_setParent (node, sucNode);
  ds_setBalance (node, 0);
  ds_setBalance (sucNode, 0);
  return sucNode;
}

/**
 * Rotation routines.
 * Sucessor becomes the new Root (update parent to succesor link and
 * succesor to parent link).
 * Node takes ownership of Sucessors left child as its Right child.
 * Update the Sucessors left child for the new parent.
 * Sucessor takes ownership of Node as its left child.
 * Restore balance for the Node and the Successor.
 * Return the succesor as the new root.Use this for further rotations.
 * @param dsPtr base object reference.
 * @param node The node (packet container) from where the balancing starts.
 * @param sucNode
 * @param opType
 * @return Returns the successor as new root.
 */
PRIVATE inline ds_packetContainer *
ds_doLRotate (ds_packetContainer * node, ds_packetContainer * sucNode)
{
  ds_packetContainer *tparent = NULL;
  ds_packetContainer *childNode = NULL;

  tparent = ds_getParent (node);

  //Update the parent's link and the update succesor's parent
  if (tparent != NULL)
    {
      if (ds_getPrevPtr (tparent) == node)
        ds_setPrevPtr (tparent, sucNode);
      else if (ds_getNextPtr (tparent) == node)
        ds_setNextPtr (tparent, sucNode);
      else
        assert (0);
    }
  ds_setParent (sucNode, tparent);
  childNode = ds_getPrevPtr (sucNode);
  if (childNode != NULL)
    {
      ds_setParent (childNode, node);
    }
  ds_setNextPtr (node, childNode);
  ds_setPrevPtr (sucNode, node);
  ds_setParent (node, sucNode);
  ds_setBalance (node, 0);
  ds_setBalance (sucNode, 0);
  return sucNode;
}

/**
 * Double Rotation routines.
 * First do a left rotation for the left subtree
 * and then perform a right rotation for the node.
 * @param dsPtr base object reference.
 * @param node The node (packet container) from where the balancing starts.
 * @param sucNode
 * @return Returns node.
 */
PRIVATE inline ds_packetContainer *
ds_doDRRotate (ds_packetContainer * node, ds_packetContainer * sucNode)
{
  sucNode = ds_doLRotate (sucNode, ds_getNextPtr (sucNode));
  node = ds_doRRotate (node, sucNode);
  return node;
}

/**
 * Double Rotation.
 * First do a right rotation for the right subtree and then perform a left
 * rotation for the node.
 * @param dsPtr base object reference.
 * @param node The node (packet container) from where the balancing starts.
 * @param sucNode
 * @return Returns node.
 */
PRIVATE inline ds_packetContainer *
ds_doDLRotate (ds_packetContainer * node, ds_packetContainer * sucNode)
{
  sucNode = ds_doRRotate (sucNode, ds_getPrevPtr (sucNode));
  node = ds_doLRotate (node, sucNode);
  return node;
}

/* Remove - Use key to remove.*/

/**
 * Remove node and perform rotations.
 * @note removal of the non-empty head node still not handled.
 * @param dsPtr base object reference.
 * @param node The node to be removed.
 * @return The \c error-code if any error during operations else
 * success is returned.
 */
inline ds_packetContainer *
ds_removeT (ds_dsBase * dsPtr, ds_packetContainer * node)
{
  ds_packetContainer *retNode = NULL;
  ds_packetContainer *tnext, *tprev, *tparent;
  t_bool head = false;
  int balanceFactor;

  if (ds_isEmpty (dsPtr))
    return NULL;

  if (node == NULL)
    assert (0);

  tnext = ds_getNextPtr (node);
  tprev = ds_getPrevPtr (node);
  tparent = ds_getParent (node);

  head = (node == ds_getHeadPtr (dsPtr)) ? true : false;

  if ((tparent == NULL) && (!head))
    assert (0);

  if ((tnext == NULL) && (tprev == NULL))
    {
      //If this is the root node then delete this.
      if (head)
        {
          retNode = node;
          return node;
        }

      //Leaf node, with no child.
      if (ds_getPrevPtr (tparent) == node)
        {
          /*As pervious node is getting removed. This
            node would have added a -1. Now since this is getting
            removed we need to add a +1 to the parent node */
          balanceFactor = +1;
          ds_setPrevPtr (tparent, NULL);
        }
      else if (ds_getNextPtr (tparent) == node)
        {
          /*Similarly on adding a node at next would add +1 to
            the node. Since we are removing this node we need to add
            -1 to the parent node. */
          balanceFactor = -1;
          ds_setNextPtr (tparent, NULL);
        }
      else
        {
          assert (0);
        }
      retNode = node;
    }
  if ((tnext == NULL) && (tprev != NULL))
    {
      //If this is the root node then delete this.
      if (head)
        {
          retNode = node;
          ds_setHeadPtr (dsPtr, tprev);
          ds_setParent (tprev, NULL);
          return retNode;
        }

      //Only Left node is present.
      ds_setParent (tprev, ds_getParent (node));
      if (ds_getPrevPtr (tparent) == node)
        {
          balanceFactor = +1;
          ds_setPrevPtr (tparent, tprev);
        }
      else if (ds_getNextPtr (tparent) == node)
        {
          balanceFactor = -1;
          ds_setNextPtr (tparent, tprev);
        }
      else
        {
          assert (0);
        }
      retNode = node;
    }
  if ((tnext != NULL) && (tprev == NULL))
    {
      //If this is the root node then delete this.
      if (head)
        {
          retNode = node;
          ds_setHeadPtr (dsPtr, tnext);
          ds_setParent (tnext, NULL);
          return retNode;
        }

      //Only Right node is present.
      ds_setParent (tnext, ds_getParent (node));
      if (ds_getPrevPtr (tparent) == node)
        {
          balanceFactor = +1;
          ds_setPrevPtr (tparent, tnext);
        }
      else if (ds_getNextPtr (tparent) == node)
        {
          balanceFactor = -1;
          ds_setNextPtr (tparent, tnext);
        }
      else
        {
          assert (0);
        }
      retNode = node;
    }
  if ((tnext != NULL) && (tprev != NULL))
    {
      ds_packetContainer *suc, *sucPar;

      //Both child are present. find inorder successor.
      sucPar = node;
      suc = tprev;
      while (ds_getNextPtr (suc) != NULL)
        {
          sucPar = suc;
          suc = ds_getNextPtr (suc);
        }
      //Delink sucessor from its parent.
      if (ds_getPrevPtr (sucPar) == suc)
        {
          balanceFactor = +1;
          ds_setPrevPtr (sucPar, ds_getPrevPtr (suc));
        }
      else if (ds_getNextPtr (sucPar) == suc)
        {
          balanceFactor = -1;
          ds_setNextPtr (sucPar, ds_getPrevPtr (suc));
        }
      else
        {
          assert (0);
        }

      //Update the nodes details into its sucessor.
      ds_setNextPtr (suc, ds_getNextPtr (node));
      ds_setPrevPtr (suc, ds_getPrevPtr (node));
      ds_setParent (suc, ds_getParent (node));

      //If this is the root node then delete this.
      if (head)
        {
          retNode = node;
          ds_setHeadPtr (dsPtr, tnext);
          ds_setParent (tnext, NULL);
          return retNode;
        }


      //Link the suc with node's parent
      if (ds_getPrevPtr (tparent) == node)
        ds_setPrevPtr (tparent, suc);
      else if (ds_getNextPtr (tparent) == node)
        ds_setNextPtr (tparent, suc);
      else
        {
          assert (0);
        }
      tparent = sucPar;
      retNode = node;
    }

  if (dsPtr->type == DS_AVL)
    {
      ds_adjustBalance (dsPtr, tparent, balanceFactor, 0);
    }

  ds_decCount (dsPtr);
  return retNode;
}

/**
 * Clear the tree.
 * @note recursive operation.
 * @param dsPtr base object reference.
 * @param travNode Node from which the clear operation should start.
 * @param Memory object that will be used for memory freeing.
 * @return The \c error-code if any error during memory operations else
 * success is returned.
 */
inline genErr_t
ds_clearT (ds_dsBase * dsPtr, ds_packetContainer * travNode, bs_mmodCls mObj)
{
  ds_packetContainer *tnode = NULL;

  validateObj (dsPtr);

  if (travNode != NULL)
    {
      ds_clearT (dsPtr, ds_getPrevPtr (travNode), mObj);
      ds_clearT (dsPtr, ds_getNextPtr (travNode), mObj);
      tnode = ds_removeT (dsPtr, travNode);
      if (mObj != NULL)
        {
          bs_freeMem (mObj, (void **) &tnode);
        }
    }
  return SUCCESS;
}

/**
 * Traverse the tree.
 * @note recursive operation.
 * @param dsPtr base object reference.
 * @param CBHandle The call back function that would be called inside traverse.
 * @param CBHArgs The arguments to the call back handler.
 * @param travNode Node from which the traversing should start.
 * @param dir the direction of traversal. For tree its post order, pre order and in order traversal.
 * @return The \c error-code if any error during memory operations else
 * success is returned.
 */
inline ds_packetContainer *
ds_traverseT (ds_dsBase * dsPtr, CBHandleType CBHandle, void *CBHArgs,
              ds_packetContainer * travNode, ds_e_trav_dir dir)
{
  ds_packetContainer *node = NULL;

  validateObj (dsPtr);

  if (travNode != NULL)
    {
      travNode = ds_getHeadPtr(dsPtr);
    }

  //inorder traversal
  if (dir == 0)
    {
      //Left
      ds_traverseT (dsPtr, CBHandle, CBHArgs, ds_getPrevPtr(travNode), dir);
      //Process
      node = processNodeT (dsPtr, CBHandle, CBHArgs, travNode);
      if (node != NULL)
        return node;
      //Right
      ds_traverseT (dsPtr, CBHandle, CBHArgs, ds_getNextPtr(travNode), dir);
    }
  //preorder traversal
  else if (dir == 1)
    {
      //Process
      node = processNodeT (dsPtr, CBHandle, CBHArgs, travNode);
      if (node != NULL)
        return node;
      //Left
      ds_traverseT (dsPtr, CBHandle, CBHArgs, ds_getPrevPtr(travNode), dir);
      //Right
      ds_traverseT (dsPtr, CBHandle, CBHArgs, ds_getNextPtr(travNode), dir);
    }
  //postorder traversal
  else if (dir == 2)
    {
      //Left
      ds_traverseT (dsPtr, CBHandle, CBHArgs, ds_getPrevPtr(travNode), dir);
      //Right
      ds_traverseT (dsPtr, CBHandle, CBHArgs, ds_getNextPtr(travNode), dir);
      //Process
      node = processNodeT (dsPtr, CBHandle, CBHArgs, travNode);
      if (node != NULL)
        return node;
    }
  return NULL;
}

/**
 * Process the node. Call the call back handler for the node.
 * @param dsPtr base object reference.
 * @param CBHandle The call back function that would be processed.
 * @param CBHArgs The arguments to the call back handler.
 * @param node this node is processed with the call back handler.
 * @return The \c error-code if any error during memory operations else
 * success is returned.
 */
PRIVATE inline ds_packetContainer *
processNodeT (ds_dsBase * dsPtr, CBHandleType CBHandle, void *CBHArgs,
              ds_packetContainer * node)
{
  (void)dsPtr;

  if (node == NULL)
    return NULL;

  if (CBHandle == NULL)
    assert (0);

  return CBHandle(CBHArgs, node);
}

/**
 * Search the data structure with the provided key.
 * @note Provide a search handler else use the default internal handler.
 * @param dsPtr
 * @param Key The key will be used as the criteria for search.
 * @param CBHandle
 * @return The node that matches the key.
 */
inline ds_packetContainer *
ds_searchT (ds_dsBase *dsPtr, int key, CBHandleType CBHandle, ds_e_trav_dir dir)
{
  validateObj (dsPtr);

  if (CBHandle == NULL)
    CBHandle = &ds_searchCBFuncT;
  return ds_traverseT (dsPtr, CBHandle, (void *) &key, NULL, dir);
}

/**
 * Internal search call back function.
 * @param arg In case of this CB for search this is the key value.
 * @param Node
 * @return Node that matches the key.
 */
PRIVATE inline ds_packetContainer *
ds_searchCBFuncT (void *arg, ds_packetContainer * node)
{
  int *key = (int *) arg;

  if (node == NULL)
    return NULL;

  if (*key == ds_getKey (node))
    return node;

  return NULL;
}

/**
 * Process the node. Call the call back handler for the node.
 * @param dsPtr base object reference.
 * @param node From whihc printing starts.
 * @param pchar the character that is used as separator.
 * @param indent the amount of indendation.
 * @return The \c error-code if any error during memory operations else
 * success is returned.
 */
void ds_prettyPrintT (ds_dsBase * dsPtr, ds_packetContainer * node, char pchar, int indent)
{
  //char="-", indent=1)
  if (node == NULL)
    {
      node = ds_getHeadPtr(dsPtr);
    }

  ds_prettyPrintT(dsPtr, ds_getPrevPtr(node), '/', indent+3);
  printf("%s%c%d[%d]", " ", pchar, ds_getKey(node), ds_getBalance(node));
  ds_prettyPrintT(dsPtr, ds_getNextPtr(node), '\\', indent+2);
}

/****************************************************************************/
