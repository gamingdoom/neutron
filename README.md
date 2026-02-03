<h1 align="center">Neutron</h1>

English | [简体中文](./README-SC.md) | [繁体中文](./README-TC.md)

# About Neutron

  Neutron is an open-source tool for creating desktop applications based on web applications. Neutron uses Gecko/Firefox under the hood.

# Usage
  Neutron can either be configured through the ``configurator.py`` configuration wizard or the `pwa_configurator.py` tool. After being configured, ``config.json`` is generated in the build folder and ``build.py`` can be run to build your application. One example of a Neutron application is [Datcord](https://github.com/gamingdoom/datcord). More information can be found on the [wiki](https://github.com/gamingdoom/neutron/wiki).

  Currently, Neutron applications can only be built on Linux.

  ## Making an Application (Configuration Wizard Method)
  ```bash
  git clone https://github.com/gamingdoom/neutron.git --recurse-submodules -j8
  cd neutron
  pip install -r requirements.txt
  python configurator.py -b
  ```

  ## Making an Application (PWA Manifest Method)
  ```bash
  git clone https://github.com/gamingdoom/neutron.git --recurse-submodules -j8
  cd neutron
  pip install -r requirements.txt
  python pwa_configurator.py <url of PWA manifest> <output directory>
  python configurator.py -c <output directory>/config.json -b
  ```

# Why?
 Neutron is beneficial for the internet as a whole as it challenges the status quo of everything being Chromium based. If more people are able to use browsers other than Chromium, the internet will be freer since there will be no browser monoply.
