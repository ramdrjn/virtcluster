/**
 * @file packet_container.c
 * Contains packet container routines.
 * @author RD
 * @date Sat Jan 15 15:32:25 IST 2011
 */

#include "gen.h"
#include "generr.h"
#include "gentypes.h"
#include "utLib/packet_container.h"

/**
 * Initialize the packet counter and set valid flag.
 * @NOTE: No memory allocation is done here.
 * @param pcPtr packet container object.
 * @return The \c error-code if any error during initilization else
 * success is returned.
 */
inline genErr_t
ds_packetContainerInit (ds_packetContainer * pcPtr)
{
  pcPtr->_validFlag = true;

  return SUCCESS;
}

/**
 * Finalize the packet container. The valid flag is unset.
 * @NOTE: No memory allocation is done here.
 * @param pcPtr packet container object.
 * @return The \c error-code else success is returned.
 */
inline genErr_t
ds_packetContainerFin (ds_packetContainer * pcPtr)
{
  validateObj (pcPtr);

  pcPtr->_validFlag = false;

  return SUCCESS;
}

/**
 * Set the previous pointer in packet container.
 * @param currNode The packet container where the pointer needs to be set.
 * @param newNode The pointer that will be set in the packet container.
 * @return The \c error-code else success is returned.
 */
inline genErr_t
ds_setPrevPtr (ds_packetContainer * currNode, ds_packetContainer * newNode)
{
  validateObj (currNode);
  currNode->prevPtr = newNode;
  return SUCCESS;
}

/**
 * Get the previous pointer from the packet container.
 * @param currNode The packet container from where the pointer will be obtained.
 * @return The previous pointer.
 */
inline ds_packetContainer *
ds_getPrevPtr (ds_packetContainer * currNode)
{
  validateObj (currNode);
  return currNode->prevPtr;
}

/**
 * Set the next pointer in packet container.
 * @param currNode The packet container where the pointer needs to be set.
 * @param newNode The pointer that will be set in the packet container.
 * @return The \c error-code else success is returned.
 */
inline genErr_t
ds_setNextPtr (ds_packetContainer * currNode, ds_packetContainer * newNode)
{
  validateObj (currNode);
  currNode->nextPtr = newNode;
  return SUCCESS;
}

/**
 * Get the next pointer from the packet container.
 * @param currNode The packet container from where the pointer will be obtained.
 * @return The next pointer.
 */
inline ds_packetContainer *
ds_getNextPtr (ds_packetContainer * currNode)
{
  validateObj (currNode);
  return currNode->nextPtr;
}

/**
 * Set the timer data pointer in packet container.
 * @param currNode The packet container where the pointer needs to be set.
 * @param tmrNode The pointer that will be set in the packet container.
 * @return The \c error-code else success is returned.
 */
inline genErr_t
ds_setTimerData (ds_packetContainer * currNode, ds_packetContainer * tmrNode)
{
  validateObj (currNode);
  currNode->timer_data_ptr = tmrNode;
  return SUCCESS;
}

/**
 * Get the timer data pointer from the packet container.
 * @param currNode The packet container from where the pointer will be obtained.
 * @return The timer data pointer.
 */
inline ds_packetContainer *
ds_getTimerData (ds_packetContainer * currNode)
{
  validateObj (currNode);
  return currNode->timer_data_ptr;
}

/**
 * Set the payload data pointer in packet container.
 * @param currNode The packet container where the pointer needs to be set.
 * @param payload The pointer that will be set in the packet container.
 * @return The \c error-code else success is returned.
 */
inline genErr_t
ds_setPayLoadData (ds_packetContainer * currNode, void *payload)
{
  validateObj (currNode);
  currNode->payLoadPtr = payload;
  return SUCCESS;
}

/**
 * Get the payload pointer from the packet container.
 * @param currNode The packet container from where the pointer will be obtained.
 * @return The payload data pointer.
 */
inline void *
ds_getPayLoadData (ds_packetContainer * currNode)
{
  validateObj (currNode);
  return currNode->payLoadPtr;
}

/**
 * Set the queue data pointer in packet container.
 * @param currNode The packet container where the pointer needs to be set.
 * @param queueData The pointer that will be set in the packet container.
 * @return The \c error-code else success is returned.
 */
inline genErr_t
ds_setQueueData (ds_packetContainer * currNode, void *queueData)
{
  validateObj (currNode);
  currNode->queueDataPtr = queueData;
  return SUCCESS;
}

/**
 * Get the queueData pointer from the packet container.
 * @param currNode The packet container from where the pointer will be obtained.
 * @return The queue data pointer.
 */
inline void *
ds_getQueueData (ds_packetContainer * currNode)
{
  validateObj (currNode);
  return currNode->queueDataPtr;
}

/**
 * Set the key for the node
 * @param currNode The packet container where the key needs to be set.
 * @param key
 * @return The \c error-code else success is returned.
 */
inline genErr_t
ds_setKey (ds_packetContainer * currNode, int key)
{
  validateObj (currNode);
  currNode->key = key;
  return SUCCESS;
}

/**
 * Get the key of the node
 * @param currNode The packet container from where the key will be obtained.
 * @return The key value
 */
inline int
ds_getKey (ds_packetContainer * currNode)
{
  validateObj (currNode);
  return currNode->key;
}

/**
 * Set the parent pointer for the node
 * @param currNode The packet container where the pointer needs to be set.
 * @param parentPtr
 * @return The \c error-code else success is returned.
 */
inline genErr_t
ds_setParent (ds_packetContainer * currNode, ds_packetContainer * parentPtr)
{
  validateObj (currNode);
  currNode->parentPtr = parentPtr;
  return SUCCESS;
}

/**
 * Get the parent of the node
 * @param currNode The packet container whose parent needs tobe returned.
 * @return The parent pointer.
 */
inline ds_packetContainer *
ds_getParent (ds_packetContainer * currNode)
{
  validateObj (currNode);
  return currNode->parentPtr;
}

/**
 * Adjust the balance of the node.
 * @param currNode The packet container whose parent needs tobe returned.
 * @param balanceFactor The balance factor that needs to be adjusted.
 * @return The error code.
 */
inline genErr_t
ds_adjustNodeBalance (ds_packetContainer * currNode, int balanceFactor)
{
  validateObj (currNode);
  currNode->balance = +balanceFactor;
  return SUCCESS;
}

/**
 * Get the balance of the node.
 * @param currNode The packet container whose parent needs tobe returned.
 * @param balanceFactor The balance factor that needs to be adjusted.
 * @return The error code.
 */
inline int
ds_getBalance (ds_packetContainer * currNode)
{
  validateObj (currNode);
  return currNode->balance;
}

/**
 * Set the balance of the node.
 * @param currNode The packet container whose parent needs tobe returned.
 * @param balanceFactor The new balance value.
 * @return The error code.
 */
inline genErr_t
ds_setBalance (ds_packetContainer * currNode, int balance)
{
  validateObj (currNode);
  currNode->balance = balance;
  return SUCCESS;
}

/****************************************************************************/
