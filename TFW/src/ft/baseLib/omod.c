
/*Autogenerated file*/

#include "_proto.h"
#include "../../../../src/utLib/inc/_omod.h"

genErr_t userParseFun (bs_e_optionsType optType, char a, char *b, void *userdata);

genErr_t
userParseFun (bs_e_optionsType optType, char a, char *b, void *userdata)
{
  (void)userdata;
  static int scmdF = 0;
  switch (optType)
    {
    case OPTIONS:
      switch (a)
	{
	case 'a':
	  if ((strcmp (b, "a5") == 0) && (scmdF == 1))
	    break;
	  else if ((strcmp (b, "a1") == 0) && (scmdF == 0))
	    break;
	  return INVALID_OPTIONS;
	case 'b':
	  if (strcmp (b, "a2") != 0)
	    return INVALID_OPTIONS;
	  break;
	case 'd':
	  if (strcmp (b, "a3") != 0)
	    return INVALID_OPTIONS;
	  break;
	case 'e':
	  if (strcmp (b, "a4") != 0)
	    return INVALID_OPTIONS;
	  break;
	case 'h':
	  if (strcmp (b, "a6") != 0)
	    return INVALID_OPTIONS;
	  break;
	case 'i':
	  if (strcmp (b, "a7") != 0)
	    return INVALID_OPTIONS;
	  break;
	case 'j':
	  if (strcmp (b, "a8") != 0)
	    return INVALID_OPTIONS;
	  break;
	case 'l':
	  if (strcmp (b, "a9") != 0)
	    return INVALID_OPTIONS;
	  break;
	case 'k':
	case 'g':
	case 'c':
	  if (b != 0)
	    return INVALID_OPTIONS;
	  break;
	default:
	  return INVALID_OPTIONS;
	}
      break;
    case ARGS:
      if (strcmp (b, "a10") != 0)
	return INVALID_OPTIONS;
      break;
    case SUB_COMMANDS:
      if ((strcmp (b, "scmd1") != 0) && (strcmp (b, "scmd2") != 0))
	return INVALID_OPTIONS;
      scmdF = 1;
      break;
    default:
      return INVALID_OPTIONS;
    }
  return SUCCESS;
}

void
test_omod (void)
{

  bs_omodCls oObj = NULL;
  bs_opts opts[] =
    { {MANDATORY, "mandatory string", "atest", 'a'}, {OPTIONAL,
						      "optional string",
						      "btest", 'b'},
    {NO_OPTIONS, "no options string", "ctest", 'c'}, {MANDATORY,
						      "mandatory no long string",
						      0, 'd'}, {SUB_COMMAND,
								"sub command -header-",
								"scmd1", 0},
    {MANDATORY, "mandatory string", "etest", 'e'}, {OPTIONAL,
						    "optional string (same as main)",
						    "atest", 'a'},
    {NO_OPTIONS, "no options string", "gtest", 'g'}, {OPTIONAL,
						      "optional no long string",
						      0, 'h'}, {SUB_COMMAND,
								"sub command 2 -header-",
								"scmd2", 0},
    {MANDATORY, "mandatory string", 0, 'i'}, {OPTIONAL, "optional string", 0,
					      'j'}, {NO_OPTIONS,
						     "no options string", 0,
						     'k'}, {OPTIONAL,
							    "optional string",
							    0, 'l'} };
  char *args[] =
    { "EXE", "--atest", "a1", "-b", "a2", "--ctest", "-d", "a3", "scmd1",
"--etest", "a4", "-a", "a5", "-g", "-h", "a6", "scmd2", "-i", "a7", "-j", "a8", "-k",
"-l", "a9", "a10" };
  char *userDoc = "User document";
  char *helpDoc = "Help \v document";
  char *userData = "User Data";
  int cnt = 25;

  hdr ("Testing of omod module started");

  retVal = bs_omodInit (&oObj, userDoc, helpDoc, opts, &userParseFun, iMObj);
  EXEC_TSTCASE (&tstCase, " Initialize the options module ", retVal, retVal,
		ec2ES (retVal), 0);

  //  retVal = bs_parseOpts (oObj, cnt, args, userData);
  EXEC_TSTCASE (&tstCase, " Start parsing the options ", retVal, retVal,
		ec2ES (retVal), 0);

  retVal = bs_omodFin (&oObj, iMObj);
  EXEC_TSTCASE (&tstCase, " Finalise the options module ", retVal, retVal,
		ec2ES (retVal), 0);

  hdr ("Testing of omod module compleated");
}
