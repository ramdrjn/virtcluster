#ifndef _JSON_IFC_H_
#define _JSON_IFC_H_
/**
 * @file json_ifc.h
 * json interface header file
 * @author RD
 * @date Sun Dec 22 15:08:17 IST 2013
 */

#include "gen.h"
#include "generr.h"
#include "gentypes.h"

#include "utLib/mmod.h"
#include "utLib/fmod.h"
#include "utLib/lmod.h"

genErr_t parse_json(const char *input, void **jobj_ref, bs_lmodCls lObj);
void free_json_obj(void *jobj_ref);
void * get_val_from_key(void *jobj_ref, const char *key, bs_lmodCls lObj);
int get_int(void *jobj_ref, bs_lmodCls lObj);
const char* get_string(void *jobj_ref, bs_lmodCls lObj);

#define debug(fmt, ...) bs_log(lObj, LVL_DEBUG, FO_LOG, "\n"fmt, __VA_ARGS__)
#define info(fmt, ...) bs_log(lObj, LVL_INFO, FO_LOG, "\n"fmt, __VA_ARGS__)
#define error(fmt, ...) bs_log(lObj, LVL_ERROR, FO_LOG, "\n"fmt, __VA_ARGS__)

/****************************************************************************/
#endif /*_JSON_IFC_H_*/
