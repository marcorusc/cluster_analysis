#!/bin/bash

values=(0.001 0.01 0.02 0.03 0.04 0.05 0.06 0.07 0.08 0.09 0.1)

physi_folder=$HOME"/PhysiBoSS"

config_folder=$physi_folder"/config/"

script_folder=$HOME"/data/Cluster_analysis/"

config_file=$config_folder"PhysiCell_settings_2D.xml"

sed -i '286s/0.05/0/' $config_file

for f in "${values[@]}"
do
 cd $physi_folder
 sed -i '286s/0/'"$f"'/' $config_file
 for n in {1..10}
 do
  echo $f
  cd $physi_folder
  ./Invasion_model $config_file 
  cd $script_folder
  python collect_data.py "$f"
  done
 sed -i '286s/'"$f"'/0/' $config_file
done

