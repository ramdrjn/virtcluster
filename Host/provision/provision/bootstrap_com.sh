json_file=$1
val=""

get_json_val()
{
    local key=$1
    val="$(awk -F ":" -v RS="," '$1~/'${key}'/ {print $2}' $json_file|sed -e 's/[{}]//g' -e 's/\"//g')"
}

setup_smart()
{
    smart channel --add $1 -y
    smart update
}

setup_pm()
{
    if [ "$1" = "smart" ]
    then
        setup_smart $PM_CONFIG_FILE
    fi
}

setup_smart_init_pkt()
{
    smart install py-scripts-common -y
    smart install commision -y
}

setup_init_pkg()
{
    if [ "$1" = "smart" ]
    then
        setup_smart_init_pkt
    fi
}

start_2nd_stage_commision()
{
    python /opt/x86vm/vc_com.py
}

get_json_val "pkg-mgmt"
PKG_MGMT=$val

get_json_val "pm-config-file"
PM_CONFIG_FILE=$val

setup_pm $PKG_MGMT $PM_CONFIG_FILE

setup_init_pkg $PKG_MGMT

start_2nd_stage_commision
