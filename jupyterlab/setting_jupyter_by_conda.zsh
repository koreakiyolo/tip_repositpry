#!/usr/bin/env zsh


# sudo apt-get install npm
# sudo apt-get install nodejs
conda install jupyter
conda install -c conda-forge jupyterlab
conda install -c conda-forge jupyter_contrib_nbextensions
jupyter contrib nbextension install --user
jupyter notebook --generate-config
echo "c.NotebookApp.token = 'auto'" >> ~/.jupyter/jupyter_notebook_config.py
jupyter labextension install @lckr/jupyterlab_variableinspector
jupyter labextension install @jupyterlab/toc
conda install -c conda-forge autopep8
conda install -c conda-forge jupyterlab_code_formatter
jupyter labextension install @ryantam626/jupyterlab_code_formatter
jupyter serverextension enable --py jupyterlab_code_formatter
jupyter labextension install jupyterlab_vim
#
conda install -c conda-forge tensorflow
conda install -c conda-forge tensorboard
pip install jupyter-tensorboard
jupyter labextension install jupyterlab_tensorboard
jupyter serverextension enable --py jupyterlab_tensorboard
#
jupyter labextension install @jupyterlab/git
conda install -c conda-forge jupyterlab-git
jupyter serverextension enable --py jupyterlab_git
conda install -c conda-forge ipywidgets
jupyter labextension install @jupyter-widgets/jupyterlab-manager
jupyter nbextension enable --py --sys-prefix widgetsnbextension
conda install -c conda-forge jupyterlab-nvdashboard
jupyter labextension install jupyterlab-nvdashboard
conda install -c anaconda flake8
jupyter labextension install jupyterlab-flake8
# pip install jupyter-lsp
# jupyter labextension install @krassowski/jupyterlab-lsp
