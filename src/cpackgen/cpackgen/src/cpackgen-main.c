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

/**
 * Main
 */
int main(int argc, char *argv[])
{
  genErr_t retVal;
  char *input = NULL;
  char *mode = NULL;
  bs_mmodCls mObj = NULL;
  bs_fmodCls fObj = NULL;
  bs_lmodCls lObj = NULL;
  const char *debug_fname = "/tmp/cpackgen-debug";

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
  if (retVal != SUCCESS)
    {
      _exit_cleanup(mObj, fObj, lObj);
      return (retVal);
    }

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

  if (lObj == NULL)
    return (retVal);

  debug ("%s", "Starting cpackgen");

  retVal = bs_allocMem(mObj, 1024, (void *)&input);
  if (retVal != SUCCESS)
    {
      error ("%s", "Allocation memory for json input failed");
      _exit_cleanup(mObj, fObj, lObj);
      return (retVal);
    }

  mode = argv[1];
  info ("%s %s", "Starting in mode:", mode);

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
