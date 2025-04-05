#!/bin/sh
rm *.png
echo "Removed all old pngs"

for file in *.aseprite; do
  aseprite -b "$file" --save-as "./pngs/${file%.aseprite}.png"
done


