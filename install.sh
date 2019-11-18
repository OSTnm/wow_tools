#!/bin/env bash

pyinstaller -i idling/wow_idling.ico -F idling/idling.py
if [ $? -ne 0 ]; then
    echo "idling - converting to exe failed!"
    exit 1
else
    echo "idling - converting to exe done!"
fi
echo "putting resource into idling..."
mkdir -p dist/idling
mv dist/idling.exe dist/idling/
cp -r idling/classic dist/idling/
cp -r idling/idling.ico dist/idling/
echo "done"
