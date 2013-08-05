#ifndef _I_LMOD_H_
#define _I_LMOD_H_
/**
 * @file _lmod.h
 * Internal Log module header.
 * @author RD
 * @date Mon Jan 26 20:06:57 EET 2009
 */

#include "gen.h"
#include "generr.h"
#include "gentypes.h"
#include "utLib/mmod.h"
#include "utLib/fmod.h"
#include "utLib/lmod.h"

#include <syslog.h>

/**@def LOG_BUFFER_SIZE
 * Maximum Log message size.*/
#define LOG_BUFFER_SIZE 100

/**@struct bs_lmodClsType
 * Log object class Type. */
struct bs_lmodClsType
{
  t_bool _validFlag;
  int _verboseFlag;
  int _quiteFlag;
  int _syslogFlag;
  bs_fmodCls _filePtr;
  char _buffer[LOG_BUFFER_SIZE + 1];
};

/*Internal function prototypes*/
PRIVATE inline t_bool _checkLogLevel (bs_lmodCls lObj, bs_e_logLvl logLevel);
PRIVATE inline int _retSyslogLvl (bs_e_logLvl logLevel);
PRIVATE inline void _log (bs_lmodCls lObj, bs_e_logLvl logLevel,
                          bs_e_logMode mode);

/****************************************************************************/
#endif /*_I_LMOD_H_*/
