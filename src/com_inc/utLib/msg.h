#ifndef _MSG_H_
#define _MSG_H_

/**
 * @file msg.h
 * Message library interfaces.
 * @author RD
 * @date Sat Jul 23 21:16:57 IST 2011
 */

/**@typedef msg_base
 * Message base class.*/
typedef struct msg_baseType *msg_base;

/**@enum msg_e_connType
 * Indicates the connection type.
 * STREAM - TCP reliable.
 * DGRAM - UDP unreliable and
 * PMSGQ - POsix message Q.
 */
typedef enum
  {
    MSG_STREAM = 0,
    MSG_DGRAM,
    MSG_PMSGQ
  } msg_e_connType;

/**@enum msg_e_shutMode
 * Indicates the shutdown mode.
 */
typedef enum
  {
    MSG_SHRD = 0,
    MSG_SHWR,
    MSG_SHRDWR
  } msg_e_shutMode;

/**@def NODE_ID_SIZE
 * The maximum size of node id */
#define NODE_ID_SIZE 128

/**@def APP_ID_SIZE
 * The maximum size of app id */
#define APP_ID_SIZE 4

/**@struct msg_addrType
 * Address class Type. */
struct msg_addrType
{
  char nodeID[NODE_ID_SIZE];
  char appID[APP_ID_SIZE];
};

/**@typedef msg_addr
 * Message address class.*/
typedef struct msg_addrType *msg_addr;

/**@enum msg_e_opts
 * Various options that cen be set for the socket
 */
typedef enum
  {
    MSG_REUSE_ADDR = 0,
    MSG_NO_BLOCK
  } msg_e_opts;

/*Prototypes*/
inline genErr_t msg_baseInit (msg_base *msgPtr, bs_mmodCls mObj);
inline genErr_t msg_setAddr (msg_base msgPtr, msg_e_connType type,
                             msg_addr selfAddr, msg_addr remoteAddr);
inline genErr_t msg_baseFin (msg_base *msgPtr, bs_mmodCls mObj);
inline genErr_t msg_setOptions (msg_base msgPtr, msg_e_opts opt, int value);
inline genErr_t msg_bind (msg_base msgPtr);
inline genErr_t msg_connect (msg_base msgPtr);
inline genErr_t msg_listen (msg_base msgPtr, int backlog);
inline genErr_t msg_accept (msg_base msgPtr, msg_base *newPtr, msg_addr addr);
inline genErr_t msg_shut (msg_base msgPtr, msg_e_shutMode how);
inline genErr_t msg_unlink (msg_base msgPtr);
inline genErr_t msg_sendVec (msg_base msgPtr, int *retCount, vec_io vec);
inline genErr_t msg_recvVec (msg_base msgPtr, int *retCount, vec_io vec);
inline genErr_t msg_sendBuf (msg_base msgPtr, int *retCount, char *buf,
                             int len, priority_t prio);
inline genErr_t msg_recvBuf (msg_base msgPtr, int *retCount, char *buf,
                             int len, priority_t *prio);

/****************************************************************************/
#endif /*_MSG_H__*/
