#ifndef _PACKET_CONTAINER_H_
#define _PACKET_CONTAINER_H_

/**
 * @file packet_container.h
 * Packet container header.
 * @author RD
 * @date Sat Jan 15 14:56:03 IST 2011
 */

/**
 * @typedef ds_packetContainer
 * Packet Container.
 */
typedef struct ds_packetContainerType ds_packetContainer;

/**
 * @struct ds_packetContainerType
 * Packet Container class Type.
 */
struct ds_packetContainerType
{
  t_bool _validFlag;
  ds_packetContainer *prevPtr;
  ds_packetContainer *nextPtr;
  ds_packetContainer *parentPtr;
  ds_packetContainer *timer_data_ptr;
  void *payLoadPtr;
  void *queueDataPtr;
  int key;
  int balance;
  unsigned int timestamp;
  //self.__peerNodePtr = []
};

/*Access routines*/
genErr_t ds_packetContainerInit (ds_packetContainer * pcPtr);
genErr_t ds_packetContainerFin (ds_packetContainer * pcPtr);
genErr_t ds_setPrevPtr (ds_packetContainer * currNode,
                        ds_packetContainer * newNode);
ds_packetContainer *ds_getPrevPtr (ds_packetContainer * currNode);
genErr_t ds_setNextPtr (ds_packetContainer * currNode,
                        ds_packetContainer * newNode);
ds_packetContainer *ds_getNextPtr (ds_packetContainer * currNode);
genErr_t ds_setTimerData (ds_packetContainer * currNode,
                          ds_packetContainer * tmrNode);
ds_packetContainer *ds_getTimerData (ds_packetContainer * currNode);
genErr_t ds_setPayLoadData (ds_packetContainer * currNode, void *payload);
void *ds_getPayLoadData (ds_packetContainer * currNode);
genErr_t ds_setQueueData (ds_packetContainer * currNode, void *queueData);
void *ds_getQueueData (ds_packetContainer * currNode);
genErr_t ds_setKey (ds_packetContainer * currNode, int key);
int ds_getKey (ds_packetContainer * currNode);
genErr_t ds_setParent (ds_packetContainer * currNode,
                       ds_packetContainer * parentPtr);
ds_packetContainer *ds_getParent (ds_packetContainer * currNode);
genErr_t ds_adjustNodeBalance (ds_packetContainer * currNode, int balance);
genErr_t ds_setBalance (ds_packetContainer * currNode, int balance);
int ds_getBalance (ds_packetContainer * currNode);
genErr_t ds_setTimestamp (ds_packetContainer * currNode, unsigned int tstamp);
unsigned int ds_getTimestamp (ds_packetContainer * currNode);

/****************************************************************************/
#endif /*_PACKET_CONTAINER_H_*/
