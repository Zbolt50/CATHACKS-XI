#!/bin/sh

for file in *.aseprite; do
  aseprite -b "$file" --save-as "../pngs/${file%.aseprite}.png"
done


