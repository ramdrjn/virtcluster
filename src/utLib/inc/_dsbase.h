#ifndef _I_DS_BASE_H_
#define _I_DS_BASE_H_

/**
 * @file _dsbase.h
 * Internal base implementation header.
 * @author RD
 * @date Sun Jan 16 22:09:12 IST 2011
 */

#include "gen.h"
#include "generr.h"
#include "gentypes.h"
#include "utLib/mmod.h"
#include "utLib/packet_container.h"
#include "utLib/dsbase.h"

/**
 * @define MAX_DS_VALUES
 * The maximum number of nodes that can be inserted in the datastructure.
 */
#define MAX_DS_VALUES 65535

/**@enum ds_e_dsType
 * The type of datastructure that will be registered in the base.*/
typedef enum
  {
    DS_STACK = 0,
    DS_QUEUE,
    DS_SLIST,
    DS_DLIST,
    DS_CQUEUE,
    DS_CLIST,
    DS_CDLIST,
    DS_BST,
    DS_AVL
  } ds_e_dsType;

/**@enum ds_e_opType
 * The operation type (either insert or remove) mainly used in tree balance
 * operations.*/
typedef enum
  {
    DS_REM = 0,
    DS_INS
  } ds_e_opType;

/**
 * @typedef ds_dsBaseType
 * DS base class.
 */
typedef struct ds_dsBaseType ds_dsBase;

/**
 * @struct ds_dsBaseType
 * DS base class Type.
 */
struct ds_dsBaseType
{
  t_bool _validFlag;
  unsigned short count;
  ds_packetContainer *headPtr;
  ds_packetContainer *tailPtr;
  t_bool circular;
  ds_e_dsType type;
  unsigned short elementLimit;
};

/**
 * @struct ds_stackType
 * DS stack class Type.
 */
struct ds_stackType
{
  ds_dsBase base;
};
/**
 * @struct ds_queueType
 * DS queue class Type.
 */
struct ds_queueType
{
  ds_dsBase base;
};
/**
 * @struct ds_cqueueType
 * DS circular queue class Type.
 */
struct ds_cqueueType
{
  ds_dsBase base;
};
/**
 * @struct ds_slistType
 * DS single list class Type.
 */
struct ds_slistType
{
  ds_dsBase base;
};
/**
 * @struct ds_dlistType
 * DS double list class Type.
 */
struct ds_dlistType
{
  ds_dsBase base;
};
/**
 * @struct ds_clistType
 * DS circular list class Type.
 */
struct ds_clistType
{
  ds_dsBase base;
};
/**
 * @struct ds_cdlistType
 * DS circular double list class Type.
 */
struct ds_cdlistType
{
  ds_dsBase base;
};

/*NON linear DS*/

/**
 * @struct ds_bstType
 * DS Binary search tree class Type.
 */
struct ds_bstType
{
  ds_dsBase base;
};
/**
 * @struct ds_avlType
 * DS AVL tree class Type.
 */
struct ds_avlType
{
  ds_dsBase base;
};

/*Access routines*/
inline genErr_t ds_dsBaseInit (ds_dsBase * dsPtr, ds_e_dsType type);
inline genErr_t ds_dsBaseFin (ds_dsBase * dsPtr);
inline t_bool ds_isEmpty (ds_dsBase * dsPtr);
inline unsigned short ds_getCount (ds_dsBase * dsPtr);
inline genErr_t ds_insert (ds_dsBase * dsPtr, ds_packetContainer * data,
                           ds_packetContainer * node, ds_e_direction dir);
inline genErr_t ds_clear (ds_dsBase * dsPtr, bs_mmodCls mObj);
inline ds_packetContainer *ds_remove (ds_dsBase * dsPtr,
                                      ds_packetContainer * node,
                                      ds_e_headTail htail);
inline ds_packetContainer *ds_search (ds_dsBase * dsPtr, int key,
                                      CBHandleType CBHandle);
inline ds_packetContainer *ds_traverse (ds_dsBase * dsPtr,
                                        CBHandleType CBHandle,
                                        void *CBHArgs,
                                        ds_packetContainer * travNode,
                                        ds_e_direction dir);
inline genErr_t ds_setElementLimit (ds_dsBase * dsPtr,
                                    unsigned short elementLimit);

/*Non linear data structures.*/
inline genErr_t ds_insertT (ds_dsBase * dsPtr, ds_packetContainer * data);
inline ds_packetContainer *ds_removeT (ds_dsBase * dsPtr,
                                       ds_packetContainer * node);
inline genErr_t ds_clearT (ds_dsBase * dsPtr, ds_packetContainer * travNode,
                           bs_mmodCls mObj);
inline ds_packetContainer *ds_traverseT (ds_dsBase * dsPtr, CBHandleType CBHandle, void *CBHArgs, ds_packetContainer * travNode, ds_e_trav_dir dir);
inline ds_packetContainer *ds_searchT (ds_dsBase * dsPtr, int key, CBHandleType CBHandle, ds_e_trav_dir dir);

/*for debugging*/
void ds_prettyPrintT (ds_dsBase * dsPtr, ds_packetContainer * node, char pchar, int indent);

/****************************************************************************/
#endif /*_I_DS_BASE_H_*/
