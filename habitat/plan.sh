pkg_origin=brighthive
pkg_name=program-registry
pkg_version=0.0.1
pkg_maintainer="engineering@brighthive.io"
pkg_filename=${pkg_name}-${pkg_version}.tar.gz
pkg_upstream_url="https://github.com/brighthive/program-registry.git"
pkg_exports=(
    [port]=listening_port
    [db-port]=db.port
)

pkg_exposes=(port db-port)
pkg_build_deps=(
    core/openssl
    core/gcc
    core/libffi
)
pkg_deps=(core/python core/postgresql core/shadow)
pkg_interpreters=(bin/python3 bin/bash)

pkg_lib_dirs=(lib)
pkg_include_dirs=(include)
pkg_bin_dirs=(bin)
pkg_svc_user=root
pkg_svc_group=root
pkg_licence=('MIT')

do_verify () {
  return 0
}

do_clean() {
  return 0
}

do_unpack() {
  PROJECT_ROOT="${PLAN_CONTEXT}/.."

  build_line "Copying project data from $PROJECT_ROOT to $pkg_prefix ..."
  mkdir -p $pkg_prefix
  cp -vr $PROJECT_ROOT/api $pkg_prefix/
  cp -vr $PROJECT_ROOT/app $pkg_prefix/
  cp -vr $PROJECT_ROOT/habitat/config/helpers.sh $pkg_prefix/
  cp -vr $PROJECT_ROOT/instance $pkg_prefix/
  cp -vr $PROJECT_ROOT/tests $pkg_prefix/
  cp -vr $PROJECT_ROOT/*.py $pkg_prefix/
  cp -vr $PROJECT_ROOT/requirements.txt $pkg_prefix/
}

do_prepare() {
  export LD_LIBRARY_PATH="$(hab pkg path core/gcc)/lib"
  export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$(hab pkg path core/libffi)/lib"
  export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$(hab pkg path core/postgresql)/lib"
  build_line "Updating pip and create virtual env..."
  pip install --upgrade pip virtualenv
  virtualenv "${pkg_prefix}" -p python3
}

do_build() {
  return 0
}

do_install() {
  build_line "Activating virtual env..."
  source "${pkg_prefix}/bin/activate"

  build_line "Install gunicorn ..."
  pip install gunicorn
  pip install --no-binary :all: $(grep psycopg2 /src/requirements.txt)
  build_line "Installing requirements from requirements.txt ..."
  pip install -r /src/requirements.txt

  source $pkg_prefix/helpers.sh
  mkdir -p $pkg_svc_var_path
  mkdir -p $pkg_svc_config_path
  mkdir -p $pkg_svc_data_path

  create_db_superuser_on_install
  set_dir_permissions_on_install
}
