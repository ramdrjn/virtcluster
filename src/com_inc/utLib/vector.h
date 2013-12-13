#ifndef _VECTOR_H_
#define _VECTOR_H_
/**
 * @file vector.h
 * Vector IO module. Used in file and socket modules.
 * @author RD
 * @date Sun Aug  7 23:13:01 IST 2011
 */

#include <sys/uio.h>

/**@typedef priority_t
 * Message priority type*/
typedef unsigned int priority_t;

/**@struct vec_ioType
 * vector of io base */
struct vec_ioType
{
  struct iovec *ioVecPtr;
  int vecCount;
  priority_t priority;
};

/**@typedef vec_io
 * vector IO.*/
typedef struct vec_ioType *vec_io;


/****************************************************************************/
#endif /*_VECTOR_H_*/
