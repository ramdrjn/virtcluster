#ifndef _GENERR_H_
#define _GENERR_H_
/**
 * @file generr.h
 * Error module header containing error codes declarations, functions
 * and macros to manipulate them.
 * @author RD
 * @date Mon Jan 26 20:06:57 EET 2009
 */

#include <errno.h>
#include <assert.h>

/**@typedef genErr_t
 * Error code type that will be used to deal with \c error-codes.*/
typedef int genErr_t;

/**@def validateObj
 * Validation macros for \b internal objects.*/
#define validateObj(obj) {                      \
  if (obj != NULL)                              \
    {                                           \
      if(true != (obj)->_validFlag)             \
        {                                       \
          assert(0);                            \
        }                                       \
    }                                           \
  else                                          \
    assert(0);                                  \
  }

/**@def errno2EC
 * Convert \c errno to \c error-code.*/
#define errno2EC(err) (-((genErr_t)err))

/**@def ec2ES
 * Return \c error-string corresponding to the \c error-code.*/
#define ec2ES(err) (bs_ec2ES_r(err, NULL, 0))

#ifdef _USE_DUMMY_ASSERT_
#define dummy_assert(x) {}
#define ASSERT dummy_assert
#else
/**@def ASSERT
 * ASSERT. Should be enabled in debug mode.*/
#define ASSERT assert
#endif

/*Prototype.*/
char *bs_ec2ES_r (genErr_t err, char *buf, size_t size);

/**@def ERR_BASE_VALUE
 * The \b user-defined \b error-codes start from this base value.*/
#define ERR_BASE_VALUE 65000

/* Basic error codes definitions. */
#define SUCCESS 1
#define FAILURE -1

#define UNKNOWN_ERROR       -(ERR_BASE_VALUE)
#define FAILED              -(ERR_BASE_VALUE+1)
/*Define new error codes after this.*/
#define MEM_ALLOC_FAIL      -(ERR_BASE_VALUE+2)
#define INVALID_MEM_LOC     -(ERR_BASE_VALUE+3)
#define INVALID_OBJ         -(ERR_BASE_VALUE+4)
#define INVALID_FILETYP     -(ERR_BASE_VALUE+5)
#define INVALID_OPTIONS     -(ERR_BASE_VALUE+6)
#define INVALID_ADDR        -(ERR_BASE_VALUE+7)
#define DATASTRUCT_FULL     -(ERR_BASE_VALUE+8)
#define DUPLICATE_DATA      -(ERR_BASE_VALUE+9)
#define OBJECTIFY_FAIL      -(ERR_BASE_VALUE+10)
#define ADDR_NOT_SET        -(ERR_BASE_VALUE+11)
#define ADDRINFO_FAIL       -(ERR_BASE_VALUE+12)
#define TIMEOUT             -(ERR_BASE_VALUE+13)
#define EOF_REACHED         -(ERR_BASE_VALUE+14)
#define JSON_PARSE_FAIL     -(ERR_BASE_VALUE+15)
/*Define new error codes before this.*/
#define INVALID_ERROR_CODE  -(ERR_BASE_VALUE+MAX_ERR_STRING_SIZE-1)

/****************************************************************************/
#endif /*_GENERR_H_*/
