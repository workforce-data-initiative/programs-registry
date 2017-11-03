pkg_origin=brighthive
pkg_name=program-registry
pkg_version=0.1.0
pkg_maintainer="jee@brighthive.io, stanley@brighthive.io, aretha@brighthive.io"
pkg_filename=${pkg_name}-${pkg_version}.tar.gz
pkg_upstream_url="https://github.com/brighthive/program-registry.git"
pkg_exports=([port]=listening_port)
pkg_exposes=(port)
pkg_build_deps=(core/virtualenv core/postgresql core/gcc core/openssl)
pkg_deps=(core/python)
pkg_interpreters=(bin/python3)
pkg_licence=('MIT')

do_verify () {
  return 0
}

do_clean() {
  return 0
}

do_unpack() {
  # create a env variable for the project root
  PROJECT_ROOT="${PLAN_CONTEXT}/.."

  mkdir -p $pkg_prefix
  # copy the contents of the source directory to the habitat cache path
  build_line "Copying project data from /program-registry to $pkg_prefix ..."
  cp -r $PROJECT_ROOT/app $pkg_prefix/
  cp -r $PROJECT_ROOT/instance $pkg_prefix/
  cp -r $PROJECT_ROOT/tests $pkg_prefix/
  cp -r $PROJECT_ROOT/*.py $pkg_prefix/
  cp -r $PROJECT_ROOT/requirements.txt $pkg_prefix/
}

do_build() {
  return 0
}

do_install() {
  cd $pkg_prefix
  build_line "Creating virtual environment venv..."
  virtualenv "venv" -p python3
  . venv/bin/activate
  build_line "Install gunicorn ..."
  pip install gunicorn
  build_line "Installing requirements from requirements.txt ..."
  pip install -r requirements.txt
}
