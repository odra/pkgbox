container::create() {
    local basedir=$1
    local name=$2

    runc \
        create \
        --bundle $basedir \
        --pid-file $basedir/pkgbox.pid  \
        $name
}

container::delete() {
    local name=$1

    runc \
        delete --force \
        $name
}

container::exec() {
    local name=$1
    local cmdargs="${@:2}"

    runc \
        exec \
        $name \
        $cmdargs
}
