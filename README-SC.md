<h1 align="center">Neutron</h1>

[English](./README.md) | 简体中文 | [繁体中文](./README-TC.md)

# 关于 Neutron

  Neutron 是一个用于构建基于 Web 应用的桌面应用的开源工具，其使用 Gecko/Firefox 作为浏览器引擎。

# 使用方法

  Neutron 通过 ``configurator.py`` 来调整设定。当完成设定后，构建目录下会生成一个 ``config.json``，此时再运行 ``build.py`` 即可构建你的应用了。[Datcord](https://github.com/gamingdoom/datcord) 就是一个利用 Neutron 所构建的 Web 应用。可在 [wiki](https://github.com/gamingdoom/neutron/wiki) 中找到更多信息。

  ## 制作应用

  目前，Neutron 应用程序只能在 Linux 上构建。

  ```bash
  git clone https://github.com/gamingdoom/neutron.git --recurse-submodules -j8
  cd neutron
  pip install -r requirements.txt
  python configurator.py
  cd build
  python build.py
  ```

# 缘何如是？

  Neutron 能够使整个互联网从中获益，它使当前应用生态的多元化发展迈向新的一步，也利用一种不同的技术路线，对当下一切 Web 应用皆基于 Chromium 的现状发起挑战。尽管可能力量微小，但也是星星之火可以燎原。我们认为，更多的人应当拥有这份选择的权利，使其**能够**使用非 Chromium 的浏览器所构建的内容，无论这是否更加自由，这都是用户所应有的权利。我们所做的，也正是迈出打破 Chromium 浏览器垄断的一小步。
