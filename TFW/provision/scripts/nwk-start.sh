#!/bin/sh

OVS_DIR=/opt/ovs
OVS_BIN_DIR=$OVS_DIR/bin/
OVS_SBIN_DIR=$OVS_DIR/sbin/
OVS_DEPLOY_DIR=/opt/deploy-ovs

OVS_BRIDGE_NAME=fabbr0
OVS_BRIDGE_IP=192.168.100.1

DNSMASQ_DIR=/opt/dnsmasq
DNSMASQ_CONF=/opt/dnsmasq/dnsmasq.conf

export PATH=$PATH:$OVS_BIN_DIR:$OVS_SBIN_DIR

log()
{
    echo $1
}

# ifconfig $OVS_BRIDGE_NAME $OVS_BRIDGE_IP up

# if [ $? -ne 0 ]
# then
#     log "Failed assigning ip to br"
#     exit 1
# else
#     log "br ip assigned and started"
# fi

$DNSMASQ_DIR/dnsmasq -C $DNSMASQ_CONF -i $OVS_BRIDGE_NAME

if [ $? -ne 0 ]
then
    log "Failed starting dnsmasq"
    exit 1
else
    log "dnsmasq started"
fi

