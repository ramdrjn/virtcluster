#ifndef _I_MSG_H_
#define _I_MSG_H_

/**
 * @file _msg.h
 * Internal message implementation header.
 * @author RD
 * @date Sat Jul 23 21:05:12 IST 2011
 */

#include "gen.h"
#include "generr.h"
#include "gentypes.h"
#include "utLib/mmod.h"
#include "utLib/fmod.h"

#include "utLib/msg.h"

#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <fcntl.h>
#include <netdb.h>
#include <mqueue.h>

/**@struct msg_baseType
 * Message object class Type. */
struct msg_baseType
{
  t_bool _validFlag;

  bs_fmodCls _fObj;
  bs_mmodCls _mObj;

  msg_e_connType _connType;

  union
  {
    struct
    {
      int _sockFD;
      struct addrinfo *_self;
      struct addrinfo *_peer;
    }_sock;
    struct
    {
      int _mqFD;
      char _filename[NODE_ID_SIZE+APP_ID_SIZE+1];
    }_mq;
  }_connData;
};

/*Internal Prototypes*/
PRIVATE inline genErr_t _shut (msg_base msgPtr, msg_e_shutMode how);

/****************************************************************************/
#endif /*_I_MSG_H_*/
