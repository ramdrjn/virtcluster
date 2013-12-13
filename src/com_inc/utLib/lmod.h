#ifndef _LMOD_H_
#define _LMOD_H_
/**
 * @file lmod.h
 * Log module header containing interface declarations.
 * @author RD
 * @date Mon Jan 26 20:06:57 EET 2009
 */

/**@typedef bs_lmodCls
 * Log object class.*/
typedef struct bs_lmodClsType *bs_lmodCls;

/**@enum bs_e_logLvl
 * Log levels- debug, info or error levels.*/
typedef enum
  {
    LVL_DEBUG,
    LVL_INFO,
    LVL_ERROR
  } bs_e_logLvl;

/**@enum bs_e_logMode
 * Log modes- print screen only or log in file also.*/
typedef enum
  {
    PO_LOG = 1,
    PF_LOG = 2
  } bs_e_logMode;

/*Prototypes*/
genErr_t bs_lmodInit (bs_lmodCls * lObjPtr, int syslog, int quite,
                      int verbose, bs_fmodCls fileObj, bs_mmodCls mObj);
genErr_t bs_lmodFin (bs_lmodCls * lObjPtr, bs_mmodCls mObj);
void bs_setQuite (bs_lmodCls lObj);
void bs_setVerbose (bs_lmodCls lObj);
void bs_unsetQuite (bs_lmodCls lObj);
void bs_unsetVerbose (bs_lmodCls lObj);
void bs_log (bs_lmodCls lObj, bs_e_logLvl lvl, bs_e_logMode mode,
             const char *fmt, ...);

/****************************************************************************/
#endif /*_LMOD_H_*/
