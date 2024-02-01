<!--
<br />

<div align="center">
  <a href="https://github.com/gamingdoom/datcord">
    <img src="src/changed/browser/branding/datcord/default256.png" alt="Logo" width="80" height="80">
  </a>
-->
  <h3 align="center">Neutron</h3>
<!--
  <p align="center">
    A tool for embedding a website into a desktop app that uses Gecko 
    <br/>
    <br/>
    <img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/gamingdoom/datcord"> 
    <img alt="GitHub all releases" src="https://img.shields.io/github/downloads/gamingdoom/datcord/total"> 
    <img alt="GitHub Workflow Status" src="https://img.shields.io/github/actions/workflow/status/gamingdoom/datcord/build-linux-x86_64.yml?branch=master&label=Linux%20%20Build"> 
    <img alt="GitHub Workflow Status" src="https://img.shields.io/github/actions/workflow/status/gamingdoom/datcord/build-win64.yml?branch=master&label=Windows%20%20Build"> 
    <img alt="GitHub" src="https://img.shields.io/github/license/gamingdoom/datcord">
  </p>
</div>
-->

# About Neutron

  Neutron is an open-source tool for creating desktop applications based on web applications. Neutron uses Gecko/Firefox under the hood.

# Usage
  Neutron can be configured through the ``configurator.py`` configuration wizard. After being configured, ``config.json`` is generated in the build folder and ``build.py`` can be run to build your application. One example of a Neutron application is [Datcord](https://github.com/gamingdoom/datcord). More information can be found on the [wiki](https://github.com/gamingdoom/neutron/wiki).
  ## Making an application
  Currently, neutron applications can only be built on Linux, so you might have to use WSL.
  ```
  git clone https://github.com/gamingdoom/neutron.git --recurse-submodules -j8
  cd neutron
  pip install -r requirements.txt
  python configurator.py
  cd build
  python build.py
  ```
# Why?
 Neutron is beneficial for the internet as a whole as it challenges the status quo of everything being Chromium based. If more people are able to use browsers other than Chromium, the internet will be freer since there will be no browser monoply.
