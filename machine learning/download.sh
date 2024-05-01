if [ ! -d "processed_data" ]; then
    wget -O data.zip "https://uapt33090-my.sharepoint.com/:u:/g/personal/jmourao_ua_pt/EXXMICXdVaBLpsdqzqWVpXQBXzEYQnoVWnRuClkbfXk0Jg?e=fEcsdp&download=1"
    unzip data.zip
    rm data.zip
else
    echo "Files already exist. Skipping download and extraction."
fi