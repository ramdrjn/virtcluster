#ifndef _DS_BASE_H_
#define _DS_BASE_H_

/**
 * @file dsbase.h
 * Data structure interfaces.
 * @author RD
 * @date Tue Feb 22 18:46:58 IST 2011
 */

/**@typedef ds_stack
 * Stack class.*/
typedef struct ds_stackType *ds_stack;
/**@typedef ds_queue
 * Queue class.*/
typedef struct ds_queueType *ds_queue;
/**@typedef ds_cqueue
 * circular queue class.*/
typedef struct ds_cqueueType *ds_cqueue;
/**@typedef ds_slist
 * Single List class.*/
typedef struct ds_slistType *ds_slist;
/**@typedef ds_dlist
 * double list class.*/
typedef struct ds_dlistType *ds_dlist;
/**@typedef ds_clist
 * circular singular list class.*/
typedef struct ds_clistType *ds_clist;
/**@typedef ds_cdlist
 * circular double List class.*/
typedef struct ds_cdlistType *ds_cdlist;

/*Non linear DS*/

/* @typedef ds_bst
 * Binary search tree class.*/
typedef struct ds_bstType *ds_bst;
/**@typedef ds_avl
 * AVL tree class.*/
typedef struct ds_avlType *ds_avl;

/**
 * @typedef CBHandleType
 * CallBack handler type for the base class functions.
 */
typedef ds_packetContainer *(*CBHandleType) (void *arg,
                                             ds_packetContainer * node);

/**@enum ds_e_direction
 * Indicates where to push the node. The direction can be left or right. */
typedef enum
  {
    DS_LEFT = 0,
    DS_RIGHT
  } ds_e_direction;

/**@enum ds_e_headTail
 * Indicates whether to remove the head or the tail node.*/
typedef enum
  {
    DS_HEAD = 0,
    DS_TAIL
  } ds_e_headTail;

/**@enum ds_e_trav_dir
 * Traversal direction can be inorder, port order and pre order.*/
typedef enum
  {
    DS_INORDER = 0,
    DS_PREORDER,
    DS_POSTORDER
  } ds_e_trav_dir;


/*Prototypes*/

/*stack*/
genErr_t ds_st_init (ds_stack * stPtr, bs_mmodCls mObj);
genErr_t ds_st_fin (ds_stack * stPtr, bs_mmodCls mObj);
t_bool ds_st_is_empty (ds_stack stPtr);
unsigned short ds_st_get_count (ds_stack stPtr);
genErr_t ds_st_limit (ds_stack stPtr, unsigned short element_limit);
genErr_t ds_st_insert (ds_stack stPtr, ds_packetContainer * data);
ds_packetContainer *ds_st_remove (ds_stack stPtr);
genErr_t ds_st_clear (ds_stack stPtr, bs_mmodCls mObj);
ds_packetContainer *ds_st_traverse (ds_stack stPtr, CBHandleType CBHandle,
                                    void *CBHArgs);
ds_packetContainer *ds_st_search (ds_stack stPtr, int key,
                                  CBHandleType CBHandle);

/*queue*/
genErr_t ds_qu_init (ds_queue * quPtr, bs_mmodCls mObj);
genErr_t ds_qu_fin (ds_queue * quPtr, bs_mmodCls mObj);
t_bool ds_qu_is_empty (ds_queue quPtr);
unsigned short ds_qu_get_count (ds_queue quPtr);
genErr_t ds_qu_limit (ds_queue quPtr, unsigned short element_limit);
genErr_t ds_qu_insert (ds_queue quPtr, ds_packetContainer * data);
ds_packetContainer *ds_qu_remove (ds_queue quPtr);
genErr_t ds_qu_clear (ds_queue quPtr, bs_mmodCls mObj);
ds_packetContainer *ds_qu_traverse (ds_queue quPtr, CBHandleType CBHandle,
                                    void *CBHArgs);
ds_packetContainer *ds_qu_search (ds_queue quPtr, int key,
                                  CBHandleType CBHandle);

/*cqueue*/
genErr_t ds_cq_init (ds_cqueue * cqPtr, bs_mmodCls mObj);
genErr_t ds_cq_fin (ds_cqueue * cqPtr, bs_mmodCls mObj);
t_bool ds_cq_is_empty (ds_cqueue cqPtr);
unsigned short ds_cq_get_count (ds_cqueue cqPtr);
genErr_t ds_cq_limit (ds_cqueue cqPtr, unsigned short element_limit);
genErr_t ds_cq_insert (ds_cqueue cqPtr, ds_packetContainer * data);
ds_packetContainer *ds_cq_remove (ds_cqueue cqPtr);
genErr_t ds_cq_clear (ds_cqueue cqPtr, bs_mmodCls mObj);
ds_packetContainer *ds_cq_traverse (ds_cqueue cqPtr, CBHandleType CBHandle,
                                    void *CBHArgs);
ds_packetContainer *ds_cq_search (ds_cqueue cqPtr, int key,
                                  CBHandleType CBHandle);

/*slist*/
genErr_t ds_sl_init (ds_slist * slPtr, bs_mmodCls mObj);
genErr_t ds_sl_fin (ds_slist * slPtr, bs_mmodCls mObj);
t_bool ds_sl_is_empty (ds_slist slPtr);
unsigned short ds_sl_get_count (ds_slist slPtr);
genErr_t ds_sl_limit (ds_slist slPtr, unsigned short element_limit);
genErr_t ds_sl_insert (ds_slist slPtr, ds_packetContainer * data,
                       ds_packetContainer * node);
ds_packetContainer *ds_sl_remove (ds_slist slPtr, ds_packetContainer * node,
                                  ds_e_headTail htail);
genErr_t ds_sl_clear (ds_slist slPtr, bs_mmodCls mObj);
ds_packetContainer *ds_sl_traverse (ds_slist slPtr, CBHandleType CBHandle,
                                    void *CBHArgs, ds_packetContainer * node);
ds_packetContainer *ds_sl_search (ds_slist slPtr, int key,
                                  CBHandleType CBHandle);

/*dlist*/
genErr_t ds_dl_init (ds_dlist * dlPtr, bs_mmodCls mObj);
genErr_t ds_dl_fin (ds_dlist * dlPtr, bs_mmodCls mObj);
t_bool ds_dl_is_empty (ds_dlist dlPtr);
unsigned short ds_dl_get_count (ds_dlist dlPtr);
genErr_t ds_dl_limit (ds_dlist dlPtr, unsigned short element_limit);
genErr_t ds_dl_insert (ds_dlist dlPtr, ds_packetContainer * data,
                       ds_packetContainer * node, ds_e_direction dir);
ds_packetContainer *ds_dl_remove (ds_dlist dlPtr, ds_packetContainer * node,
                                  ds_e_headTail htail);
genErr_t ds_dl_clear (ds_dlist dlPtr, bs_mmodCls mObj);
ds_packetContainer *ds_dl_traverse (ds_dlist dlPtr, CBHandleType CBHandle,
                                    void *CBHArgs, ds_packetContainer * node,
                                    ds_e_direction dir);
ds_packetContainer *ds_dl_search (ds_dlist dlPtr, int key,
                                  CBHandleType CBHandle);

/*clist*/
genErr_t ds_cl_init (ds_clist * clPtr, bs_mmodCls mObj);
genErr_t ds_cl_fin (ds_clist * clPtr, bs_mmodCls mObj);
t_bool ds_cl_is_empty (ds_clist clPtr);
unsigned short ds_cl_get_count (ds_clist clPtr);
genErr_t ds_cl_limit (ds_clist clPtr, unsigned short element_limit);
genErr_t ds_cl_insert (ds_clist clPtr, ds_packetContainer * data,
                       ds_packetContainer * node);
ds_packetContainer *ds_cl_remove (ds_clist clPtr, ds_packetContainer * node,
                                  ds_e_headTail htail);
genErr_t ds_cl_clear (ds_clist clPtr, bs_mmodCls mObj);
ds_packetContainer *ds_cl_traverse (ds_clist clPtr, CBHandleType CBHandle,
                                    void *CBHArgs, ds_packetContainer * node);
ds_packetContainer *ds_cl_search (ds_clist clPtr, int key,
                                  CBHandleType CBHandle);

/*cdlist*/
genErr_t ds_cd_init (ds_cdlist * cdPtr, bs_mmodCls mObj);
genErr_t ds_cd_fin (ds_cdlist * cdPtr, bs_mmodCls mObj);
t_bool ds_cd_is_empty (ds_cdlist cdPtr);
unsigned short ds_cd_get_count (ds_cdlist cdPtr);
genErr_t ds_cd_limit (ds_cdlist cdPtr, unsigned short element_limit);
genErr_t ds_cd_insert (ds_cdlist cdPtr, ds_packetContainer * data,
                       ds_packetContainer * node, ds_e_direction dir);
ds_packetContainer *ds_cd_remove (ds_cdlist cdPtr, ds_packetContainer * node,
                                  ds_e_headTail htail);
genErr_t ds_cd_clear (ds_cdlist cdPtr, bs_mmodCls mObj);
ds_packetContainer *ds_cd_traverse (ds_cdlist cdPtr, CBHandleType CBHandle,
                                    void *CBHArgs, ds_packetContainer * node,
                                    ds_e_direction dir);
ds_packetContainer *ds_cd_search (ds_cdlist cdPtr, int key,
                                  CBHandleType CBHandle);

/*Non linear DS*/
/*bst*/
genErr_t ds_bst_init (ds_bst *bstPtr, bs_mmodCls mObj);
genErr_t ds_bst_fin (ds_bst *bstPtr, bs_mmodCls mObj);
t_bool ds_bst_is_empty (ds_bst bstPtr);
unsigned short ds_bst_get_count (ds_bst bstPtr);
genErr_t ds_bst_limit (ds_bst bstPtr, unsigned short element_limit);
genErr_t ds_bst_insert (ds_bst bstPtr, ds_packetContainer * data);
ds_packetContainer *ds_bst_remove (ds_bst bstPtr, ds_packetContainer * node);
genErr_t ds_bst_clear(ds_bst bstPtr, ds_packetContainer *node, bs_mmodCls mObj);
ds_packetContainer *ds_bst_traverse (ds_bst bstPtr, CBHandleType CBHandle,
                                     void *CBHArgs, ds_packetContainer * node,
                                     ds_e_trav_dir dir);
ds_packetContainer *ds_bst_search (ds_bst bstPtr, int key,
                                   CBHandleType CBHandle, ds_e_trav_dir dir);

/*avl*/
genErr_t ds_avl_init (ds_avl *avlPtr, bs_mmodCls mObj);
genErr_t ds_avl_fin (ds_avl *avlPtr, bs_mmodCls mObj);
t_bool ds_avl_is_empty (ds_avl avlPtr);
unsigned short ds_avl_get_count (ds_avl avlPtr);
genErr_t ds_avl_limit (ds_avl avlPtr, unsigned short element_limit);
genErr_t ds_avl_insert (ds_avl avlPtr, ds_packetContainer * data);
ds_packetContainer *ds_avl_remove (ds_avl avlPtr, ds_packetContainer * node);
genErr_t ds_avl_clear(ds_avl avlPtr, ds_packetContainer *node, bs_mmodCls mObj);
ds_packetContainer *ds_avl_traverse (ds_avl avlPtr, CBHandleType CBHandle,
                                     void *CBHArgs, ds_packetContainer * node,
                                     ds_e_trav_dir dir);
ds_packetContainer *ds_avl_search (ds_avl avlPtr, int key,
                                   CBHandleType CBHandle, ds_e_trav_dir dir);

/*for debugging purpose*/
void ds_prettyPrint (ds_bst bstPtr, char pchar, int indent);

/****************************************************************************/
#endif /*_DS_BASE_H__*/
