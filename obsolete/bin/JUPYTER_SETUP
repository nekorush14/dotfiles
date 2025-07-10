#! /usr/bin/env bash

#########
### Setup the python environment
#########

####
# Variables
####
PROGNAME=$(basename $0)
VERSION="1.2.0-alpha1"

####
## functions
####

install_pip_general_package() {
    pip install -U pip
    pip install jupyter-contrib-nbextensions
    pip install jupyter-nbextensions-configurator
    pip install isort
    pip install autopep8
}

install_jupyter_general_package() {

    jupyter contrib nbextension install --user
    jupyter nbextensions_configurator enable --user

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
    jupyter contrib nbextension install --user
    jupyter nbextensions_configurator enable --user

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

####
# General settings
####
set -eu

for OPT in "$@"
do
    case $OPT in
        '-h | --help')
            usage
            exit 1
            ;;
        '-m | --minimal-install')
            install_pip_general_package
            jupyter_minimal_install
            exit 1
            ;;
        '-v | --version')
            echo "Jupyter setuper: $VERSION"
            exit 1
            ;;
    esac
    shift
done

install_pip_general_package
jupyter_minimal_install
# install_jupyter_general_package