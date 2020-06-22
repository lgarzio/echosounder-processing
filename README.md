# echosounder-processing
Tools for processing echo sounder data using the [echopype package](https://echopype.readthedocs.io/en/latest/usage.html).


## Installation Instructions
Add the channel conda-forge to your .condarc. You can find out more about conda-forge from their website: https://conda-forge.org/

`conda config --add channels conda-forge`

Clone the echosounder-processing repository

`git clone https://github.com/lgarzio/echosounder-processing.git`

Change your current working directory to the location that you downloaded echosounder-processing. 

`cd /Users/lgarzio/Documents/repo/echosounder-processing/`

Create conda environment from the included environment.yml file:

`conda env create -f environment.yml`

Once the environment is done building, activate the environment:

`conda activate echosounder-processing`

Install the toolbox to the conda environment from the root directory of the echosounder-processing toolbox:

`pip install .`

The toolbox should now be installed to your conda environment.
