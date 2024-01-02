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
        --installroot $path/rootfs  \
        install -y '@minimal-environment'

  unlink $path/rootfs/etc/resolv.conf
  cat << EOM > $path/rootfs/etc/resolv.conf
nameserver 8.8.8.8
nameserver 8.8.4.4
EOM

chown -R $(env | grep SUDO_USER | cut -d= -f2-) $path/rootfs
}
