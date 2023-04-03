#!/bin/bash

physi_folder=$HOME"/PhysiBoSS"
config_folder=$physi_folder"/config/"
script_folder=$HOME"/data/cluster_analysis/"
config_file=$config_folder"PhysiCell_settings_2D.xml"

parameter="migration_bias"
values=(0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0)

sed -i '255s/0.85/0.0/' $config_file

for run_count in {1..5} # run 5 sets of 10, 20, 30, 40, 50
do
    run_size=$((run_count * 10)) # increase the run size by 10 each time
    mkdir "$script_folder/analysis_$run_size"

    for f in "${values[@]}"
    do
        cd $physi_folder
        sed -i '255s/0.0/'"$f"'/' $config_file

        for n in $(seq 1 $run_size)
        do
            echo $f
            ./Invasion_model $config_file
            cd $script_folder
            python3 collect_data.py "$f"  "analysis_$run_size"
            cd $physi_folder
        done

        sed -i '255s/'"$f"'/0.0/' $config_file
    done

done

cd $HOME
cd $script_folder

echo "FINISH WITH THE SCRIPT"
