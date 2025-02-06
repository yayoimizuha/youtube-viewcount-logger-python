#!/usr/bin/env bash
# shellcheck disable=SC2164
cd /tmp/
sudo apt install curl tar -y
curl -sSL "https://download.mozilla.org/?product=firefox-latest-ssl&os=linux64&lang=ja" | tar -xf -
sudo mv firefox /opt