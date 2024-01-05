rootfs::gen() {
    local path=$1

    if [ -z "$path" ]; then
        echo "Specify a basedir."
        exit 1
    fi

    if [ ! -d "$path" ]; then
        echo "Creating \"$path\"."

        mkdir -p $path
    else 
        echo "\"$path\" already exists, skipping creation."
    fi

    echo "Generating a minimal rootfs in \"$path\"."

    dnf \
      --releasever 39 \
      --installroot $path/rootfs \
      update -y 
    
    dnf \
        --releasever 39 \
        --installroot $path/rootfs  \
        install -y '@minimal-environment'
    
    dnf --releasever 39 --installroot $path/rootfs clean all

  unlink $path/rootfs/etc/resolv.conf
  cat << EOM > $path/rootfs/etc/resolv.conf
nameserver 8.8.8.8
nameserver 8.8.4.4
EOM

chown -R $(env | grep SUDO_USER | cut -d= -f2-) $path/rootfs
}

rootfs::apply() {
  local layers=$1
  local dest=$2

  if [ -z "$layers" ]; then
    echo "Missing layers folder path"
    exit 1
  fi

  if [ -z "$dest" ]; then
    echo "Missing dest folder"
    exit 1
  fi

  mkdir -p $dest/rootfs

  for layer in ${layers[@]}; do
    cp -R $PKGBOX_HOME/buildboxes/$layer/rootfs/* $dest/rootfs
  done
}

rootfs::tree::snapshot() {
  local build_dir=$1
  local fname=$2

  if [ -z "$build_dir" ]; then
    echo "Missing build_dir path"
    exit 1
  fi

  if [ -z "$fname" ]; then
    echo "Missing fname path"
    exit 1
  fi

  (cd $build_dir/rootfs; tree -ialf -I pkgbox-build) > $build_dir/builddata/$fname
}

rootfs::tree::diff() {
  local build_dir=$1

  if [ -z "$build_dir" ]; then
    echo "Missing build_dir path"
    exit 1
  fi

  diff \
    -I "./var/cache/dnf/" \
    $build_dir/builddata/before.tree \
    $build_dir/builddata/after.tree \
    > $build_dir/builddata/tree.diff

  if [ ! -z "$PKGBOX_ENV" ]; then
    pkgbox-tree-diff $build_dir/builddata/tree.diff > $build_dir/builddata/rootfs.diff.txt
  else
    ./bin/pkgbox-tree-diff $build_dir/builddata/tree.diff > $build_dir/builddata/rootfs.diff.txt
  fi

  mkdir -p $build_dir/diff
  for f in $(cat $build_dir/builddata/rootfs.diff.txt); do
    (cd $build_dir/rootfs; install -Dp $f $build_dir/diff/$(dirname $f)/$(basename $f))
  done

  tree $build_dir/diff
}
