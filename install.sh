#!/bin/sh

cd frontend
npm uninstall --save-dev angular-cli
npm uninstall -g angular-cli
rm -rf node_modules
npm cache clean --force
npm install -g @angular/cli@latest
npm install --save-dev @angular/cli@latest
npm install
