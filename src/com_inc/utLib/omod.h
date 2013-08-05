#ifndef _OMOD_H_
#define _OMOD_H_
/**
 * @file omod.h
 * Options module header containing interface declarations.
 * @author RD
 * @date Sat Jun 13 19:48:39 IST 2009
 */

/**@typedef bs_omodCls
 * options object class.*/
typedef struct bs_omodClsType *bs_omodCls;

/**@enum bs_e_optionsType
 * This is used in the user parser function to differentiate between a
 * sub-command, option or its argument.*/
typedef enum
  {
    OPTIONS = 1,
    ARGS,
    SUB_COMMANDS
  } bs_e_optionsType;

/**@enum bs_e_argType
 * Used to specify the type of the argument for the options and also to
 * differentiate between an option and a sub-command.*/
typedef enum
  {
    NO_OPTIONS = 1,
    MANDATORY,
    OPTIONAL,
    SUB_COMMAND
  } bs_e_argType;

/**@struct bs_opts
 * Argument Options Type. */
typedef struct
{
  bs_e_argType argTyp;
  const char *desc;
  const char *longName;
  char shortName;
} bs_opts;

/**@typedef bs_userParserType
 * Defines the user parser function type.*/
typedef genErr_t (*bs_userParserType) (bs_e_optionsType, char, char *,
                                       void *);

/*Prototypes*/
genErr_t bs_omodInit (bs_omodCls * oObjPtr, char *usDoc, char *helpDoc,
                      bs_opts * opts, bs_userParserType fun, bs_mmodCls mObj);
genErr_t bs_omodFin (bs_omodCls * oObjPtr, bs_mmodCls mObj);
genErr_t bs_parseOpts (bs_omodCls oObj, int argC, char **argV,
                       void *userData);

/****************************************************************************/
#endif /*_OMOD_H_*/
