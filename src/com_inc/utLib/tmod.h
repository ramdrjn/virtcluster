#ifndef _TMOD_H_
#define _TMOD_H_
/**
 * @file tmod.h
 * Timer module header containing interface declarations.
 * @author RD
 * @date Sun Dec 26 23:40:58 IST 2010
 */

/**@typedef bs_tmodCls
 * Timer object class.*/
typedef struct bs_tmodClsType *bs_tmodCls;

/**@typedef bs_timerHandlerType
 * Defines the timer handler function.*/
#ifdef SIG_USER_DATA_CHGS
typedef genErr_t (*bs_timerHandlerType) (bs_tmodCls tObj, void *userData);
#else
typedef void (*bs_timerHandlerType) (int sigNum);
#endif

/*Prototypes*/
genErr_t bs_tmodInit (bs_tmodCls * tObjPtr, bs_mmodCls mObj);
genErr_t bs_tmodFin (bs_tmodCls * tObjPtr, bs_mmodCls mObj);
genErr_t bs_registerTimerHandler (bs_tmodCls tObj, int usec,
                                  bs_timerHandlerType tmrHndlr,
                                  void *userData);

/****************************************************************************/
#endif /*_TMOD_H_*/
