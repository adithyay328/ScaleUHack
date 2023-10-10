# From ubuntu 22.04
FROM ubuntu:22.04

# Use bash as the default shell
SHELL ["/bin/bash", "-c"]

# Run apt installs with a cache clear to keep the image size down
RUN apt-get update && apt-get install -y \
    curl \
    git \
    python3 \
    python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Setting environment variable that lets us use NVM
ENV NVM_DIR /.nvm
ENV NODE_VERSION 18.18.0

# Creating the NVM_DIR folder so nvm doens't complain
RUN mkdir ${NVM_DIR}

# Getting and installing NVM for node
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash

# install node and npm
RUN source $NVM_DIR/nvm.sh \
    && nvm install $NODE_VERSION \
    && nvm alias default $NODE_VERSION \
    && nvm use default