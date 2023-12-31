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
