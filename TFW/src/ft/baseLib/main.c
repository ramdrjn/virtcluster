/****************************************************************************
 *                                                                          * 
 *                                                                          * 
 ****************************************************************************/

#include "_proto.h"

/****************************************************************************
 * Main function call. Invoke all test cases from here.                     *
 ****************************************************************************/
int
main (int argc, char *argv[])
{
  (void)argc;
  (void)argv;

  init ();

  hdr ("Starting to run the test cases.");

  test_emod ();

  test_mmod ();

  test_fmod ();

  test_lmod ();

  test_omod ();

  test_smod ();

  test_tmod ();

  hdr ("Test case run finished execution.");

  fin ();

  return 0;
}

/****************************************************************************/
