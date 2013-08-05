#ifndef _FMOD_H_
#define _FMOD_H_
/**
 * @file fmod.h
 * File module header containing interface declarations.
 * @author RD
 * @date Mon Jan 26 20:06:57 EET 2009
 */

#include "vector.h"

/**@typedef bs_fmodCls
 * File object class.*/
typedef struct bs_fmodClsType *bs_fmodCls;

/**@enum bs_e_fType
 * File type declarations- binary, ascii or special (device, pipes etc)*/
typedef enum
  {
    F_BINARY,
    F_ASCII,
    F_SPECIAL
  } bs_e_fType;

/**@enum bs_e_fAMode
 * File operations- read, write, read-write and append.*/
typedef enum
  {
    FA_RD,
    FA_WR,
    FA_RDWR,
    FA_APND
  } bs_e_fAMode;

/*Prototypes.*/
genErr_t bs_fmodInit (bs_fmodCls * fObjPtr, bs_mmodCls mObj);
genErr_t bs_fmodFin (bs_fmodCls * fObjPtr, bs_mmodCls mObj);
genErr_t bs_fCreate (bs_fmodCls fObj, const char *fPath, mode_t fPerm);
genErr_t bs_fOpen (bs_fmodCls fObj, const char *fPath, bs_e_fType fType,
                   bs_e_fAMode fMode);
genErr_t bs_fClose (bs_fmodCls fObj);
genErr_t bs_fOpts (bs_fmodCls fObj, int cmd, void *argP);
genErr_t bs_fObjectify (int fd, bs_fmodCls fObjPtr);
int bs_getFD (bs_fmodCls fObj);

genErr_t bs_fRead (bs_fmodCls fObj, void *buffer, int size, int *retCount);
genErr_t bs_fWrite (bs_fmodCls fObj, const void *buffer, int size,
                    int *retCount);
genErr_t bs_fReadV (bs_fmodCls fObj, int *retCount, const char *fmt, ...);
genErr_t bs_fWriteV (bs_fmodCls fObj, int *retCount, const char *fmt, ...);
genErr_t bs_fVecWrite (bs_fmodCls fObj, vec_io vec, int *retCount);
genErr_t bs_fVecRead (bs_fmodCls fObj, vec_io vec, int *retCount);

/****************************************************************************/
#endif /*_FMOD_H_*/
