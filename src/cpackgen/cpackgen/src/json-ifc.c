/**
 * @file json-ifc.c
 * Contains json decode and encode funtions.
 * @author RD
 * @date Thu Dec 26 16:54:29 IST 2013
 */

#include "json-ifc.h"
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

  if (!jobj)
    {
      error("%s", "Invalid json object");
      return (NULL);
    }

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

  json_type typ;
  int val=-1;
  struct json_object *jobj = (struct json_object *)jobj_ref;

  if (!jobj)
    {
      error("%s", "Invalid json object");
      return (val);
    }

  typ = json_object_get_type(jobj);
  if (typ != json_type_int)
    {
      debug ("%s", "Type not int");
      return (val);
    }

  val = json_object_get_int(jobj);

  debug ("Integer value returned %d", val);

  return (val);
}

/**
 * Get string value from the object
 * @param jobj_ref json object returned on successful parse
 * @param lObj logger reference
 * @return The string value stored in the object.
 */
const char* get_string(void *jobj_ref, bs_lmodCls lObj)
{
  debug ("In function %s", __FUNCTION__);

  json_type typ;
  char const *val = NULL;
  struct json_object *jobj = (struct json_object *)jobj_ref;

  if (!jobj)
    {
      error("%s", "Invalid json object");
      return (NULL);
    }

  typ = json_object_get_type(jobj);
  if (typ != json_type_string)
    {
      debug ("%s", "Type not string");
      return (NULL);
    }

  val = json_object_get_string(jobj);

  debug ("String value returned %s", val);

  return (val);
}

/****************************************************************************/
