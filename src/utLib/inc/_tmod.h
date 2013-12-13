#ifndef _I_TMOD_H_
#define _I_TMOD_H_
/**
 * @file _tmod.h
 * Internal timer module header.
 * @author RD
 * @date Sun Dec 26 23:36:36 IST 2010
 */

#include "gen.h"
#include "generr.h"
#include "gentypes.h"
#include "utLib/mmod.h"
#include "utLib/tmod.h"

#include <sys/time.h>

/**@struct bs_tmodClsType
 * Timer object class Type. */
struct bs_tmodClsType
{
  t_bool _validFlag;
  void *userData;
  bs_timerHandlerType tmrHndlr;
};

/*Internal function prototypes*/
#ifdef SIG_USER_DATA_CHGS
PRIVATE void
bs_timerCntxt (int signum, void *userData)
#endif
/****************************************************************************/
#endif /*_I_TMOD_H_*/
