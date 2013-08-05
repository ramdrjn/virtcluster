#ifndef _MMOD_H_
#define _MMOD_H_
/**
 * @file mmod.h
 * Memory module header containing interface declerations.
 * @author RD
 * @date Mon Jan 26 20:06:57 EET 2009
 */

/**@typedef bs_mmodCls
 * Memory object class.*/
typedef struct bs_mmodClsType *bs_mmodCls;

/*Prototype*/
genErr_t bs_mmodInit (bs_mmodCls * memObjPtr);
genErr_t bs_mmodFin (bs_mmodCls * memObjPtr);
genErr_t bs_allocMem (bs_mmodCls memObj, size_t size, void **memPtr);
genErr_t bs_freeMem (bs_mmodCls memObj, void **memPtr);

/****************************************************************************/
#endif /*_MMOD_H_*/
