#!/bin/bash

# Define the paths to the input XML file and the C++ software executable
INPUT_XML="./config/PhysiCell_settings_2D.xml"
EXECUTABLE="./Invasion_model"

# Define the subset of parameters to vary and their ranges
PARAMETERS=("param1" "param2" "param3" "param4" "param5" "param6" "param7")
RANGES=(0.1 0.9 0.1 0.9 0.1 0.9 0.1 0.9)

# Define the number of samples to generate for the LHS analysis
NUM_SAMPLES=100
# Define the number of nodes used to parallelize the analysis
NUM_NODES=4
# Generate the LHS samples using a Python script
python lhs_sampling.py ${NUM_SAMPLES}

python generate_subspaces.py ${NUM_NODES}

# Loop over the LHS samples and run the C++ software with each parameter set
python parser.py ${INPUT_XML}


