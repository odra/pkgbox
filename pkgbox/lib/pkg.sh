export PKGBOX_DEPENDS=()

pkgbox::pkg::depends() {
  local box_name=$1

  if [ -z "$box_name" ]; then
    echo "Missing box name to apply from."
    exit 1
  fi

  if [ ! -d "$PKGBOX_HOME/buildboxes/$box_name" ]; then
    echo "Buildbox \"$box_name\" does not exist."
    exit 1
  fi

  PKGBOX_DEPENDS=("${PKGBOX_DEPENDS[@]}" "$box_name") 
}

pkgbox::pkg::prepare() {
  echo 'Not Implemented: pkgbox::pkg::prepare'
  exit 38
}

pkgbox::pkg::build() {
  echo 'Not Implemented: pkgbox::pkg::build'
  exit 38
}

pkgbox::pkg::install() {
  echo 'Not Implemented: pkgbox::pkg::install'
  exit 38
}

pkgbox::pkg::cleanup() {
  echo 'Not Implemented: pkgbox::pkg::cleanup'
  exit 38
}
