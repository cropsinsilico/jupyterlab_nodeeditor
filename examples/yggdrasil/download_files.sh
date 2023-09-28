#!/bin/bash

# Clone the repository
git clone https://github.com/cropsinsilico/yggdrasil


# Define the base directory and source_directory
src_dir="./yggdrasil/yggdrasil/examples/fakeplant/"
base_dir="."

# Creating necessary directories in my_project
mkdir -p "$base_dir"/{Input,Output,src,yamls}

# Function to copy files
copy_files() {
  local dest_dir=$1
  shift
  local src_path
  for rel_path in "$@"; do
    src_path="$src_dir/$rel_path"
    cp "$src_path" "$dest_dir"
  done
}

# Copy the files to the respective directories
copy_files "$base_dir/Input" \
  "Input/ambient_light.txt" \
  "Input/canopy_structure.txt" \
  "Input/co2.txt" \
  "Input/growth_rate.txt" \
  "Input/light_intensity.txt" \
  "Input/photosynthesis_rate.txt" \
  "Input/plant_layout.txt" \
  "Input/temperature.txt" \
  "Input/time.txt"
  
copy_files "$base_dir/Output" \
  "Input/canopy_structure.txt" \
  "Input/co2.txt" \
  "Input/growth_rate.txt" \
  "Input/light_intensity.txt" \
  "Input/photosynthesis_rate.txt"
  
copy_files "$base_dir/src" \
  "src/canopy.cpp" \
  "src/growth.py" \
  "src/light.c" \
  "src/photosynthesis.py"

rm -rf ./yggdrasil

echo "Files Have Been Set Up"