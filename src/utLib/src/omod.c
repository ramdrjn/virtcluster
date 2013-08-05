/**
 * @file omod.c
 * Contains routines for parsing options.
 * @author RD
 * @date Sat Jun 13 23:30:42 IST 2009
 */

#include "_omod.h"

/**
 * The initializer function.
 * @return genErr_t
 * @param  oObj
 * @param  usDoc The usage document. Displayed in --usage.
 * @param  helpDoc Displayed during --help. A \\v separates two
 * sections of the help documentation.
 * @param  opts The options in the optsType format. This will contain the
 * supported options (compalsory short option, optional long option in case of
 * options) or sub-commands, their internal documentation (shown in --help
 * option) and the type of arguments that option will handle i.e whether the
 * option is mandatory or optional.
 * @param  fun The funtion pointer that will point to the user defined parse
 * function.
 * @param  mObj Memory object used in internal memory operations.
 */
genErr_t
bs_omodInit (bs_omodCls * oObjPtr, char *usDoc, char *helpDoc, bs_opts * opts,
             bs_userParserType fun, bs_mmodCls mObj)
{
  void *ptr = NULL;
  genErr_t retVal;

  if(oObjPtr == NULL)
    return INVALID_MEM_LOC;
  *oObjPtr = NULL;

  retVal = bs_allocMem (mObj, sizeof (struct bs_omodClsType), &ptr);
  if (retVal != SUCCESS)
    return retVal;

  (*oObjPtr) = (bs_omodCls) ptr;

  (*oObjPtr)->_validFlag = true;

  int i = 0;
  int j = 0;
  for (; opts[i].argTyp != 0; i++)
    {
      if (i >= _MAX_ARG_OPTS)
        break;

      (*oObjPtr)->argOpts[i].flags = 0;
      (*oObjPtr)->argOpts[i].group = 0;
      (*oObjPtr)->argOpts[i].name = 0;
      (*oObjPtr)->argOpts[i].key = 0;
      (*oObjPtr)->argOpts[i].arg = 0;
      (*oObjPtr)->argOpts[i].doc = opts[i].desc;

      if (opts[i].argTyp != SUB_COMMAND)
        {
          (*oObjPtr)->argOpts[i].name = opts[i].longName;
          (*oObjPtr)->argOpts[i].key = opts[i].shortName;
          if (opts[i].argTyp != NO_OPTIONS)
            (*oObjPtr)->argOpts[i].arg = "ARGS";
        }
      else
        {
          (*oObjPtr)->subOpts[j] = (char *) opts[i].longName;
          j++;
        }
    }

  //User needs to specify the parse function.
  if (!fun)
    assert (0);
  (*oObjPtr)->userParseFun = fun;

  (*oObjPtr)->mainARGP.options = (*oObjPtr)->argOpts;
  (*oObjPtr)->mainARGP.parser = bs_genericParse;
  (*oObjPtr)->mainARGP.args_doc = usDoc;
  (*oObjPtr)->mainARGP.doc = helpDoc;

  return SUCCESS;
}

/**
 * The finalizer destroys the option object.
 * @return genErr_t
 * @param  oObj
 */
genErr_t
bs_omodFin (bs_omodCls * oObjPtr, bs_mmodCls mObj)
{
  validateObj (*oObjPtr);

  genErr_t retVal;

  (*oObjPtr)->_validFlag = false;

  retVal = bs_freeMem (mObj, (void *) oObjPtr);
  if (retVal != SUCCESS)
    return retVal;

  return SUCCESS;
}

/**
 * The main parser function.
 * This needs to be invoked by the application to start
 * the parsing of the options. The function takes the following options:
 * 1. The reference options object that should be initialised before
 * calling this function.
 * 2. The arugument count.
 * 3. The reference to the argument buffer.
 * 4. Any optional user data. This user data will be available in
 * the user parse function.
 * @return genErr_t
 * @param  oObj
 * @param  argC Number of arguments held in the argument buffer.
 * @param  argV The argument buffer that holds the user options.
 * @param  userData Application specific user data. This will be passed
 * to the user parser function.
 */
genErr_t
bs_parseOpts (bs_omodCls oObj, int argC, char **argV, void *userData)
{
  error_t retVal;
  int flags = ARGP_IN_ORDER;

  if(oObj == NULL)
    return INVALID_MEM_LOC;

  //Store the user data so that this information can be passed transparently to
  //the user parser function.
  oObj->userData = userData;

  retVal = argp_parse (&(oObj->mainARGP), argC, argV, flags, 0, oObj);

  if (retVal != 0)
    return errno2EC (retVal);

  return SUCCESS;
}

/**
 * The primary options handler.
 * This is invoked when the parser encounters the options,
 * sub-commands and the arguments. This function classifies the options
 * into the types i.e whether they are valid options, sub-commands
 * or arguments. After successful classification the user defined
 * parser function is invoked.
 * @return others
 * @param  key The option as defined by the underlying parser.
 * @param  arg The arguments/sub-commands passed from the underlying parser.
 * @param  state State details of the arguments as defined by the parser.
 */
PRIVATE error_t
bs_genericParse (int key, char *arg, struct argp_state * state)
{
  bs_omodCls oObjPtr = (bs_omodCls) state->input;

  if(oObjPtr == NULL)
    return INVALID_MEM_LOC;

  switch (key)
    {
    case ARGP_KEY_ARG:
      {
        int i = 0;
        bs_e_optionsType typ = ARGS;
        for (; oObjPtr->subOpts[i] != NULL; i++)
          {
            if (!strcmp (oObjPtr->subOpts[i], arg))
              {
                typ = SUB_COMMANDS;
                break;
              }
          }
        if (oObjPtr->userParseFun (typ, 0, arg, oObjPtr->userData) ==
            INVALID_OPTIONS)
          {
            argp_usage (state);
            return ARGP_ERR_UNKNOWN;
          }
      }
    case ARGP_KEY_ARGS:
    case ARGP_KEY_ERROR:
    case ARGP_KEY_NO_ARGS:
    case ARGP_KEY_INIT:
    case ARGP_KEY_END:
    case ARGP_KEY_SUCCESS:
    case ARGP_KEY_FINI:
      break;
    default:
      {
        if (oObjPtr->userParseFun (OPTIONS, key, arg, oObjPtr->userData) ==
            INVALID_OPTIONS)
          {
            argp_usage (state);
            return ARGP_ERR_UNKNOWN;
          }
      }
    }
  return 0;
}
