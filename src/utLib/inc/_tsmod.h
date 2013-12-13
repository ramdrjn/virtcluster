#ifndef _I_TSMOD_H_
#define _I_TSMOD_H_
/**
 * @file _tsmod.h
 * Internal timer module header for signal implementation.
 * @author RD
 * @date Sat Jan  1 01:04:03 IST 2011
 */

#include "_smod.h"
#include "_tmod.h"

/*Signal handler functional pointer*/
#ifdef SIG_USER_DATA_CHGS
typedef void (*bs_timerSignalHandlerType) (int sigNum, void *userData);
#else
typedef void (*bs_timerSignalHandlerType) (int sigNum);
#endif

/*Internal function prototype*/
genErr_t bs_tmrSigHndlrReg (bs_timerSignalHandlerType tmrHndlr,
                            bs_tmodCls tObj);

/****************************************************************************/
#endif /*_I_TSMOD_H_*/
