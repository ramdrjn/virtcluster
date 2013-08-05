#ifndef _I_SMOD_H_
#define _I_SMOD_H_
/**
 * @file _smod.h
 * Internal signal module header.
 * @author RD
 * @date Sun Dec 19 22:13:11 IST 2010
 */

#include "gen.h"
#include "generr.h"
#include "gentypes.h"
#include "utLib/mmod.h"
#include "utLib/smod.h"

#include <signal.h>

/**@struct bs_smodClsType
 * Signals object class Type. */
struct bs_smodClsType
{
  t_bool _validFlag;
  void *userData;
  bs_userSignalHandlerType sigHndlr;
};

/*Internal function prototypes*/
#ifdef SIG_USER_DATA_CHGS
PRIVATE void bs_sigHandler (int sigNum, void *userData);
#endif

/****************************************************************************/
#endif /*_I_SMOD_H_*/
