#! /usr/bin/env bash

#########
### Setup the python environment
#########

####
# Variables
####
PROGNAME=$(basename $0)
VERSION="1.1.0-alpha1"


####
## functions
####

path=$(cd $(dirname $0) && pwd)

get_anaconda() {
    if which conda > /dev/null 2>&1; then
        echo "conda environment has been already exist."
    else
        if [[ "$(uname)" = 'Darwin' ]]; then
            cd $HOME/Downloads
            # For macOS, Anaconda 3.x:Python 3.7.x
            wget https://repo.anaconda.com/archive/Anaconda3-2018.12-MacOSX-x86_64.pkg
            sudo installer -pkg Anaconda3-2018.12-MacOSX-x86_64.pkg -target /
        elif [[ "$(uname)" = 'Linux' ]]; then
            cd $HOME/Downloads
            # For Linux, Anaconda 3.x:Python 3.7.x
            wget https://repo.anaconda.com/archive/Anaconda3-2018.12-Linux-x86_64.sh
            bash ./Anaconda3-2018.12-Linux-x86_64.sh
        fi
    fi
    echo "Anaconda environment setup has been compleated."
}

install_pip_general_package() {
    pip install -U pip
    pip install jupyter_contrib_nbextensions
}

install_jupyter_general_package() {
    # Jupyter Lab templates
    pip install jupyterlab_templates
    jupyter labextension install jupyterlab_templates
    jupyter serverextension enable --py jupyterlab_templates

    # Jupyter Lab wiget nb extension
    pip install ipywidgets
    jupyter nbextension enable --py --sys-prefix widgetsnbextension

    # Jupyter Lab beakerx
    pip install beakerx
    beakerx install
    jupyter labextension install @jupyter-widgets/jupyterlab-manager
    jupyter labextension install beakerx-jupyterlab

    # Jupyter Lab git
    jupyter labextension install @jupyterlab/git
    pip install jupyterlab-git
    jupyter serverextension enable --py jupyterlab_git

    # Jupyter Lab GitHub
    jupyter labextension install @jupyterlab/github

    # Jupyter Lab Go to definition
    jupyter labextension install @krassowski/jupyterlab_go_to_definition

    # Jupyter Lab variable inspector
    jupyter labextension install @lckr/jupyterlab_variableinspector

    # Jupyter Lab theme: Material Darker
    jupyter labextension install @oriolmirosa/jupyterlab_materialdarker

    # Jupyter Lab code formatter
    jupyter labextension install @ryantam626/jupyterlab_code_formatter
    pip install jupyterlab_code_formatter
    jupyter serverextension enable --py jupyterlab_code_formatter

    # Jupyter TensorBoard
    pip install jupyter-tensorboard

    # Jupyter Lab TensorBoard
    jupyter labextension install jupyterlab_tensorboard

    # Vim key bind
    jupyter labextension install jupyterlab_vim
}

jupyter_minimal_install() {
    # Jupyter Lab templates
    pip install jupyterlab_templates
    jupyter labextension install jupyterlab_templates
    jupyter serverextension enable --py jupyterlab_templates

    # Jupyter Lab wiget nb extension
    pip install ipywidgets
    jupyter nbextension enable --py --sys-prefix widgetsnbextension

    # Jupyter Lab Go to definition
    jupyter labextension install @krassowski/jupyterlab_go_to_definition

    # Jupyter Lab variable inspector
    jupyter labextension install @lckr/jupyterlab_variableinspector

    # Jupyter Lab theme: Material Darker
    jupyter labextension install @oriolmirosa/jupyterlab_materialdarker

    # Jupyter Lab code formatter
    jupyter labextension install @ryantam626/jupyterlab_code_formatter
    pip install jupyterlab_code_formatter
    jupyter serverextension enable --py jupyterlab_code_formatter

    # Jupyter Lab git
    jupyter labextension install @jupyterlab/git
    pip install jupyterlab-git
    jupyter serverextension enable --py jupyterlab_git

    # Jupyter Lab GitHub
    jupyter labextension install @jupyterlab/github
}

get_gopher_notes() {
    if which go > /dev/null 2>&1; then
        go get -u github.com/gopherdata/gophernotes
        mkdir -p $HOME/.local/share/jupyter/kernels/gophernotes
        cp $GOPATH/src/github.com/gopherdata/gophernotes/kernel/* $HOME/.local/share/jupyter/kernels/gophernotes
    fi
}

set_virtual_env() {
    ####
    # Create conda environments
    ####
    conda create -n tf-2.0 python=3.6 anaconda
    conda create -n tf-latest python=3.6 anaconda

    ####
    # Install python packages in each environment
    ####
    if [[ "$(uname)" = 'Darwin' ]]; then
        source activate tf-2.0
        install_pip_general_package
        pip install tensorflow==2.0.0-alpha0

        source activate tf-latest
        install_pip_general_package
        pip install tensorflow
    elif [[ "$(uname)" = 'Linux' ]]; then
        source activate tf-2.0
        install_pip_general_package
        if which nvidia-smi > /dev/null 2>&1; then
            # If GPU enabled
            pip install tensorflow-gpu==2.0.0-alpha0
        else
            pip install tensorflow==2.0.0-alpha0
        fi

        source activate tf-latest
        install_pip_general_package
        if which nvidia-smi > /dev/null 2>&1; then
            # If GPU enabled
            pip install tensorflow-gpu
        else
            pip install tensorflow
        fi
    fi

    ####
    # Install Jupyter extensions
    ####
    cd $HOME
    if [[ "$(uname)" = 'Linux' ]]; then
        source $HOME/.bashrc
    else
        source $HOME/.bash_profile
    fi
       install_jupyter_general_package

    ####
    # Add kernel to Jupyter envs
    ####
    source activate tf-2.0
    ipython kernel install --user --name=tf-2.0 --display-name=tf-2.0
    source activate tf-latest
    ipython kernel install --user --name=tf-latest --display-name=tf-latest
     if [[ "$(uname)" = 'Linux' ]]; then
        source $HOME/.bashrc
    else
        source $HOME/.bash_profile
    fi
    get_gopher_notes
}

usage() {
    echo "Usage: $PROGNAME [OPTIONS] FILE"
    echo "  This script is setup the python environment on your new machine."
    echo
    echo "Options:"
    echo "  -h, --help : Display help information"
    echo "  -m, --minimal-install : Install minimal packages "
    echo "  -v, --version : Display version"
    echo
    exit 0
}

minimal_install() {
    # In minimal_install function.
    # Currentry we run only get_anaconda and jupyter_minimal_install function.
    get_anaconda
    pip install -U pip
    pip install jupyter_contrib_nbextensions
    jupyter_minimal_install
}


#################

####
# General settings
####
# get_anaconda

set -eu

for OPT in "$@"
do
    case $OPT in
        '-h | --help')
            usage
            exit 1
            ;;
        '-m | --minimal-install')
            minimal_install
            exit 1
            ;;
        '-v | --version')
            echo "Python Env Setuper: $VERSION"
            exit 1
            ;;
    esac
    shift
done

get_anaconda
set_virtual_env

