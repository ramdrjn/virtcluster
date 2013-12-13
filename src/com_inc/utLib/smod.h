#ifndef _SMOD_H_
#define _SMOD_H_
/**
 * @file smod.h
 * Signals module header containing interface declarations.
 * @author RD
 * @date Sun Dec 19 22:11:10 IST 2010
 */

/**@typedef bs_smodCls
 * Signals object class.*/
typedef struct bs_smodClsType *bs_smodCls;

/**@typedef bs_userSignalType
 * Defines the handler function for the specified signal number.*/
#ifdef SIG_USER_DATA_CHGS
typedef genErr_t (*bs_userSignalHandlerType) (int signum, bs_smodCls sObj,
                                              void *userData);
#else
typedef void (*bs_userSignalHandlerType) (int signum);
#endif

/*Prototypes*/
genErr_t bs_smodInit (bs_smodCls * sObjPtr, bs_mmodCls mObj);
genErr_t bs_smodFin (bs_smodCls * sObjPtr, bs_mmodCls mObj);
genErr_t bs_registerHandler (bs_smodCls sObj, int sigNum,
                             bs_userSignalHandlerType sigHndlr,
                             void *userData);

/****************************************************************************/
#endif /*_SMOD_H_*/
