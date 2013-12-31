/**
 * @file json-ifc.c
 * Contains json decode and encode funtions.
 * @author RD
 * @date Thu Dec 26 16:54:29 IST 2013
 */

#include "cpackgen.h"
#include "json/json.h"

/**
 * Parse json string.
 * json object returned memory reference count should be decremented after
 * usage to free it.
 * @param input string containing the json string.
 * @param jobj_ref json object returned on successful parse
 * @return The \c error-code if any error during operations else
 * success is returned. A reference to the json object is also returned
 * on success
 */
genErr_t
parse_json(const char *input, void **jobj_ref, bs_lmodCls lObj)
{
  debug ("In function %s", __FUNCTION__);

  struct json_object *jobj = NULL;

  jobj = json_tokener_parse(input);
  if (is_error(jobj))
    {
      error("error parsing json: %s\n",
             json_tokener_errors[-(unsigned long)jobj]);
      return (JSON_PARSE_FAIL);
    }

  debug("%s", json_object_to_json_string(jobj));

  *jobj_ref=jobj;

  debug ("Exit function %s", __FUNCTION__);
  return (SUCCESS);
}

/**
 * Decrease reference count of the json object. One nill reference free object.
 * @param jobj_ref json object returned on successful parse
 * @return None
 */
void free_json_obj(void *jobj_ref)
{
  if (jobj_ref)
    json_object_put((struct json_object *)jobj_ref);
}

/**
 * Convert json command to internal command enum value.
 * @param jobj_ref json object returned on successful parse
 * @param lObj logger reference
 * @return The enum for the command.
 */
cmd_e_type get_cmd_from_json(void *jobj_ref, bs_lmodCls lObj)
{
  debug ("In function %s", __FUNCTION__);

  json_type typ;
  struct json_object *jobj = (struct json_object *)jobj_ref;
  cmd_e_type cmd = NIL;
  char const *cmd_str = NULL;

  if (!jobj)
    {
      error("%s", "Invalid json object");
      return (cmd);
    }

  typ = json_object_get_type(jobj);
  if (typ != json_type_string)
    {
      debug ("%s", "Type not string");
      return (cmd);
    }

  cmd_str = json_object_get_string(jobj);
  if ((!cmd_str) || !strlen(cmd_str))
    {
      debug ("%s", "Invalid comand string");
      return (cmd);
    }

  if (strncmp(cmd_str, "start", 5) == 0)
    cmd=START;
  else if (strncmp(cmd_str, "stop", 4) == 0)
    cmd=STOP;
  else if (strncmp(cmd_str, "pause", 5) == 0)
    cmd=PAUSE;
  else if (strncmp(cmd_str, "resume", 6) == 0)
    cmd=RESUME;
  else
    cmd=NIL;

  debug ("Exit function %s", __FUNCTION__);
  return (cmd);
}

/**
 * Get object value for a given key
 * @param jobj_ref json object returned on successful parse
 * @param key String value that will be searched in the jobj.
 * @param lObj logger reference
 * @return The new jobj or null on error
 */
void * get_val_from_key(void *jobj_ref, const char *key, bs_lmodCls lObj)
{
  debug ("In function %s", __FUNCTION__);

  struct json_object *jobj = (struct json_object *)jobj_ref;
  struct json_object *njobj = NULL;

  njobj = json_object_object_get(jobj, key);
  debug ("New object returned %s", json_object_to_json_string(njobj));

  return (njobj);
}

/**
 * Get interger value from the object
 * @param jobj_ref json object returned on successful parse
 * @param lObj logger reference
 * @return The interger value stored in the object.
 */
int get_int(void *jobj_ref, bs_lmodCls lObj)
{
  debug ("In function %s", __FUNCTION__);

  int val=-1;
  struct json_object *jobj = (struct json_object *)jobj_ref;

  val = json_object_get_int(jobj);

  debug ("Integer value returned %d", val);

  return (val);
}

/****************************************************************************/
