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

/**@enum cmd_type
 * Commands definitions.*/
typedef enum
  {
    START,
    STOP,
    PAUSE,
    RESUME,
    NIL
  } cmd_e_type;

#define debug(fmt, ...) bs_log(lObj, LVL_DEBUG, FO_LOG, "\n"fmt, __VA_ARGS__)
#define info(fmt, ...) bs_log(lObj, LVL_INFO, FO_LOG, "\n"fmt, __VA_ARGS__)
#define error(fmt, ...) bs_log(lObj, LVL_ERROR, FO_LOG, "\n"fmt, __VA_ARGS__)

genErr_t parse_json(const char *input, void **jobj_ref, bs_lmodCls lObj);
void free_json_obj(void *jobj_ref);
cmd_e_type get_cmd_from_json(void *jobj_ref, bs_lmodCls lObj);
void * get_val_from_key(void *jobj_ref, const char *key, bs_lmodCls lObj);

/****************************************************************************/
#endif /*_CPACKGEN_H_*/
