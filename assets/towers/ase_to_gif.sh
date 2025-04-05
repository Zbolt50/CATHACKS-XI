#!/bin/sh
for f in *.aseprite; do aseprite -b "$f" --save-as "${f%.aseprite}.gif"; done

