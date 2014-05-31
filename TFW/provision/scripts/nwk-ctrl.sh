#!/bin/sh

OVS_DIR=/opt/ovs
OVS_BIN_DIR=$OVS_DIR/bin/
OVS_SBIN_DIR=$OVS_DIR/sbin/
OVS_DEPLOY_DIR=/opt/deploy-ovs

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

ovs-vswitchd --pidfile --log-file --detach

if [ $? -ne 0 ]
then
    log "Failed starting ovs-vswitchd"
    exit 1
else
    log "ovs-vswitchd started"
fi

