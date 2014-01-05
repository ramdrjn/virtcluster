/**
 * @file pkt-define.c
 * Contains packet definitions
 * @author RD
 * @date Sun Jan  5 09:57:32 IST 2014
 */

#include "cpackgen.h"
#include "_pkt.h"

static bs_mmodCls mObj = NULL;

genErr_t
process_ethernet(void *jobj_ref, struct gen_packet_t *gen_pkt, bs_lmodCls lObj)
{
  debug ("In function %s", __FUNCTION__);
  struct json_object *jobj = (struct json_object *)jobj_ref;
  void *tjobj = NULL;

  tjobj=get_val_from_key(jobj, "smac", lObj);
  if(tjobj)
    {
      strcpy(gen_pkt->l2.ethernet.smac, get_string(tjobj, lObj));
      debug ("smac value %s", gen_pkt->l2.ethernet.smac);
      free_json_obj(tjobj);
    }
  else
    {
      debug ("%s", "smac not available");
    }

  tjobj=get_val_from_key(jobj, "dmac", lObj);
  if(tjobj)
    {
      strcpy(gen_pkt->l2.ethernet.dmac, get_string(tjobj, lObj));
      debug ("dmac value %s", gen_pkt->l2.ethernet.dmac);
      free_json_obj(tjobj);
    }
  else
    {
      debug ("%s", "dmac not available");
    }

  tjobj=get_val_from_key(jobj, "ethertype", lObj);
  if(tjobj)
    {
      gen_pkt->l2.ethernet.ethertype = get_int(tjobj, lObj);
      debug ("ethertype value %d", gen_pkt->l2.ethernet.ethertype);
      free_json_obj(tjobj);
    }
  else
    {
      debug ("%s", "ethertype not available");
    }

  tjobj=get_val_from_key(jobj, "payload", lObj);
  if(tjobj)
    {
      genErr_t retVal;
      void *ptr = NULL;
      const char *p_ptr = get_string(tjobj, lObj);

      gen_pkt->l2.ethernet.payload_size = strlen(p_ptr);

      retVal = bs_allocMem(mObj, gen_pkt->l2.ethernet.payload_size, &ptr);
      if (retVal != SUCCESS)
        {
          error ("%s", "Allocation memory for json input failed");
          return (retVal);
        }
      gen_pkt->l2.ethernet.payload = (char *)ptr;

      strncpy(gen_pkt->l2.ethernet.payload, p_ptr,
              gen_pkt->l2.ethernet.payload_size);
      debug ("payload value %s and length %d", gen_pkt->l2.ethernet.payload,
             gen_pkt->l2.ethernet.payload_size);
      free_json_obj(tjobj);
    }
  else
    {
      debug ("%s", "payload not available");
    }

  return (SUCCESS);
}

genErr_t
process_ipv4(void *jobj_ref, struct gen_packet_t *gen_pkt, bs_lmodCls lObj)
{
  debug ("In function %s", __FUNCTION__);
  struct json_object *jobj = (struct json_object *)jobj_ref;
  void *tjobj = NULL;

  tjobj=get_val_from_key(jobj, "sip", lObj);
  if(tjobj)
    {
      gen_pkt->l3.ipv4.sip = get_int(tjobj, lObj);
      debug ("sip value %d", gen_pkt->l3.ipv4.sip);
      free_json_obj(tjobj);
    }
  else
    {
      debug ("%s", "sip not available");
    }

  tjobj=get_val_from_key(jobj, "dip", lObj);
  if(tjobj)
    {
      gen_pkt->l3.ipv4.dip = get_int(tjobj, lObj);
      debug ("dip value %d", gen_pkt->l3.ipv4.dip);
      free_json_obj(tjobj);
    }
  else
    {
      debug ("%s", "dip not available");
    }

  tjobj=get_val_from_key(jobj, "ttl", lObj);
  if(tjobj)
    {
      gen_pkt->l3.ipv4.ttl = get_int(tjobj, lObj);
      debug ("ttl value %d", gen_pkt->l3.ipv4.ttl);
      free_json_obj(tjobj);
    }
  else
    {
      debug ("%s", "ttl not available");
    }

  tjobj=get_val_from_key(jobj, "protocol", lObj);
  if(tjobj)
    {
      gen_pkt->l3.ipv4.protocol = get_int(tjobj, lObj);
      debug ("protocol value %d", gen_pkt->l3.ipv4.protocol);
      free_json_obj(tjobj);
    }
  else
    {
      debug ("%s", "protocol not available");
    }

  tjobj=get_val_from_key(jobj, "dscp", lObj);
  if(tjobj)
    {
      gen_pkt->l3.ipv4.dscp = get_int(tjobj, lObj);
      debug ("dscp value %d", gen_pkt->l3.ipv4.dscp);
      free_json_obj(tjobj);
    }
  else
    {
      debug ("%s", "dscp not available");
    }

  tjobj=get_val_from_key(jobj, "payload", lObj);
  if(tjobj)
    {
      genErr_t retVal;
      void *ptr = NULL;
      const char *p_ptr = get_string(tjobj, lObj);

      gen_pkt->l3.ipv4.payload_size = strlen(p_ptr);

      retVal = bs_allocMem(mObj, gen_pkt->l3.ipv4.payload_size, &ptr);
      if (retVal != SUCCESS)
        {
          error ("%s", "Allocation memory for json input failed");
          return (retVal);
        }
      gen_pkt->l3.ipv4.payload = (char *)ptr;

      strncpy(gen_pkt->l3.ipv4.payload, p_ptr,
              gen_pkt->l3.ipv4.payload_size);
      debug ("payload value %s and length %d", gen_pkt->l3.ipv4.payload,
             gen_pkt->l3.ipv4.payload_size);
      free_json_obj(tjobj);
    }
  else
    {
      debug ("%s", "payload not available");
    }

  return (SUCCESS);
}

genErr_t
process_udp(void *jobj_ref, struct gen_packet_t *gen_pkt, bs_lmodCls lObj)
{
  debug ("In function %s", __FUNCTION__);
  struct json_object *jobj = (struct json_object *)jobj_ref;
  void *tjobj = NULL;

  tjobj=get_val_from_key(jobj, "sport", lObj);
  if(tjobj)
    {
      gen_pkt->l4.udp.sport = get_int(tjobj, lObj);
      debug ("udp source port value %d", gen_pkt->l4.udp.sport);
      free_json_obj(tjobj);
    }
  else
    {
      debug ("%s", "source port not available");
    }

  tjobj=get_val_from_key(jobj, "dport", lObj);
  if(tjobj)
    {
      gen_pkt->l4.udp.dport = get_int(tjobj, lObj);
      debug ("udp destination port value %d", gen_pkt->l4.udp.dport);
      free_json_obj(tjobj);
    }
  else
    {
      debug ("%s", "destination port not available");
    }

  return (SUCCESS);
}

genErr_t
process_tcp(void *jobj_ref, struct gen_packet_t *gen_pkt, bs_lmodCls lObj)
{
  debug ("In function %s", __FUNCTION__);
  struct json_object *jobj = (struct json_object *)jobj_ref;
  void *tjobj = NULL;

  tjobj=get_val_from_key(jobj, "sport", lObj);
  if(tjobj)
    {
      gen_pkt->l4.tcp.sport = get_int(tjobj, lObj);
      debug ("tcp source port value %d", gen_pkt->l4.tcp.sport);
      free_json_obj(tjobj);
    }
  else
    {
      debug ("%s", "source port not available");
    }

  tjobj=get_val_from_key(jobj, "dport", lObj);
  if(tjobj)
    {
      gen_pkt->l4.tcp.dport = get_int(tjobj, lObj);
      debug ("tcp destination port value %d", gen_pkt->l4.tcp.dport);
      free_json_obj(tjobj);
    }
  else
    {
      debug ("%s", "destination port not available");
    }

  return (SUCCESS);
}

genErr_t
process_l2(void *jobj_ref, struct gen_packet_t *gen_pkt, bs_lmodCls lObj)
{
  debug ("In function %s", __FUNCTION__);
  struct json_object *jobj = (struct json_object *)jobj_ref;
  void *tjobj = NULL;

  tjobj=get_val_from_key(jobj, "ethernet", lObj);
  if(tjobj)
    {
      process_ethernet(tjobj, gen_pkt, lObj);
      free_json_obj(tjobj);
    }
  else
    {
      debug ("%s", "ethernet not available");
    }

  return (SUCCESS);
}

genErr_t
process_l3(void *jobj_ref, struct gen_packet_t *gen_pkt, bs_lmodCls lObj)
{
  debug ("In function %s", __FUNCTION__);
  struct json_object *jobj = (struct json_object *)jobj_ref;
  void *tjobj = NULL;

  tjobj=get_val_from_key(jobj, "ipv4", lObj);
  if(tjobj)
    {
      process_ipv4(tjobj, gen_pkt, lObj);
      free_json_obj(tjobj);
    }
  else
    {
      debug ("%s", "ipv4 not available");
    }

  return (SUCCESS);
}

genErr_t
process_l4(void *jobj_ref, struct gen_packet_t *gen_pkt, bs_lmodCls lObj)
{
  debug ("In function %s", __FUNCTION__);
  struct json_object *jobj = (struct json_object *)jobj_ref;
  void *tjobj = NULL;

  tjobj=get_val_from_key(jobj, "udp", lObj);
  if(tjobj)
    {
      process_udp(tjobj, gen_pkt, lObj);
      free_json_obj(tjobj);
    }
  else
    {
      debug ("%s", "udp not available");
    }

  tjobj=get_val_from_key(jobj, "tcp", lObj);
  if(tjobj)
    {
      process_tcp(tjobj, gen_pkt, lObj);
      free_json_obj(tjobj);
    }
  else
    {
      debug ("%s", "tcp not available");
    }

  return (SUCCESS);
}

genErr_t
process_gen_packet(void *jobj_ref, struct gen_packet_t *gen_pkt,
                   bs_lmodCls lObj, bs_mmodCls mObj_ref)
{
  debug ("In function %s", __FUNCTION__);

  struct json_object *jobj = (struct json_object *)jobj_ref;
  void *tjobj = NULL;

  mObj=mObj_ref;

  tjobj=get_val_from_key(jobj, "l2", lObj);
  if(tjobj)
    {
      process_l2(tjobj, gen_pkt, lObj);
      free_json_obj(tjobj);
    }
  else
    {
      debug ("%s", "l2 not available");
    }

  tjobj=get_val_from_key(jobj, "l3", lObj);
  if(tjobj)
    {
      process_l3(tjobj, gen_pkt, lObj);
      free_json_obj(tjobj);
    }
  else
    {
      debug ("%s", "l3 not available");
    }

  tjobj=get_val_from_key(jobj, "l4", lObj);
  if(tjobj)
    {
      process_l4(tjobj, gen_pkt, lObj);
      free_json_obj(tjobj);
    }
  else
    {
      debug ("%s", "l4 not available");
    }

  return (SUCCESS);
}

/****************************************************************************/
