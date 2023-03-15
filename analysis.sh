#!/bin/bash

physi_folder=$HOME"/PhysiBoSS"

config_folder=$physi_folder"/config/"

script_folder=$HOME"/data/cluster_analysis/"

config_file=$config_folder"PhysiCell_settings_2D.xml"

parameter="cell_junction_attach"

mkdir $parameter

values=(0.001 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9)

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
  python3 collect_data.py "$f" "$parameter"
  done
 sed -i '286s/'"$f"'/0/' $config_file
done
sed -i '286s/0/0.05/' $config_file

cd $HOME
cd $script_folder

parameter="cell_junction_detach"

values=(0.001 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9)

mkdir $parameter

sed -i '287s/0.3/0/' $config_file

for f in "${values[@]}"
do
 cd $physi_folder
 sed -i '287s/0/'"$f"'/' $config_file
 for n in {1..10}
 do
  echo $f
  cd $physi_folder
  ./Invasion_model $config_file
  cd $script_folder
  python3 collect_data.py "$f" "$parameter"
  done
 sed -i '287s/'"$f"'/0/' $config_file
done
sed -i '287s/0/0.3/' $config_file

cd $HOME
cd $script_folder

parameter="migration_bias"

values=(0.5 0.55 0.6 0.65 0.7 0.75 0.8 0.85 0.9)

mkdir $parameter

sed -i '289s/0.85/0/' $config_file

for f in "${values[@]}"
do
 cd $physi_folder
 sed -i '289s/0/'"$f"'/' $config_file
 for n in {1..10}
 do
  echo $f
  cd $physi_folder
  ./Invasion_model $config_file
  cd $script_folder
  python3 collect_data.py "$f" "$parameter"
  done
 sed -i '289s/'"$f"'/0/' $config_file
done
sed -i '289s/0/0.85/' $config_file

cd $HOME
cd $script_folder

parameter="migration_speed"

values=(0.3 0.4 0.5 0.6 0.7 0.8 0.9)

mkdir $parameter

sed -i '290s/0.8/0/' $config_file

for f in "${values[@]}"
do
 cd $physi_folder
 sed -i '290s/0/'"$f"'/' $config_file
 for n in {1..10}
 do
  echo $f
  cd $physi_folder
  ./Invasion_model $config_file
  cd $script_folder
  python3 collect_data.py "$f" "$parameter"
  done
 sed -i '290s/'"$f"'/0/' $config_file
done
sed -i '290s/0/0.8/' $config_file

cd $HOME
cd $script_folder


parameter="contact_cell_ecm_threshold"

values=(0.001 0.01 0.02 0.03 0.04 0.05 0.06 0.07 0.08 0.09)

mkdir $parameter

sed -i '283s/0.05/0/' $config_file

for f in "${values[@]}"
do
 cd $physi_folder
 sed -i '283s/0/'"$f"'/' $config_file
 for n in {1..10}
 do
  echo $f
  cd $physi_folder
  ./Invasion_model $config_file
  cd $script_folder
  python3 collect_data.py "$f" "$parameter"
  done
 sed -i '283s/'"$f"'/0/' $config_file
done
sed -i '283s/0/0.05/' $config_file

cd $HOME
cd $script_folder

parameter="contact_cell_cell_threshold"

values=(0.01 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9)

mkdir $parameter

sed -i '285s/0.3/0/' $config_file

for f in "${values[@]}"
do
 cd $physi_folder
 sed -i '285s/0/'"$f"'/' $config_file
 for n in {1..10}
 do
  echo $f
  cd $physi_folder
  ./Invasion_model $config_file
  cd $script_folder
  python3 collect_data.py "$f" "$parameter"
  done
 sed -i '285s/'"$f"'/0/' $config_file
done
sed -i '285s/0/0.3/' $config_file


cd $HOME
cd $script_folder

parameter="cell_ecm_repulsion"

values=(5 10 15 20 25 30 35 40 45 50)

mkdir $parameter

sed -i '273s/15/0/' $config_file

for f in "${values[@]}"
do
 cd $physi_folder
 sed -i '273s/0/'"$f"'/' $config_file
 for n in {1..10}
 do
  echo $f
  cd $physi_folder
  ./Invasion_model $config_file
  cd $script_folder
  python3 collect_data.py "$f" "$parameter"
  done
 sed -i '273s/'"$f"'/0/' $config_file
done
sed -i '273s/0/15/' $config_file

cd $HOME
cd $script_folder

echo "FINISH WITH THE SCRIPT"
