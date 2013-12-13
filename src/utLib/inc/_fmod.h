#ifndef _I_FMOD_H_
#define _I_FMOD_H_
/**
 * @file _fmod.h
 * Internal File module header.
 * @author RD
 * @date Mon Jan 26 20:06:57 EET 2009
 */

#include "gen.h"
#include "generr.h"
#include "gentypes.h"
#include "utLib/mmod.h"
#include "utLib/fmod.h"

#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>

/**@struct bs_fmodClsType
 * File object class Type. */
struct bs_fmodClsType
{
  t_bool _validFlag;
  int _fd;
  FILE *_fp;
  bs_e_fType _type;
};

/****************************************************************************/
#endif /*_I_FMOD_H_*/
