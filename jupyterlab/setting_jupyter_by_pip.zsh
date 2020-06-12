#!/usr/bin/env zsh


# sudo apt-get install npm
# sudo apt-get install nodejs
pip install jupyter
pip install jupyterlab
pip install jupyter_contrib_nbextensions
jupyter contrib nbextension install --user
jupyter notebook --generate-config
echo "c.NotebookApp.token = 'auto'" >> ~/.jupyter/jupyter_notebook_config.py
jupyter labextension install @lckr/jupyterlab_variableinspector
jupyter labextension install @jupyterlab/toc
pip install autopep8
pip install jupyterlab_code_formatter
jupyter labextension install @ryantam626/jupyterlab_code_formatter
jupyter serverextension enable --py jupyterlab_code_formatter
jupyter labextension install jupyterlab_vim
pip install tensorflow-gpu
pip install tensorboard
pip install jupyter-tensorboard
jupyter labextension install jupyterlab_tensorboard
jupyter serverextension enable --py jupyterlab_tensorboard
jupyter labextension install @jupyterlab/git
pip install jupyterlab-git
jupyter serverextension enable --py jupyterlab_git
pip install ipywidgets
jupyter labextension install @jupyter-widgets/jupyterlab-manager
jupyter nbextension enable --py --sys-prefix widgetsnbextension
pip install jupyterlab-nvdashboard
jupyter labextension install jupyterlab-nvdashboard
pip install flake8
jupyter labextension install jupyterlab-flake8
# pip install jupyter-lsp
# jupyter labextension install @krassowski/jupyterlab-lsp
