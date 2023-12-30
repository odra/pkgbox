oci::bundle::config::gen() {
    local path=$1

    if [ -z $path ]; then
        echo "Set a path"
    fi

    if [ -f $path/config.json ]; then
        rm $path/config.json
    fi

    (cd $path; runc spec --rootless)

    local cfg=$(cat $path/config.json)

    cfg=$(echo $cfg | jq '.process.args = ["sleep", "infinity"]')
    cfg=$(echo $cfg | jq '.root.readonly = false')
    cfg=$(echo $cfg | jq '.process.terminal = false')
    cfg=$(echo $cfg | jq ".mounts[.mounts | length] |= . + {\"destination\": \"/tmp/pkgbox/build\", \"options\": [\"rbind\"], \"source\": \"$path/volumes/build\"}")

    echo $cfg | jq > $path/config.json
}
