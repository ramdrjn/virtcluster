#ifndef _TSKMOD_H_
#define _TSKMOD_H_
/**
 * @file tskmod.h
 * Task module header.
 * @author RD
 * @date Sun May 26 16:30:40 IST 2013
 */

/**@typedef bs_tskmodCls
 * Task object class.*/
typedef struct bs_tskmodClsType *bs_tskmodCls;

/**@enum bs_e_tskType
 * Task type definitions.*/
typedef enum
  {
    TSK_HEAVY,
    TSK_LIGHT
  } bs_e_tskType;

/**@typedef bs_spawnCBType
 * Defines the callback handler type that will be after spawing new process*/
typedef genErr_t (*bs_spawnCBType)(bs_tskmodCls tskObjPtr, char *argv[]);

/*Prototype*/
genErr_t bs_tskmodInit (bs_tskmodCls *tskObjPtr, bs_mmodCls mObj);
genErr_t bs_tskmodFin (bs_tskmodCls *tskObjPtr, bs_mmodCls mObj);
bs_tskmodCls bs_spawn (bs_tskmodCls tskObjPtr, bs_mmodCls mObj,
                       bs_spawnCBType spawnCB, char *argv[]);
genErr_t bs_exec (bs_tskmodCls tskObjPtr, char *path, char *argv[],
                  char *env[]);
bs_tskmodCls bs_spawnLW (bs_tskmodCls tskObjPtr, bs_mmodCls mObj,
                         bs_spawnCBType spawnCB, char *argv[]);
genErr_t bs_wait (bs_tskmodCls tskObjPtr, genErr_t *retP);

/****************************************************************************/
#endif /*_TSKMOD_H_*/
