#ifndef _PKT_FORM_H_
#define _PKT_FORM_H_
/**
 * @file pkt-form.h
 * Internal Packet formation header file
 * @author RD
 * @date Sun Dec 22 15:08:17 IST 2013
 */

#include "pkt-define.h"

genErr_t gen_packet_form(struct gen_packet_conf_t *gen_conf_ref,
                         struct gen_packet_t *gen_pkt_ref,
                         bs_lmodCls lObj_ref, bs_mmodCls mObj_ref);

/****************************************************************************/
#endif /*_PKT_FORM_H_*/
