#ifndef _CPACKGEN_H_
#define _CPACKGEN_H_
/**
 * @file cpackgen.h
 * cpackgen main header file
 * @author RD
 * @date Sun Dec 22 15:08:17 IST 2013
 */

#include "json-ifc.h"
#include "pkt-define.h"

/**@enum cmd_type
 * Commands definitions.*/
typedef enum
  {
    START,
    STOP,
    PAUSE,
    RESUME,
    NIL
  } cmd_e_type;

/**@enum mode_e_type
 * Modes.*/
typedef enum
  {
    GENERATOR,
    RECEIVER
  } mode_e_type;

/**@struct gen_param_t
 * Generator parameters */
struct gen_param_t
{
  long rate_pps;
  long rate_bps;
  long max_count;
  long duration_max;
};

/**@struct conf_t
 * Configuration structure. */
struct conf_t
{
  t_bool _validFlag;
  mode_e_type mode;
  struct gen_param_t gen_params;
  struct gen_packet_t gen_packets;
};

genErr_t
process_gen_packet(void *jobj_ref, struct gen_packet_t *gen_pkt_ref,
                   bs_lmodCls lObj_ref, bs_mmodCls mObj_ref);

/****************************************************************************/
#endif /*_CPACKGEN_H_*/
