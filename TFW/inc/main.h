#ifndef _MAIN_H_
#define _MAIN_H_
/****************************************************************************
 * 									    *
 *									    *
 ****************************************************************************/

#include "gen.h"
#include "generr.h"
#include "gentypes.h"
#include "utLib/mmod.h"
#include "utLib/fmod.h"
#include "utLib/lmod.h"

#include <sys/wait.h>

extern bs_mmodCls iMObj;
extern bs_lmodCls iLObj;
typedef struct tstCaseParamClsType tstCaseParamCls;
extern tstCaseParamCls tstCase;
extern int retVal;

#define blank()       bs_log(iLObj, LVL_INFO, PO_LOG, "\n", 0)
#define hdr(msg)      bs_log(iLObj, LVL_INFO, PO_LOG, "\n# %s", msg)
#define res(fmt, ...) bs_log(iLObj, LVL_INFO, PO_LOG, "\n\t\t= "fmt, __VA_ARGS__)
#define err(fmt, ...) bs_log(iLObj, LVL_INFO, PO_LOG, "\nX "fmt, __VA_ARGS__)
#define inf(fmt, ...) bs_log(iLObj, LVL_INFO, PO_LOG, "\n\t! "fmt, __VA_ARGS__)
#define data(fmt, ...) bs_log(iLObj, LVL_INFO, PO_LOG, "\n\t\t -> "fmt, __VA_ARGS__)

/* Flags for test cases.*/
#define HALT_ON_ERROR 0x01	/*If 1 means that the test sequence will \
				  abort if any test fails. */

/*Prototypes for some common functions.*/
void init (void);
void fin (void);
void EXEC_TSTCASE (tstCaseParamCls * tstcp, char *desc, int cond, int retval,
                   char *errmsg, int flags);
void EXEC_SH (tstCaseParamCls * tstcp, const char *cmd, char *desc,
              int flags);

/****************************************************************************/
#endif /*_MAIN_H_*/
