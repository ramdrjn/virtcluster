#ifndef _GEN_TYPES_H_
#define _GEN_TYPES_H_
/**
 * @file gentypes.h
 * General header containing basic types.
 * @author RD
 * @date Wed Aug 10 22:09:06 IST 2011
 */

/*to be included after gen.h*/

#include <stdint.h>

#define PRIVATE static

/**@enum e_bool
 * The \c true (\b 1) or \c false (\b 0) boolean enum.*/
typedef enum
  {
    false = 0,
    true = 1
  } e_bool;

//bool type.
typedef e_bool t_bool;

//Unsigned types.
typedef uint32_t t_uint32;
typedef uint16_t t_uint16;
typedef uint8_t t_uint8;
typedef uint64_t t_uint64;

//Signed types.
typedef int32_t t_int32;
typedef int16_t t_int16;
typedef int8_t t_int8;
typedef int64_t t_int64;

/****************************************************************************/
#endif /*_GEN_TYPES_H_*/
