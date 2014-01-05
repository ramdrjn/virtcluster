/**
 * @file pkt-form.c
 * Contains packet formation routines
 * @author RD
 * @date Sun Jan  5 09:57:32 IST 2014
 */

#include "cpackgen.h"
#include "pkt-define.h"
#include "pkt-form.h"

static bs_mmodCls mObj = NULL;
static bs_lmodCls lObj = NULL;
static struct gen_packet_conf_t *gen_pkt_conf;

genErr_t
gen_packet_form(struct gen_packet_conf_t *gen_conf_ref,
                struct gen_packet_t *gen_pkt_ref,
                bs_lmodCls lObj_ref, bs_mmodCls mObj_ref)
{
  lObj=lObj_ref;
  mObj=mObj_ref;
  gen_pkt_conf = gen_conf_ref;

  debug ("In function %s", __FUNCTION__);


  return (SUCCESS);
}

/****************************************************************************/
