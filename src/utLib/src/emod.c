/**
 * @file emod.c
 * Contains error code manipulation functions.
 * @author RD
 * @date Mon Jan 26 20:06:57 EET 2009
 */

#include "_emod.h"

const char *_errStrings[MAX_ERR_STRING_SIZE] = {
  "Unknown Error",
  "Failed",
  "Memory Allocation Failed",
  "Invalid Memory Location",
  "Invalid Object",
  "Invalid File Type",
  "Invalid Option",
  "Invalid Address",
  "Data Structure Full",
  "Duplicate Data",
  "Object Conversion Failed",
  "Address Not Set",
  "Address Info Failed",
  "Timeout",
  "End-Of-File reached",
  "JSON parse failed",
  "Invalid error code value"
};

/**
 * Return error string from error code.
 * @param err The \c error-code that needs to be converted to \c error-string.
 * @param buf A buffer where the error string needs to be stored.
 * @param size The size of the buffer. If the size and buffer are
 * \b not \b valid then the normal \c strerror function is called else if
 * they are \b valid then \c strerror_r is called.
 * @return The \c error-string for the passed \c error-code.
 */
char *
bs_ec2ES_r (genErr_t err, char *buf, size_t size)
{
  err = -err;

  if (err <= 0)
    return NULL;
  else if (err == 1)		/*Special case for "FAILED" */
    return (char *) _errStrings[err];

  if (err < ERR_BASE_VALUE)
    {
      if ((size) && (buf))
        {
#ifdef _GNU_SOURCE
          return strerror_r (err, buf, size);
#else
          strerror_r (err, buf, size);
          return NULL;
#endif
        }
      else
        return strerror (err);
    }
  err = err - ERR_BASE_VALUE;
  if ((err) && (err < MAX_ERR_STRING_SIZE))
    return (char *) _errStrings[err];
  return NULL;
}

/****************************************************************************/
