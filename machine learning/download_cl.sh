if [ ! -d "classification_data2" ]; then
    wget -O data.zip "https://uapt33090-my.sharepoint.com/:u:/g/personal/jmourao_ua_pt/EXxPuiC-HnFErTtdcfolrj8Bj-oEAoxvGEZviawrB4QPhQ?e=jPtbqa&download=1"
    unzip data.zip
    rm data.zip
else
    echo "Files already exist. Skipping download and extraction."
fi