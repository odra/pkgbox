container::create() {
    local basedir=$1
    local name=$2
    local specdir=$3

    cp -R $specdir/* $basedir/volumes/build/
    chmod +x $basedir/volumes/build/pkgbox.spec.bash

    runc \
        --debug \
        create \
        --bundle $basedir \
        --pid-file $basedir/pkgbox.pid \
        $name
}

container::delete() {
    local name=$1

    runc \
        --debug \
        delete --force \
        $name
}

container::exec() {
    local name=$1
    local cmdargs="${@:2}"

    runc \
        --debug \
        exec \
        $name \
        $cmdargs
}
