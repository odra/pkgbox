rootfs::gen() {
    local path=$1

    if [ -z "$path" ]; then
        echo "Specify a basedir."
        exit 1
    fi

    if [ ! -d "$path" ]; then
        echo "Creating \"$path\"."

        mkdir -p $path/rootfs
    else 
        echo "\"$path\" already exists, skipping creation."
    fi

    echo "Creating basic rootfs in \"$path\"."

    dnf \
        --releasever 39 \
        --installroot $path/rootfs  \
        --with-optional \
        group install -y minimal-environment
}
