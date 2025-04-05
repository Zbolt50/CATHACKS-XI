#!/bin/sh
for file in *.aseprite; do
  aseprite -b "$file" --save-as "./${file%.aseprite}.png"
done


