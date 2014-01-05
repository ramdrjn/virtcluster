#ifndef _PKT_DEFINE_H_
#define _PKT_DEFINE_H_
/**
 * @file pkt-define.h
 * Packet definitions header file
 * @author RD
 * @date Sun Dec 22 15:08:17 IST 2013
 */

/**@struct udp_t
 * UDP packet definitions */
struct udp_t
{
  int sport;
  int dport;
};

/**@struct tcp_t
 * TCP packet definitions */
struct tcp_t
{
  int sport;
  int dport;
};

/**@struct l4_t
 * Layer 4 packet definitions */
struct l4_t
{
  union{
    struct udp_t udp;
    struct tcp_t tcp;
  };
};

/**@struct ipv4_t
 * IPv4 packet definitions */
struct ipv4_t
{
  int sip;
  int dip;
  int ttl;
  int protocol;
  int dscp;
  int payload_size;
  char *payload;
};

/**@struct l3_t
 * Layer 3 packet definitions */
struct l3_t
{
  struct ipv4_t ipv4;
};

/**@struct ethernet_t
 * Ethernet packet definitions */
struct ethernet_t
{
  char smac[12];
  char dmac[12];
  int ethertype;
  int payload_size;
  char *payload;
};

/**@struct l2_t
 * Layer 2 packet definitions */
struct l2_t
{
  struct ethernet_t ethernet;
};

/**@struct gen_paacket_t
 * Generator packet definitions */
struct gen_packet_t
{
  struct l2_t l2;
  struct l3_t l3;
  struct l4_t l4;
};

genErr_t process_gen_packet(void *jobj_ref, struct gen_packet_t *gen_pkt,
                            bs_lmodCls lObj, bs_mmodCls mObj);

/****************************************************************************/
#endif /*_PKT_DEFINE_H_*/
