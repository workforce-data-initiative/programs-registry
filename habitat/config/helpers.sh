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
    echo "Create postgres data directories"
    mkdir -pv {{cfg.db.datapath}}
    chown -LRv {{cfg.superuser.name}}:{{cfg.superuser.group}} {{cfg.db.datapath}}
    chmod -Rv 00760 {{cfg.db.datapath}}

}

init_db_cluster() {
    echo "Initializing postgres database cluster"
    exec chpst -U {{cfg.superuser.name}} -u {{cfg.superuser.name}} \
        initdb -D {{cfg.db.datapath}} 2>&1 &
}

start_db_server() {
    echo "Starting the postgres server"
    exec chpst -U {{cfg.superuser.name}} -u {{cfg.superuser.name}} postgres \
        -D {{cfg.db.datapath}} >logfile 2>&1 &
}

set_dir_permissions() {
    echo "Set owner of var, config and data paths to postgres db superuser"
    chown -LRv {{cfg.superuser.name}}:{{cfg.superuser.group}} {{pkg.svc_var_path}}
    chown -LRv {{cfg.superuser.name}}:{{cfg.superuser.group}} {{pkg.svc_config_path}}
    chown -LRv {{cfg.superuser.name}}:{{cfg.superuser.group}} {{pkg.svc_data_path}}

}

set_dir_permissions_on_install() {
    chown -LRv regdb:regdb $pkg_svc_var_path
    chown -LRv regdb:regdb $pkg_svc_config_path
    chown -LRv regdb:regdb $pkg_svc_data_path
}

check_user_exists_on_install() {
    echo $(id -u $1 > /dev/null 2>&1; echo $?)

}

create_db_superuser_on_install() {
    if [ $(check_user_exists "regdb") -eq 1 ]; then
        echo "Create database superuser"
        useradd --user-group --create-home regdb
    fi

    echo "User-$(id regdb)"

}
