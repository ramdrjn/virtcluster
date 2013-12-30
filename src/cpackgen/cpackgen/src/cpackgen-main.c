/**
 * @file cpackgen-main.c
 * Contains main entry point
 * @author RD
 * @date Sun Dec 22 15:08:17 IST 2013
 */

#include "cpackgen.h"

void _exit_cleanup(bs_mmodCls mObj, bs_fmodCls fObj, bs_lmodCls lObj);

/**
 * Called before exit. Cleanup of all objects.
 * @param fObj Reference of the file object.
 * @param mObj Reference of the memory object.
 * @param lObj Reference of the log object.
 * @return None
 */
void _exit_cleanup(bs_mmodCls mObj, bs_fmodCls fObj, bs_lmodCls lObj)
{
  bs_lmodFin (&lObj, mObj);
  if (fObj != NULL)
    {
      bs_fClose (fObj);
      bs_fmodFin (&fObj, mObj);
    }
  bs_mmodFin (&mObj);
}

#define INPUT_JSON_BUFFER_SIZE 4096

/**
 * Main
 */
int main(int argc, char *argv[])
{
  genErr_t retVal;
  cmd_e_type cmd;
  char *input = NULL;
  void *jobj = NULL;
  char *mode = NULL;
  bs_mmodCls mObj = NULL;
  bs_fmodCls fObj = NULL;
  bs_lmodCls lObj = NULL;
  bs_fmodCls input_fObj = NULL;
  const char *debug_fname = "/tmp/cpackgen-debug";
  t_bool run_flag = true;
  int ret_cnt=-1;

  if (argc < 2)
    return (-1);

  mode = argv[1];

  retVal = bs_mmodInit (&mObj);
  if (retVal != SUCCESS)
    return (retVal);

  retVal = bs_fmodInit (&fObj, mObj);
  if (retVal != SUCCESS)
    {
      _exit_cleanup(mObj, fObj, lObj);
      return (retVal);
    }

  retVal = bs_fCreate (fObj, debug_fname, 0644);
  /*
    Ignore file creation errors.
    if (retVal != SUCCESS)
    {
    _exit_cleanup(mObj, fObj, lObj);
    return (retVal);
    }
  */

  retVal = bs_fOpen (fObj, debug_fname, F_ASCII, FA_WR);
  if (retVal != SUCCESS)
    {
      _exit_cleanup(mObj, fObj, lObj);
      return (retVal);
    }

  retVal = bs_lmodInit (&lObj, false, false, true, fObj, mObj);
  if (retVal != SUCCESS)
    {
      _exit_cleanup(mObj, fObj, lObj);
      return (retVal);
    }

  debug ("%s", "Starting cpackgen");
  info ("%s %s", "Starting in mode:", mode);

  retVal = bs_fmodInit (&input_fObj, mObj);
  if (retVal != SUCCESS)
    {
      error ("%s", "Allocation memory for input file object failed");
      _exit_cleanup(mObj, input_fObj, lObj);
      return (retVal);
    }

  retVal = bs_fObjectify (0, input_fObj);
  if (retVal != SUCCESS)
    {
      error ("%s", "STDIN open failed");
      _exit_cleanup(mObj, input_fObj, lObj);
      return (retVal);
    }

  retVal = bs_allocMem(mObj, INPUT_JSON_BUFFER_SIZE, (void *)&input);
  if (retVal != SUCCESS)
    {
      error ("%s", "Allocation memory for json input failed");
      _exit_cleanup(mObj, fObj, lObj);
      return (retVal);
    }

  while (run_flag)
    {
      retVal = bs_fRead(input_fObj, (void *)input,
                        INPUT_JSON_BUFFER_SIZE, &ret_cnt);
      if (retVal != SUCCESS)
        {
          error ("%s %s", "STDIN read failed ", ec2ES(retVal));
          _exit_cleanup(mObj, input_fObj, lObj);
          return (retVal);
        }

      debug("json input received %s length %d", input, strlen(input));

      if (ret_cnt <= 0)
        {
          error ("%s", "Exiting on 0 read");
          _exit_cleanup(mObj, input_fObj, lObj);
          return (EOF_REACHED);
        }
      input[ret_cnt]=0;

      retVal = parse_json(input, &jobj, lObj);
      if (retVal != SUCCESS)
        {
          error ("%s", "JSON parse fail");
          _exit_cleanup(mObj, fObj, lObj);
          return (retVal);
        }
      input[0]=0;

      cmd = get_cmd_from_json(jobj, lObj);

      debug("Command received: %d", cmd);

      debug("%s", "Freeing json object");
      free_json_obj(jobj);
      jobj = NULL;

      if (cmd == STOP)
        {
          info("%s", "Stopping due to JSON command");
          run_flag = false;
          break;
        }
    }

  if (input_fObj != NULL)
    {
      bs_fmodFin (&input_fObj, mObj);
    }

  retVal = bs_freeMem(mObj, (void *)&input);
  if (retVal != SUCCESS)
    {
      error ("%s", "Memory free for json input failed");
      _exit_cleanup(mObj, fObj, lObj);
      return (retVal);
    }

  _exit_cleanup(mObj, fObj, lObj);
  return (0);
}

/****************************************************************************/
