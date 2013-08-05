/**
 * @file msg.c
 * Contains message base implementations.
 * @author RD
 * @date Sat Jul 23 21:29:13 IST 2011
 */

#include "_msg.h"

/**
 * Initialize the base.
 * @param msgPtr message base object reference.
 * @param mObj memory object that will be used for allocations.
 * @return The \c error-code else success is returned.
 */
inline genErr_t
msg_baseInit (msg_base *msgPtr, bs_mmodCls mObj)
{
  void *ptr = NULL;

  genErr_t retVal = SUCCESS;

  if(msgPtr == NULL)
    return INVALID_MEM_LOC;
  *msgPtr = NULL;

  retVal = bs_allocMem (mObj, sizeof (struct msg_baseType), &ptr);
  if (retVal != SUCCESS)
    return retVal;

  *msgPtr = (msg_base) ptr;

  (*msgPtr)->_validFlag = true;
  (*msgPtr)->_connData._sock._sockFD = -1;
  (*msgPtr)->_connData._mq._mqFD = -1;
  (*msgPtr)->_mObj = mObj;

  return SUCCESS;
}

/**
 * Finalize the base object. The valid flag is unset.
 * @param msgPtr Reference of the object.
 * @param mObj that will be used for memory operations.
 * @note In case of error while closing the socket the operation continues
 * and frees the object pointer. No action is taken for the failure.
 * @return The \c error-code else success is returned.
 */
inline genErr_t
msg_baseFin (msg_base *msgPtr, bs_mmodCls mObj)
{
  int rc;
  genErr_t retVal;

  validateObj (*msgPtr);

  if ((*msgPtr)->_connType != MSG_PMSGQ)
    {
      rc = _shut(*msgPtr, MSG_SHRDWR);
      if (rc == -1)
        retVal = errno2EC (errno);

      rc = close((*msgPtr)->_connData._sock._sockFD);
      if (rc == -1)
        retVal = errno2EC (errno);

      if((*msgPtr)->_connData._sock._self)
        {
          freeaddrinfo((*msgPtr)->_connData._sock._self);
          (*msgPtr)->_connData._sock._self = NULL;
        }
      if((*msgPtr)->_connData._sock._peer)
        {
          freeaddrinfo((*msgPtr)->_connData._sock._peer);
          (*msgPtr)->_connData._sock._peer = NULL;
        }
    }
  else
    {
      rc = mq_close((*msgPtr)->_connData._mq._mqFD);
      if (rc == -1)
        retVal = errno2EC (errno);
    }

  (*msgPtr)->_validFlag = false;

  if((*msgPtr)->_fObj)
    {
      retVal = bs_fmodFin (&(*msgPtr)->_fObj, mObj);
    }

  (*msgPtr)->_mObj = NULL;

  retVal = bs_freeMem (mObj, (void *)msgPtr);

  return retVal;
}

/**
 * Sets the self address (for bind) and the remote address. The
 * function also creates the sockets (depending upon the address).
 * @note Use blank addr for any addr in case of bind
 * @param msgPtr message base object reference.
 * @param type connection type.
 * @param selfAddr The self addr. Mostly applicable for servers. Can be NULL.
 * @param remoteAddr The peer address. Can be NULL in cases of servers.
 * @return The \c error-code else success is returned.
 */
inline genErr_t
msg_setAddr (msg_base msgPtr, msg_e_connType type,
             msg_addr selfAddr, msg_addr remoteAddr)
{
  genErr_t retVal = SUCCESS;

  validateObj (msgPtr);

  msgPtr->_connType = type;

  if (type != MSG_PMSGQ)
    {
      int rc=0;
      int sockType = (type == MSG_STREAM)?SOCK_STREAM:SOCK_DGRAM;
      int family = AF_UNSPEC;
      int protocol = 0;

      struct addrinfo hints;

      SET_ZERO(hints);

      if(selfAddr)
        {
          int nodeIDLen = strlen(selfAddr->nodeID);

          hints.ai_family = AF_UNSPEC;
          hints.ai_socktype = sockType;
          hints.ai_flags = (nodeIDLen==0)?AI_PASSIVE:0;
          hints.ai_flags |= AI_NUMERICSERV;

          rc = getaddrinfo((nodeIDLen!=0)?selfAddr->nodeID:NULL,
                           (strlen(selfAddr->appID)!=0)?selfAddr->appID:NULL,
                           &hints, &msgPtr->_connData._sock._self);

          if (rc != 0)
            {
              //              printf("%s", gai_strerror(rc));
              return ADDRINFO_FAIL;
            }

          sockType = msgPtr->_connData._sock._self->ai_socktype;
          family = msgPtr->_connData._sock._self->ai_family;
          protocol = msgPtr->_connData._sock._self->ai_protocol;
        }

      if(remoteAddr)
        {
          if ((strlen(remoteAddr->nodeID) == 0) ||
              (strlen(remoteAddr->appID) == 0))
            return INVALID_ADDR;

          hints.ai_family = AF_UNSPEC;
          hints.ai_socktype = sockType;
          hints.ai_flags = AI_NUMERICSERV;

          rc = getaddrinfo(remoteAddr->nodeID, remoteAddr->appID, &hints,
                           &msgPtr->_connData._sock._peer);

          if (rc != 0)
            {
              //              printf("%s", gai_strerror(rc));
              return ADDRINFO_FAIL;
            }

          sockType = msgPtr->_connData._sock._peer->ai_socktype;
          family = msgPtr->_connData._sock._peer->ai_family;
          protocol = msgPtr->_connData._sock._peer->ai_protocol;
        }

      rc = socket(family, sockType, protocol);

      if (rc == -1)
        return errno2EC (errno);

      msgPtr->_connData._sock._sockFD = rc;
    }
  else
    {
      /*Posix message queue*/
      mqd_t rc=0;

      SET_ZERO(msgPtr->_connData._mq._filename);

      if(selfAddr)
        {
          if ((strlen(selfAddr->nodeID) == 0) ||
              (strlen(selfAddr->appID) == 0))
            return INVALID_ADDR;

          strncpy(msgPtr->_connData._mq._filename, "/", 1);
          strncat(msgPtr->_connData._mq._filename,
                  selfAddr->nodeID, NODE_ID_SIZE);
          strncat(msgPtr->_connData._mq._filename,
                  selfAddr->appID, APP_ID_SIZE);

          rc = mq_open(msgPtr->_connData._mq._filename,
                       O_RDWR|O_CREAT|O_EXCL, 0777, 0);
          if (rc == -1)
            return errno2EC (errno);
        }

      if(remoteAddr)
        {
          if ((strlen(remoteAddr->nodeID) == 0) ||
              (strlen(remoteAddr->appID) == 0))
            return INVALID_ADDR;

          strncpy(msgPtr->_connData._mq._filename, "/", 1);
          strncat(msgPtr->_connData._mq._filename,
                  remoteAddr->nodeID, NODE_ID_SIZE);
          strncat(msgPtr->_connData._mq._filename,
                  remoteAddr->appID, APP_ID_SIZE);

          rc = mq_open(msgPtr->_connData._mq._filename, O_RDWR);
          if (rc == -1)
            return errno2EC (errno);
        }
      msgPtr->_connData._mq._mqFD = rc;
    }

  retVal = bs_fmodInit (&msgPtr->_fObj, msgPtr->_mObj);
  if(retVal == SUCCESS)
    {
      if (type != MSG_PMSGQ)
        {
          retVal = bs_fObjectify(msgPtr->_connData._sock._sockFD,
                                 msgPtr->_fObj);
        }
      else
        {
          retVal = bs_fObjectify(msgPtr->_connData._mq._mqFD,
                                 msgPtr->_fObj);
        }
      if(retVal != SUCCESS)
        {
          bs_fmodFin(&msgPtr->_fObj, msgPtr->_mObj);
        }
    }
  if(msgPtr->_fObj)
    retVal = OBJECTIFY_FAIL;

  return retVal;
}

/**
 * Set options for the socket.
 * @param msgPtr base object reference.
 * @param opt Various options that can be set for the socket.
 * @param value The value for the option, whether to set or reset the option.
 * @return The \c error-code else success is returned.
 */
inline genErr_t
msg_setOptions (msg_base msgPtr, msg_e_opts opt, int value)
{
  genErr_t retVal = SUCCESS;

  validateObj (msgPtr);

  if((msgPtr->_connType != MSG_PMSGQ) &&
     (msgPtr->_connData._sock._sockFD == -1))
    return ADDR_NOT_SET;

  switch(opt)
    {
    case MSG_REUSE_ADDR:
      {
        int rc;
        if(msgPtr->_connType == MSG_PMSGQ)
          {
            retVal = SUCCESS;
            break;
          }
        rc = setsockopt (msgPtr->_connData._sock._sockFD,
                         SOL_SOCKET, SO_REUSEADDR,
                         &value, sizeof(int));
        if (rc  == -1)
          retVal = errno2EC (errno);
      }
      break;
    case MSG_NO_BLOCK:
      {
        if(msgPtr->_connType == MSG_PMSGQ)
          {
            retVal = SUCCESS;
            break;
          }

        if(msgPtr->_fObj != NULL)
          {
            retVal = bs_fOpts (msgPtr->_fObj, F_SETFL, &value);
          }
        else
          {
            retVal = INVALID_OBJ;
          }
      }
      break;
    default:
      retVal = INVALID_OPTIONS;
    }

  return retVal;
}

/**
 * Bind address with socket object.
 * @param msgPtr base object reference.
 * @param addr address of the self node.
 * @return The \c error-code else success is returned.
 */
inline genErr_t
msg_bind (msg_base msgPtr)
{
  validateObj (msgPtr);

  if((msgPtr->_connData._mq._mqFD == -1) &&
     (msgPtr->_connData._sock._sockFD == -1))
    return ADDR_NOT_SET;

  if(msgPtr->_connType != MSG_PMSGQ)
    {
      int rc;

      rc = bind(msgPtr->_connData._sock._sockFD,
                msgPtr->_connData._sock._self->ai_addr,
                msgPtr->_connData._sock._self->ai_addrlen);
      if (rc  == -1)
        return errno2EC (errno);
    }

  return SUCCESS;
}

/**
 * Connect to peer.
 * @param msgPtr base object reference.
 * @return The \c error-code else success is returned.
 */
inline genErr_t
msg_connect (msg_base msgPtr)
{
  validateObj (msgPtr);

  if((msgPtr->_connData._mq._mqFD == -1) &&
     (msgPtr->_connData._sock._sockFD == -1))
    return ADDR_NOT_SET;

  if(msgPtr->_connType != MSG_PMSGQ)
    {
      int rc;

      rc = connect (msgPtr->_connData._sock._sockFD,
                    msgPtr->_connData._sock._peer->ai_addr,
                    msgPtr->_connData._sock._peer->ai_addrlen);
      if (rc  == -1)
        return errno2EC (errno);
    }

  return SUCCESS;
}

/**
 * Make socket listen-able.
 * @param msgPtr base object reference.
 * @param backlog
 * @return The \c error-code else success is returned.
 */
inline genErr_t
msg_listen (msg_base msgPtr, int backlog)
{
  validateObj (msgPtr);

  if(msgPtr->_connType != MSG_PMSGQ)
    {
      int rc;

      rc = listen (msgPtr->_connData._sock._sockFD, backlog);
      if (rc  == -1)
        return errno2EC (errno);
    }

  return SUCCESS;
}

/**
 * Accept a new connection from peer.
 * @param msgPtr base object reference.
 * @param newPtr new object for the accepted connection.
 * @note addr and newPtr only applicable for sockets.
 * @param addr reference for storing address of the remote node.
 * @return The \c error-code else success is returned.
 */
inline genErr_t
msg_accept (msg_base msgPtr, msg_base *newPtr, msg_addr addr)
{
  validateObj (msgPtr);

  if(msgPtr->_connType != MSG_PMSGQ)
    {
      int rc;
      genErr_t retVal;

      struct sockaddr peerAddr;

      socklen_t sockLen = 0;

      SET_ZERO(peerAddr);

      retVal = msg_baseInit (newPtr, msgPtr->_mObj);
      if(retVal != SUCCESS)
        return retVal;

      rc = accept (msgPtr->_connData._sock._sockFD, &peerAddr, &sockLen);
      if (rc  == -1)
        return errno2EC (errno);

      if(addr != NULL)
        {
          inet_ntop(msgPtr->_connData._sock._self->ai_family, &peerAddr,
                    addr->nodeID, sockLen);
          snprintf(addr->appID, APP_ID_SIZE, "%d",
                   (peerAddr.sa_family == AF_INET)?
                   ((struct sockaddr_in*)&peerAddr)->sin_port:
                   ((struct sockaddr_in6*)&peerAddr)->sin6_port);
        }

      if(*newPtr != NULL)
        {
          //Store the new socket fd.
          (*newPtr)->_connData._sock._sockFD = rc;
          (*newPtr)->_connType = msgPtr->_connType;
        }
    }

  return SUCCESS;
}

/**
 * Internal shutdown routine.
 * @note applicable for sockets only.
 * @param msgPtr base object reference.
 * @param how whether to shut read, write or both.
 * @return The \c error-code else success is returned.
 */
PRIVATE inline genErr_t
_shut (msg_base msgPtr, msg_e_shutMode how)
{
  int rc;

  int mode = (how == MSG_SHRD)?SHUT_RD:((how == MSG_SHWR)?SHUT_WR:SHUT_RDWR);

  rc = shutdown (msgPtr->_connData._sock._sockFD, mode);
  if (rc  == -1)
    return errno2EC (errno);

  return SUCCESS;
}

/**
 * Shutdown but not close a connection.
 * @note applicable for sockets only.
 * @param msgPtr base object reference.
 * @param how whether to shut read, write or both.
 * @return The \c error-code else success is returned.
 */
inline genErr_t
msg_shut (msg_base msgPtr, msg_e_shutMode how)
{
  validateObj (msgPtr);

  if(msgPtr->_connType == MSG_PMSGQ)
    {
      return SUCCESS;
    }

  return _shut (msgPtr, how);
}

/**
 * Unlink (removes) the posix message queue file
 * @note applicable for mq only.
 * @param msgPtr base object reference.
 * @return The \c error-code else success is returned.
 */
inline genErr_t
msg_unlink (msg_base msgPtr)
{
  int rc;

  validateObj (msgPtr);

  if(msgPtr->_connType != MSG_PMSGQ)
    {
      return SUCCESS;
    }

  rc = mq_unlink(msgPtr->_connData._mq._filename);
  if (rc  == -1)
    return errno2EC (errno);

  return SUCCESS;
}

/*IO routines*/

/**
 * Send buffer to peer.
 * @param msgPtr base object reference.
 * @param retCount the number of bytes sent.
 * @param buf The buffer whose contents needs to be transferred out.
 * @param len length of buffer.
 * @param priority The priority of the message.
 * @return The \c error-code else success is returned.
 */
inline genErr_t
msg_sendBuf (msg_base msgPtr, int *retCount, char *buf, int len,
             priority_t prio)
{
  genErr_t retVal;
  struct vec_ioType vec;
  struct iovec iov;

  validateObj (msgPtr);

  iov.iov_base = buf;
  iov.iov_len = len;
  vec.ioVecPtr = &iov;
  vec.vecCount = 1;
  vec.priority = prio;

  retVal = msg_sendVec (msgPtr, retCount, &vec);

  return retVal;
}

/**
 * Receive to buffer from peer.
 * @param msgPtr base object reference.
 * @param retCount the number of bytes sent.
 * @param buf The buffer where received content is stored
 * @param len length of buffer
 * @param priority The priority of the message.
 * @return The \c error-code else success is returned.
 */
inline genErr_t
msg_recvBuf (msg_base msgPtr, int *retCount, char *buf, int len,
             priority_t *prio)
{
  genErr_t retVal;
  struct vec_ioType vec;
  struct iovec iov;

  validateObj (msgPtr);

  iov.iov_base = buf;
  iov.iov_len = len;
  vec.ioVecPtr = &iov;
  vec.vecCount = 1;
  vec.priority = 0;

  retVal = msg_sendVec (msgPtr, retCount, &vec);

  *prio = vec.priority;

  return retVal;
}

/**
 * Send message to peer.
 * @note Send irrespective of protocols.
 * @param msgPtr base object reference.
 * @param retCount the number of bytes sent.
 * @param msgVec the vector base of buffers.
 * @return The \c error-code else success is returned.
 */
inline genErr_t
msg_sendVec (msg_base msgPtr, int *retCount, vec_io vec)
{
  int rc = -1;

  validateObj (msgPtr);

  *retCount = -1;

  if(msgPtr->_connType != MSG_PMSGQ)
    {
      int flags = 0;
      struct msghdr msg;

      SET_ZERO(msg);

      msg.msg_iov = vec->ioVecPtr;
      msg.msg_iovlen = vec->vecCount;

      rc = sendmsg(msgPtr->_connData._sock._sockFD, &msg, flags);

      if (rc == -1)
        return errno2EC (errno);
    }
  else
    {
      rc = mq_send(msgPtr->_connData._mq._mqFD,
                   (char *)vec->ioVecPtr->iov_base,
                   vec->ioVecPtr->iov_len,
                   vec->priority);

      if (rc == -1)
        return errno2EC (errno);

      /*Add the request length as the sent lenght in case of MQ*/
      rc = vec->ioVecPtr->iov_len;
    }

  *retCount = rc;

  return SUCCESS;
}

/**
 * Receive message from peer.
 * @note Receive irrespective of protocols.
 * @param msgPtr base object reference.
 * @param retCount the number of bytes recevied.
 * @param msgVec the vector base of buffers.
 * @return The \c error-code else success is returned.
 */
inline genErr_t
msg_recvVec (msg_base msgPtr, int *retCount, vec_io vec)
{
  int rc = -1;

  validateObj (msgPtr);

  *retCount = -1;

  if(msgPtr->_connType != MSG_PMSGQ)
    {
      int flags = 0;
      struct msghdr msg;

      SET_ZERO(msg);

      msg.msg_iov = vec->ioVecPtr;
      msg.msg_iovlen = vec->vecCount;

      rc = recvmsg(msgPtr->_connData._sock._sockFD, &msg, flags);

      if (rc == -1)
        return errno2EC (errno);
    }
  else
    {
      rc = mq_receive(msgPtr->_connData._mq._mqFD,
                   (char *)vec->ioVecPtr->iov_base,
                   vec->ioVecPtr->iov_len,
                   &vec->priority);

      if (rc == -1)
        return errno2EC (errno);
    }

  *retCount = rc;

  return SUCCESS;
}

/****************************************************************************/
