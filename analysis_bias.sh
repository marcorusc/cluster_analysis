#!/bin/bash

physi_folder=$HOME"/PhysiBoSS"
config_folder=$physi_folder"/config/"
script_folder=$HOME"/data/cluster_analysis/"
config_file=$config_folder"PhysiCell_settings_2D.xml"

parameter="migration_bias"
values=($(seq 0 0.1 1))

mkdir $parameter

sed -i '255s/0.85/0/' $config_file

for run_count in {1..5} # run 5 sets of 10, 20, 30, 40, 50
do
    run_size=$((run_count * 10)) # increase the run size by 10 each time
    mkdir "$script_folder/analysis_$run_size"

    for f in "${values[@]}"
    do
        cd $physi_folder
        sed -i '255s/0/'"$f"'/' $config_file

        for n in $(seq 1 $run_size)
        do
            echo $f
            ./Invasion_model $config_file
        done

        cd $script_folder
        python3 collect_data.py "$f" "$parameter" "analysis_$run_size"
        sed -i '255s/'"$f"'/0/' $config_file
    done

    sed -i '255s/'"$run_size"'/10/' $config_file # reset "max_time" to 10
done

cd $HOME
cd $script_folder

echo "FINISH WITH THE SCRIPT"
