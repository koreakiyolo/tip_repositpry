FROM python:3
MAINTAINER Haruyuki Oda
# ENV HTTPS_PROXY
# ENV HTTP_PROXY
RUN pip install jupyterlab
RUN pip install numpy matplotlib pandas scipy argparse ipdb scikit-learn
RUN pip install pillow mglearn
RUN jupyter serverextension enable --py jupyterlab
