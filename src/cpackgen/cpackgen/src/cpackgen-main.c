/**
 * @file cpackgen-main.c
 * Contains main entry point
 * @author RD
 * @date Sun Dec 22 15:08:17 IST 2013
 */

#include "cpackgen.h"

void _exit_cleanup(bs_mmodCls mObj, bs_fmodCls fObj, bs_lmodCls lObj);
genErr_t
process_gen_param(void *njobj, struct gen_param_t *gen_param, bs_lmodCls lObj);

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

/**
 * Process generator parameters
 * @param njobj New json object cotaining parameters.
 * @param gen_param Generator parameter structure that will be populated
 * from the njobj
 * @param lObj Reference of the log object.
 * @return The \c error-code if any error else success is returned.
 */
genErr_t
process_gen_param(void *njobj, struct gen_param_t *gen_param, bs_lmodCls lObj)
{
  debug ("In function %s", __FUNCTION__);

  void *tjobj = NULL;

  tjobj=get_val_from_key(njobj, "rate_bps", lObj);
  if(tjobj)
    {
      gen_param->rate_bps=get_int(tjobj, lObj);
      debug ("rate_bps value %d", gen_param->rate_bps);
      free_json_obj(tjobj);
    }
  else
    {
      debug ("%s", "rate_bps not available");
    }

  tjobj=get_val_from_key(njobj, "rate_pps", lObj);
  if(tjobj)
    {
      gen_param->rate_pps=get_int(tjobj, lObj);
      debug ("rate_pps value %d", gen_param->rate_pps);
      free_json_obj(tjobj);
    }
  else
    {
      debug ("%s", "rate_pps not available");
    }

  tjobj=get_val_from_key(njobj, "max_count", lObj);
  if(tjobj)
    {
      gen_param->max_count=get_int(tjobj, lObj);
      debug ("max_count value %d", gen_param->max_count);
      free_json_obj(tjobj);
    }
  else
    {
      debug ("%s", "max_count not available");
    }

  tjobj=get_val_from_key(njobj, "duration_max", lObj);
  if(tjobj)
    {
      gen_param->duration_max=get_int(tjobj, lObj);
      debug ("duration_max value %d", gen_param->duration_max);
      free_json_obj(tjobj);
    }
  else
    {
      debug ("%s", "duration_max not available");
    }

  return (SUCCESS);
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

  struct conf_t conf;

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
  if (strncmp(mode, "generator", 9) ==0)
    {
      conf.mode = GENERATOR;
    }
  else if (strncmp(mode, "receiver", 8) ==0)
    {
      conf.mode = RECEIVER;
    }
  else
    {
      error ("%s", "No mode set");
      _exit_cleanup(mObj, input_fObj, lObj);
      return (FAILURE);
    }
  conf._validFlag = true;

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

      if (cmd == STOP)
        {
          info("%s", "Stopping due to JSON command");
          debug("%s", "Freeing json object");
          free_json_obj(jobj);
          jobj = NULL;
          run_flag = false;
          break;
        }

      /*Process json object and get values*/
      if (cmd == NIL)
        {
          void *njobj = NULL;
          njobj=get_val_from_key(jobj, "generator_parameter", lObj);
          if(njobj)
            {
              /*Process as generator parameter*/
              process_gen_param(njobj, &conf.gen_params, lObj);
              free_json_obj(njobj);
              njobj = NULL;
            }
          njobj=get_val_from_key(jobj, "generator_packet", lObj);
          if(njobj)
            {
              /*Process as generator packet*/
              free_json_obj(njobj);
              njobj = NULL;
            }
        }

      debug("%s", "Freeing json object");
      free_json_obj(jobj);
      jobj = NULL;

      if (cmd == START)
        {
          info("%s", "Starting on JSON command");
          run_flag = true;
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
