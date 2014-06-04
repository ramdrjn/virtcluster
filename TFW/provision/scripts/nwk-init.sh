#!/bin/sh

OVS_DIR=/opt/ovs
OVS_BIN_DIR=$OVS_DIR/bin/
OVS_SBIN_DIR=$OVS_DIR/sbin/
OVS_DEPLOY_DIR=/opt/deploy-ovs

OVS_BR_NAME=fabbr0
OVS_BR_MAC=00:11:22:33:44:55

export PATH=$PATH:$OVS_BIN_DIR:$OVS_SBIN_DIR

log()
{
    echo $1
}

ovsdb-server                                                	\
    --remote=punix:$OVS_DEPLOY_DIR/var/run/openvswitch/db.sock 	\
    --remote=db:Open_vSwitch,manager_options 			\
    --private-key=db:SSL,private_key 				\
    --certificate=db:SSL,certificate 				\
    --bootstrap-ca-cert=db:SSL,ca_cert 				\
    --pidfile 							\
    --log-file							\
    --detach

if [ $? -ne 0 ]
then
    log "Failed starting ovsdb-server"
    exit 1
else
    log "ovsdb-server started"
fi

#Insert kernel module
insmod $OVS_DIR/kernel_module/openvswitch.ko

if [ $? -ne 0 ]
then
    log "Failed kernel module insert"
    exit 1
else
    log "kernel module inserted"
fi

ovs-vsctl --log-file --no-wait init

if [ $? -ne 0 ]
then
    log "Failed db init"
    exit 1
else
    log "ovs-vsctl init done"
fi

ovs-vswitchd --pidfile --log-file --detach

if [ $? -ne 0 ]
then
    log "Failed starting ovs-vswitchd"
    exit 1
else
    log "ovs-vswitchd started"
fi

ovs-vsctl --log-file add-br $OVS_BR_NAME

if [ $? -ne 0 ]
then
    log "Failed bridge creation"
    exit 1
else
    log "bridge creation done"
fi

#ovs-vsctl set bridge $OVS_BR_NAME other-config:hwaddr=$OVS_BR_MAC

# if [ $? -ne 0 ]
# then
#     log "Failed setting MAC addr"
#     exit 1
# else
#     log "MAC addr set"
# fi