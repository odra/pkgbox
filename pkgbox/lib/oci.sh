oci::layer::gen() {
  local src=$1
  local dest=$2

  if [ -z "$src" ]; then
    echo "Missing src folder path"
    exit 1
  fi

  if [ -z "$dest" ]; then
    echo "Missing dest folder"
    exit 1
  fi

  mkdir -p $dest
  cp -aR $src/diff $dest/diff

  (
    cd $dest/diff;
    tar --acls --xattrs -cvzf $PKGBOX_HOME/oci/layers/$(basename $dest).tar.gz .;
  )

  sha=$(sha256sum $PKGBOX_HOME/oci/layers/$(basename $dest).tar.gz | awk '{print $1}')
  mv $PKGBOX_HOME/oci/layers/$(basename $dest).tar.gz $PKGBOX_HOME/oci/layers/$sha.tar.gz
}

oci::runtime::config::gen() {
  local dest=$1

  if [ -z "$dest" ]; then
    echo "Missing dest folder"
    exit 1
  fi

  cfg=$(cat etc/config.json)
  
  read -r -d '' userdata << EOM
{ 
  "destination": "/opt/pkgbox-build",
  "type": "bind",
  "source": "$dest/userdata/pkgbox-build",
  "options": [
    "bind",
    "rprivate"
  ]
}
EOM

  cfg=$(echo $cfg | jq ".mounts[.mounts | length] |= . + $userdata")
  
  echo $cfg | jq > $dest/config.json
}

oci::layer::store() {
  local build_dir=$1

  (
    cd $build_dir/diff;
    tar \
      --sort=name \
      --mtime='@0' \
      --xattrs \
      --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
      -cvf \
      $build_dir/diff.tar .;
  )

  digest=$(sha256sum $build_dir/diff.tar | awk '{print $1}')
  mv $build_dir/diff.tar $PKGBOX_HOME/oci/layers/$digest.tar
}
