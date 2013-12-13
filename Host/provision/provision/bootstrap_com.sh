
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

    smart update >>$STAGE1_LOG 2>&1
    if [ $? -ne 0 ]
    then
        log "Failed smart update"
        exit 1
    else
        log "Smart update done"
    fi
}

setup_pm()
{
    if [ "$1" = "smart" ]
    then
        setup_smart $PM_CONFIG_FILE
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

mkdir -p $LOGS_DIR
log "Stage 1 commision initiated at `date`"

get_json_val "pkg-mgmt"
PKG_MGMT=$val
if [ ! -z "$PKG_MGMT" ]
then
    log "Pkg mgmt $PKG_MGMT"
else
    log "Pkg mgmt not defined"
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

setup_pm $PKG_MGMT $PM_CONFIG_FILE

setup_init_pkg $PKG_MGMT

start_2nd_stage_commision
log "Stage1 done"
