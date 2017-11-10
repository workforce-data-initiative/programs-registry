check_user_exists() {
    echo $(id -u $1 > /dev/null 2>&1; echo $?)

}

create_db_superuser() {
    if [ $(check_user_exists "{{cfg.superuser.name}}") -eq 1 ]; then
        echo "Create database superuser"
        useradd --user-group --create-home {{cfg.superuser.name}}
    fi

    echo "User-$(id {{cfg.superuser.name}})"

}


setup_db_datapath() {
    parent_datapath=$(dirname {{cfg.db.datapath}})
    echo "Create postgres data directories"
    mkdir -pv "{{cfg.db.datapath}}"
    chown -LRv {{cfg.superuser.name}}:{{cfg.superuser.group}} $parent_datapath
    chmod -Rv 00760 $parent_datapath

}

set_dir_permissions() {
    echo "Set owner of var, config and data paths to postgres db superuser"
    chown -LRv {{cfg.superuser.name}}:{{cfg.superuser.group}} {{pkg.svc_var_path}}
    chown -LRv {{cfg.superuser.name}}:{{cfg.superuser.group}} {{pkg.svc_config_path}}
    chown -LRv {{cfg.superuser.name}}:{{cfg.superuser.group}} {{pkg.svc_data_path}}

}
