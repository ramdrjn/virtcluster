#ifndef _I_OMOD_H_
#define _I_OMOD_H_
/**
 * @file _omod.h
 * Internal options module header.
 * @author RD
 * @date Sat Jun 13 19:51:38 IST 2009
 */

#include "gen.h"
#include "generr.h"
#include "gentypes.h"
#include "utLib/mmod.h"
#include "utLib/omod.h"

#include <argp.h>

/**@def _MAX_ARG_OPTS
 * Maximum number of arguments that can be handled.*/
#define _MAX_ARG_OPTS 50

/**@def _MAX_SUB_COMMANDS
 * Maximum number of sub-commands that can be handled.*/
#define _MAX_SUB_COMMANDS 15

/**@struct bs_omodClsType
 * Options object class Type. */
struct bs_omodClsType
{
  t_bool _validFlag;
  // The main parser that will bind the options, general parser and the
  // usage and help strings.
  struct argp mainARGP;
  // The array that will contain the options and its documentation that will
  // be passed to the parser.
  struct argp_option argOpts[_MAX_ARG_OPTS];
  // A internal array that will contain the list of sub-commands.
  char *subOpts[_MAX_SUB_COMMANDS];
  // Pointer to the user parse function.
  bs_userParserType userParseFun;
  // Pointer to a user data, that will be passed transparently to the user
  // parser.
  void *userData;
};

/*Internal function prototypes*/
PRIVATE error_t bs_genericParse (int key, char *arg, struct argp_state *state);

/****************************************************************************/
#endif /*_I_OMOD_H_*/
