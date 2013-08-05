#ifndef _I_TSKMOD_H_
#define _I_TSKMOD_H_
/**
 * @file _tskmod.h
 * Internal task module header
 * @author RD
 * @date Sun May 26 16:20:42 IST 2013
 */

#include "gen.h"
#include "generr.h"
#include "gentypes.h"
#include "utLib/mmod.h"
#include "utLib/tskmod.h"
#include <pthread.h>
#include <sys/wait.h>

/**@struct bs_tskmodClsType
 * Task object class Type. */
struct bs_tskmodClsType
{
  t_bool _validFlag;
  pid_t _pid;
  pthread_t _tid;
  t_bool _parent;
  bs_e_tskType _type;
  bs_tskmodCls _child;
  int _num_child;
  bs_tskmodCls _nextPtr;
};

/**@struct bs_tskArgsType
 * Argument Type used to pass arguments to callback handler */
typedef struct
{
  bs_tskmodCls tskPtr;
  bs_spawnCBType spawnCB;
  char **argv;
  bs_mmodCls mObj;
}bs_tskArgsType;

/*Internal Prototypes*/
PRIVATE genErr_t bs_threadFun (void *argsPtr);

/****************************************************************************/
#endif /*_I_TSKMOD_H_*/
