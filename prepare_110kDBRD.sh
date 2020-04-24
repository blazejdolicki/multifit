echo "Start time:"
TZ=CET date
echo ""

# if data wasn't downloaded before
if [ ! -d "data/cls/nl-books" ] ; then
    echo "Downloading 110kDBRD dataset"
    DATA_DIR='data/cls'
    url="https://github.com/benjaminvdb/110kDBRD/releases/download/v2.0/110kDBRD_v2.tgz"
    wget -O ${DATA_DIR}/110kDBRD_v2.tgz ${url}

    # check if download failed
    if [ $? -ne 0 ]; then
        echo "Download failed. Check if the data set is still hosted at ${url}"
        exit
    fi
    echo "Unpacking tgz file"
    tar zxvf ${DATA_DIR}/110kDBRD_v2.tgz -C ${DATA_DIR}
    mkdir ${DATA_DIR}/nl-books
    # convert text files in folders into csv
    python convert_110kDBRD.py
    rm ${DATA_DIR}/110kDBRD_v2.tgz
else
    echo "Dataset already exists. Skipping download. "
fi