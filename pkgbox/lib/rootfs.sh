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
        install --nodocs -y filesystem
}

rootfs::_gen() {
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

    mkdir -p $path/{rootfs,volumes/build}

    echo "Creating basic rootfs in \"$path\"."

    # dnf \
    #     --releasever 39 \
    #     --installroot $path/rootfs  \
    #     --with-optional \
    #     group install -y minimal-environment

    dnf \
        --releasever 39 \
        --installroot $path/rootfs  \
        install --nodocs -y filesystem
        # install -y net-tools cpio filesystem

#     unlink $path/rootfs/etc/resolv.conf
#     cat << EOM > $path/rootfs/etc/resolv.conf
# nameserver 8.8.8.8
# nameserver 8.8.4.4
# EOM
}
