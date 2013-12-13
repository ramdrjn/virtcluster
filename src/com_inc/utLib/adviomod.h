#ifndef _ADVIOMOD_H_
#define _ADVIOMOD_H_
/**
 * @file adviomod.h
 * Advanced IO module headers.
 * @author RD
 * @date Sun Jun  9 20:44:52 IST 2013
 */

#include <sys/epoll.h>

/**@typedef bs_advioCls
 * Advanced IO class.*/
typedef struct bs_advioClsType *bs_advioCls;

/**@enum bs_e_trigType
 * poll trigger type definitions.*/
typedef enum
  {
    POL_LVL,
    POL_EDGE
  } bs_e_trigType;

/*Prototype*/
genErr_t bs_advioInit (bs_advioCls *advioPtr, bs_mmodCls mObj, t_bool poll);
genErr_t bs_advioFin (bs_advioCls *advioPtr, bs_mmodCls mObj);
genErr_t bs_pollAdd (bs_advioCls advioPtr, bs_fmodCls fObj,
                     void *udPtr, t_uint32 events);
genErr_t bs_pollRem (bs_advioCls advioPtr, bs_fmodCls fObj,
                     void *udPtr, t_uint32 events);
genErr_t bs_pollMod (bs_advioCls advioPtr, bs_fmodCls fObj,
                     void *udPtr, t_uint32 events);
genErr_t bs_poll (bs_advioCls advioPtr, int *count,
                  struct epoll_event *events, int maxevents, int timeout);

/****************************************************************************/
#endif /*_ADVIOMOD_H_*/
