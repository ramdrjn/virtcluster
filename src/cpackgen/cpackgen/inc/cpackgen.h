#ifndef _CPACKGEN_H_
#define _CPACKGEN_H_
/**
 * @file cpackgen.h
 * cpackgen main header file
 * @author RD
 * @date Sun Dec 22 15:08:17 IST 2013
 */

#include "gen.h"
#include "generr.h"
#include "gentypes.h"

#include "utLib/mmod.h"
#include "utLib/fmod.h"
#include "utLib/lmod.h"

#define debug(fmt, ...) bs_log(lObj, LVL_DEBUG, PF_LOG, "\n"fmt, __VA_ARGS__)
#define info(fmt, ...) bs_log(lObj, LVL_INFO, PF_LOG, "\n"fmt, __VA_ARGS__)
#define error(fmt, ...) bs_log(lObj, LVL_ERROR, PF_LOG, "\n"fmt, __VA_ARGS__)

/****************************************************************************/
#endif /*_CPACKGEN_H_*/
