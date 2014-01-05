#ifndef _PKT_H_
#define _PKT_H_
/**
 * @file _pkt.h
 * Internal Packet definitions header file
 * @author RD
 * @date Sun Dec 22 15:08:17 IST 2013
 */

genErr_t
process_l2(void *jobj_ref, struct gen_packet_t *gen_pkt, bs_lmodCls lObj);
genErr_t
process_ethernet(void *jobj_ref, struct gen_packet_t *gen_pkt,
                 bs_lmodCls lObj);
genErr_t
process_l3(void *jobj_ref, struct gen_packet_t *gen_pkt, bs_lmodCls lObj);
genErr_t
process_ipv4(void *jobj_ref, struct gen_packet_t *gen_pkt, bs_lmodCls lObj);
genErr_t
process_l4(void *jobj_ref, struct gen_packet_t *gen_pkt, bs_lmodCls lObj);
genErr_t
process_udp(void *jobj_ref, struct gen_packet_t *gen_pkt, bs_lmodCls lObj);
genErr_t
process_tcp(void *jobj_ref, struct gen_packet_t *gen_pkt, bs_lmodCls lObj);


/****************************************************************************/
#endif /*_PKT_H_*/
