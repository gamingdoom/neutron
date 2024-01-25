/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

 // open links in default browser
pref("network.protocol-handler.external.open", true);
pref("network.protocol-handler.warn-external.open", true);
pref("network.protocol-handler.expose.open", false);

pref("permissions.default.camera", 1);
pref("permissions.default.microphone", 1);

pref("browser.link.open_newwindow", 1);
pref("browser.warnOnQuit", false);
pref("browser.uitour.enabled", false);
pref("browser.privatebrowsing.vpnpromourl", "");
pref("browser.tabs.inTitlebar", 0);

pref("browser.startup.upgradeDialog.enabled", false);
pref("browser.startup.firstrunSkipsHomepage", false);
pref("browser.startup.page",                1);
pref("browser.startup.homepage",            "NEUTRON_APP_URL");

pref("browser.shell.setDefaultPDFHandler", false);
pref("browser.shell.setDefaultBrowserUserChoice", false);
pref("browser.shell.checkDefaultBrowser", false);
pref("browser.shell.skipDefaultBrowserCheckOnFirstRun", true);
#ifdef XP_WIN
  pref("default-browser-agent.enabled", false);
#endif


pref("browser.urlbar.suggest.bookmark",             false);
pref("browser.urlbar.suggest.history",              false);
pref("browser.urlbar.suggest.openpage",             false);
pref("browser.urlbar.suggest.remotetab",            false);
pref("browser.urlbar.suggest.searches",             false);
pref("browser.urlbar.suggest.topsites",             false);
pref("browser.urlbar.suggest.engines",              false);

pref("xpinstall.signatures.required", false);

// Don't show session restore page
pref("browser.sessionstore.max_tabs_undo", 0);
pref("browser.sessionstore.max_windows_undo", 0);
pref("browser.sessionstore.max_resumed_crashes", 0);
pref("browser.sessionstore.resume_from_crash", false);
pref("browser.sessionstore.collect_session_storage", false);
pref("browser.sessionstore.restore_on_demand", false);
pref("browser.startup.couldRestoreSession.count", -1);
