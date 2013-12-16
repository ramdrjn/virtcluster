
LOGS_DIR=/opt/x86vm/logs/
STAGE1_LOG=$LOGS_DIR/stage1-commision.log

json_file=$1
val=""

log()
{
    echo $1 >>$STAGE1_LOG
}

get_json_val()
{
    local key=$1
    val="$(awk -F ":" -v RS="," '$1~/'${key}'/ {print $2}' $json_file|sed -e 's/[{}]//g' -e 's/\"//g')"
}

get_pkg_grp_json_val()
{
    local pg_json_file=$1
    local key=$2
    val="$(awk -F ":" -v RS="," '$1~/'${key}'/ {print $2}' $pg_json_file|sed -e 's/[{}]//g' -e 's/\"//g')"
}

setup_smart()
{
    smart channel --add $1 -y >>$STAGE1_LOG 2>&1
    if [ $? -ne 0 ]
    then
        log "Failed to add channel in smart pm"
        exit 1
    else
        log "Smart channel added"
    fi

    smart update main >>$STAGE1_LOG 2>&1
    if [ $? -ne 0 ]
    then
        log "Failed smart update for main channel"
        exit 1
    else
        log "Smart update done for main channel"
    fi
}

setup_pm()
{
    if [ "$1" = "smart" ]
    then
        setup_smart $2
    else
        log "No PM configured"
        exit 1
    fi
}

setup_smart_init_pkg()
{
    smart install py-scripts-common -y >>$STAGE1_LOG 2>&1
    if [ $? -ne 0 ]
    then
        log "Failed smart install py-scripts-common"
        exit 1
    else
        log "Smart install py-scripts-common done"
    fi

    smart install commision -y >>$STAGE1_LOG 2>&1
    if [ $? -ne 0 ]
    then
        log "Failed smart install commision"
        exit 1
    else
        log "Smart install commision done"
    fi
}

setup_init_pkg()
{
    if [ "$1" = "smart" ]
    then
        setup_smart_init_pkg
    else
        log "Pkg management not defined"
        exit 1
    fi
}

start_2nd_stage_commision()
{
    python /opt/x86vm/vc_com.py
    if [ $? -ne 0 ]
    then
        log "Failed second stage commision"
        exit 1
    else
        log "Second stage commision done"
    fi
}

check_mount_iso()
{
    log "Mounting cdrom"

    echo "/dev/hdc  /media/cdrom0  iso9660  ro,noauto  0  0">>/etc/fstab

    mkdir /media/cdrom0
    if [ $? -ne 0 ]
    then
        log "Failed creating /media/cdrom0 directory"
        exit 1
    else
        log "/media/cdrom0 directory done"
    fi

    mount /media/cdrom0
    if [ $? -ne 0 ]
    then
        log "Failed mouting cdrom0"
        exit 1
    else
        log "cdrom0 mouting done"
    fi
}

main()
{
    mkdir -p $LOGS_DIR
    log "Stage 1 commision initiated at `date`"

    get_json_val "pm-group-file"
    PM_GRP_FILE=$val
    if [ ! -z "$PM_GRP_FILE" ]
    then
        log "Pkg group $PM_GRP_FILE"
    else
        log "Pkg group not defined"
        exit 1
    fi

    get_json_val "pm-config-file"
    PM_CONFIG_FILE=$val
    if [ ! -z "$PM_CONFIG_FILE" ]
    then
        log "Pkg config file $PM_CONFIG_FILE"
    else
        log "Pkg config not defined"
        exit 1
    fi

    get_pkg_grp_json_val $PM_GRP_FILE "manager"
    PKG_MGR=$val
    if [ ! -z "$PKG_MGR" ]
    then
        log "Pkg manager $PKG_MGR"
    else
        log "Pkg manager not defined"
        exit 1
    fi

    check_mount_iso

    setup_pm $PKG_MGR $PM_CONFIG_FILE

    setup_init_pkg $PKG_MGR

    start_2nd_stage_commision
    log "Stage1 done"
}

main
