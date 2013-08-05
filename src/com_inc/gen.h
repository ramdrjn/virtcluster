#ifndef _GEN_H_
#define _GEN_H_
/**
 * @file gen.h
 * General header containing basic files to be included by all modules.
 * @author RD
 * @date Mon Jan 26 20:06:57 EET 2009
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <stdarg.h>

#include "config.h"

/**@def SET_ZERO
 * Macro to set 0 to the passed variable*/
#define SET_ZERO(x) memset(&x, 0, sizeof(x));

/**@def SET_ZERO_PTR
 * Macro to set 0 to the address pointed by ptr*/
#define SET_ZERO_PTR(x) memset(x, 0, sizeof(*x));

/****************************************************************************/
#endif /*_GEN_H_*/
