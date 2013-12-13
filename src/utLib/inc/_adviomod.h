#ifndef _I_ADVIOMOD_H_
#define _I_ADVIOMOD_H_
/**
 * @file _adviomod.h
 * Internal Advanced IO module header
 * @author RD
 * @date Sun Jun  9 20:43:23 IST 2013
 */

#include "gen.h"
#include "generr.h"
#include "gentypes.h"
#include "utLib/mmod.h"
#include "utLib/fmod.h"
#include "utLib/adviomod.h"

/**@struct bs_advioClsType
 * Advanced IO class Type. */
struct bs_advioClsType
{
  t_bool _validFlag;
  int _pollFD;
};

/****************************************************************************/
#endif /*_I_ADVIOMOD_H_*/
