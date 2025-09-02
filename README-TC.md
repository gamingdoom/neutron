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

[English](./README.md) | [简体中文](./README-SC.md) | 繁体中文

# 關於 Neutron

  Neutron 是一個用於構建基於 Web 應用的桌面應用的開源工具，其使用 Gecko/Firefox 作為瀏覽器引擎。

# 使用方法

  Neutron 通過 ``configurator.py`` 來調整設定。當完成設定後，構建目錄下會生成一個 ``config.json`` 檔案，接著再執行 ``build.py`` 即可構建您的應用了。[Datcord](https://github.com/gamingdoom/datcord) 就是一個利用 Neutron 所構建的桌面應用程式。可在 [wiki](https://github.com/gamingdoom/neutron/wiki) 中找到更多資訊。

  ## 製作應用

  目前，Neutron 應用程式只能在 Linux 作業系統上構建。

  ```bash
  git clone https://github.com/gamingdoom/neutron.git --recurse-submodules -j8
  cd neutron
  pip install -r requirements.txt
  python configurator.py
  cd build
  python build.py
  ```

# 爲何 Neutronify？

  Neutron 有益於整個網際網路生態的多元化發展。它提供了另一種技術路線的可能性，向當前所有 Web 應用都基於 Chromium 的現狀發起了挑戰，雖然這份力量看似微弱，但也能點燃星星之火，形成燎原之勢。我們認為，更多人應該擁有這份選擇的權利，使他們**能**使用非 Chromium 浏覽器構建的應用，這將使得使用者選擇更加自由。我們所做的，正是邁出打破 Chromium 瀏覽器壟斷的第一小步。
