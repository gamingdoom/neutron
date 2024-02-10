#!/usr/bin/python
import json
from PIL import Image
from cairosvg import svg2png
import os
import subprocess
import shutil

def replaceTextInFile(filePath: str, old: str, new: str) -> None:
    with open(filePath, "r") as f:
        data = f.read()
    
    data = data.replace(old, new)

    with open(filePath, "w") as f:
        f.write(data)

def build(component: str) -> bool:
    if component not in os.listdir("src/scripts/build"):
        print(f"Neutron does not support building for {component}.")
        return False
    
    completed = subprocess.run(f"src/scripts/build/{component}")
    if completed.returncode == 0:
        print(f"Build for {component} success!")
        return True
    else:
        print(f"Build for {component} failed!")
        return False 

def main():
    with open("config.json", "r") as f:
        appinfo = json.load(f)

    # Make changes to firefox

    # Create branding
    shutil.copytree("src/branding-template", f"src/changed/browser/branding/{appinfo['internalAppName']}", dirs_exist_ok=True)
    
    # List of icons that need to be created    
    pngIcons = {
        f"src/changed/browser/branding/{appinfo['internalAppName']}/default16.png": 16,
        f"src/changed/browser/branding/{appinfo['internalAppName']}/default22.png": 22,
        f"src/changed/browser/branding/{appinfo['internalAppName']}/default24.png": 24,
        f"src/changed/browser/branding/{appinfo['internalAppName']}/default32.png": 32,
        f"src/changed/browser/branding/{appinfo['internalAppName']}/default48.png": 48,
        f"src/changed/browser/branding/{appinfo['internalAppName']}/default64.png": 64,
        f"src/changed/browser/branding/{appinfo['internalAppName']}/default128.png": 128,
        f"src/changed/browser/branding/{appinfo['internalAppName']}/default256.png": 256,
        f"src/changed/browser/branding/{appinfo['internalAppName']}/VisualElements_70.png": 70,
        f"src/changed/browser/branding/{appinfo['internalAppName']}/VisualElements_150.png": 150,
        f"src/changed/browser/branding/{appinfo['internalAppName']}/msix/Assets/SmallTile.scale-200.png": 96,
        f"src/changed/browser/branding/{appinfo['internalAppName']}/msix/Assets/LargeTile.scale-200.png": 256,
        f"src/changed/browser/branding/{appinfo['internalAppName']}/msix/Assets/Square150x150Logo.scale-200.png": 150,
        f"src/changed/browser/branding/{appinfo['internalAppName']}/msix/Assets/Square44x44Logo.altform-lightunplated_targetsize-256.png": 256,
        f"src/changed/browser/branding/{appinfo['internalAppName']}/msix/Assets/Square44x44Logo.altform-unplated_targetsize-256.png": 256,
        f"src/changed/browser/branding/{appinfo['internalAppName']}/msix/Assets/Square44x44Logo.scale-200.png": 256,
        f"src/changed/browser/branding/{appinfo['internalAppName']}/msix/Assets/Square44x44Logo.targetsize-256.png": 256,
        f"src/changed/browser/branding/{appinfo['internalAppName']}/msix/Assets/StoreLogo.scale-200.png": 256,
        f"src/packages/appimage/neutron.AppImage/.DirIcon": 256,
        f"src/packages/appimage/neutron.AppImage/icon256.png": 256,
        f"src/packages/appimage/neutron.AppImage/usr/share/icons/{appinfo['internalAppName']}256.png": 256,
    }
    icoIcons = {
        f"src/changed/browser/branding/{appinfo['internalAppName']}/firefox64.ico": [256,128,64,48,32,24,22,16],
        f"src/changed/browser/branding/{appinfo['internalAppName']}/firefox.ico": [256,128,64,48,32,24,22,16],
        f"src/windows/{appinfo['internalAppName']}.ico": [256,128,64,48,32,24,22,16]
    }
    icnsIcons = {
        f"src/changed/browser/branding/{appinfo['internalAppName']}/firefox.icns": 512
    }

    for path, size in pngIcons.items():
        svg2png(url=appinfo["logoSvgFilePath"], write_to=path, output_height=size, output_width=size)

    #with open(f"src/changed/browser/branding/{appinfo['internalAppName']}/default256.png", "r") as iconFile:
    im = Image.open(f"src/changed/browser/branding/{appinfo['internalAppName']}/default256.png")

    for path, sizes in icoIcons.items():
        im.save(path, sizes=[(x, x) for x in sizes], bitmap_format="bmp")

    # Make banner
    #with open(f"src/changed/browser/branding/{appinfo['internalAppName']}/default128.png", "r") as iconFile:
    im = Image.open(f"src/changed/browser/branding/{appinfo['internalAppName']}/default128.png")

    banner = Image.new(size=(164, 314), color="white", mode="RGBA")
    # (164/2)-64=18 and (314/2)-64=93
    banner.paste(im, (18, 93), im)
    banner.save("src/windows/banner.bmp", bitmap_format="bmp")

    for path, size in icnsIcons.items():
        svg2png(url=appinfo["logoSvgFilePath"], write_to="temp.png", output_height=size, output_width=size)
        im = Image.open("temp.png")
        im.save(path)
        os.remove("temp.png")

    # Create the disk icon that shows up when you mount the dmg
    im = Image.open(f"src/changed/browser/branding/{appinfo['internalAppName']}/disk.icns")
    

    # Replace placeholders with actual info
    replaceTextInFile(f"src/changed/browser/branding/{appinfo['internalAppName']}/pref/firefox-branding.js", "NEUTRON_APP_URL", appinfo["url"])

    replaceTextInFile(f"src/changed/browser/branding/{appinfo['internalAppName']}/configure.sh", "NEUTRON_INTERNAL_APP_NAME", appinfo["internalAppName"])
    replaceTextInFile(f"src/changed/browser/branding/{appinfo['internalAppName']}/configure.sh", "NEUTRON_APP_NAME", appinfo["appName"])

    replaceTextInFile(f"src/changed/browser/branding/{appinfo['internalAppName']}/locales/en-US/brand.properties", "NEUTRON_INTERNAL_APP_NAME", appinfo["internalAppName"])
    replaceTextInFile(f"src/changed/browser/branding/{appinfo['internalAppName']}/locales/en-US/brand.properties", "NEUTRON_APP_NAME", appinfo["appName"])
    
    replaceTextInFile(f"src/changed/browser/branding/{appinfo['internalAppName']}/locales/en-US/brand.dtd", "NEUTRON_INTERNAL_APP_NAME", appinfo["internalAppName"])
    replaceTextInFile(f"src/changed/browser/branding/{appinfo['internalAppName']}/locales/en-US/brand.dtd", "NEUTRON_APP_NAME", appinfo["appName"])
    
    replaceTextInFile(f"src/changed/browser/branding/{appinfo['internalAppName']}/locales/en-US/brand.ftl", "NEUTRON_INTERNAL_APP_NAME", appinfo["internalAppName"])
    replaceTextInFile(f"src/changed/browser/branding/{appinfo['internalAppName']}/locales/en-US/brand.ftl", "NEUTRON_APP_NAME", appinfo["appName"])

    replaceTextInFile(f"src/changed/browser/branding/{appinfo['internalAppName']}/branding.nsi", "NEUTRON_INTERNAL_APP_NAME", appinfo["internalAppName"])
    replaceTextInFile(f"src/changed/browser/branding/{appinfo['internalAppName']}/branding.nsi", "NEUTRON_APP_NAME", appinfo["appName"])
    replaceTextInFile(f"src/changed/browser/branding/{appinfo['internalAppName']}/branding.nsi", "NEUTRON_PROJECT_URL", appinfo["projectURL"])
    replaceTextInFile(f"src/changed/browser/branding/{appinfo['internalAppName']}/branding.nsi", "NEUTRON_PROJECT_HELP_URL", appinfo["projectHelpURL"])
    
    replaceTextInFile("src/mozconfig.linux", "NEUTRON_INTERNAL_APP_NAME", appinfo["internalAppName"])
    replaceTextInFile("src/mozconfig.linux", "NEUTRON_APP_NAME", appinfo["appName"])
    replaceTextInFile("src/mozconfig.linux-aarch64", "NEUTRON_INTERNAL_APP_NAME", appinfo["internalAppName"])
    replaceTextInFile("src/mozconfig.linux-aarch64", "NEUTRON_APP_NAME", appinfo["appName"])
    replaceTextInFile("src/mozconfig.windows", "NEUTRON_INTERNAL_APP_NAME", appinfo["internalAppName"])
    replaceTextInFile("src/mozconfig.windows", "NEUTRON_APP_NAME", appinfo["appName"])
    replaceTextInFile("src/mozconfig.mac-arm", "NEUTRON_INTERNAL_APP_NAME", appinfo["internalAppName"])
    replaceTextInFile("src/mozconfig.mac-arm", "NEUTRON_APP_NAME", appinfo["appName"])
    replaceTextInFile("src/mozconfig.mac-intel", "NEUTRON_INTERNAL_APP_NAME", appinfo["internalAppName"])
    replaceTextInFile("src/mozconfig.mac-intel", "NEUTRON_APP_NAME", appinfo["appName"])

    replaceTextInFile("src/scripts/build/launch-app-linux", "NEUTRON_OPEN_IN_DEFAULT_BROWSER", str(appinfo["openInDefaultBrowser"]).lower())
    replaceTextInFile("src/scripts/build/launch-app-linux", "NEUTRON_INTERNAL_APP_NAME", appinfo["internalAppName"])
    replaceTextInFile("src/scripts/build/launch-app-linux", "NEUTRON_SHOULD_RUN_IN_BACKGROUND", str(appinfo["runInBackground"]).lower())

    replaceTextInFile("src/scripts/build/launch-app-linux-aarch64", "NEUTRON_OPEN_IN_DEFAULT_BROWSER", str(appinfo["openInDefaultBrowser"]).lower())
    replaceTextInFile("src/scripts/build/launch-app-linux-aarch64", "NEUTRON_INTERNAL_APP_NAME", appinfo["internalAppName"])
    replaceTextInFile("src/scripts/build/launch-app-linux-aarch64", "NEUTRON_SHOULD_RUN_IN_BACKGROUND", str(appinfo["runInBackground"]).lower())

    replaceTextInFile("src/scripts/build/launch-app-windows", "NEUTRON_OPEN_IN_DEFAULT_BROWSER", str(appinfo["openInDefaultBrowser"]).lower())
    replaceTextInFile("src/scripts/build/launch-app-windows", "NEUTRON_INTERNAL_APP_NAME", appinfo["internalAppName"])
    replaceTextInFile("src/scripts/build/launch-app-windows", "NEUTRON_SHOULD_RUN_IN_BACKGROUND", str(appinfo["runInBackground"]).lower())

    replaceTextInFile("src/scripts/build/launch-app-mac-arm", "NEUTRON_OPEN_IN_DEFAULT_BROWSER", str(appinfo["openInDefaultBrowser"]).lower())
    replaceTextInFile("src/scripts/build/launch-app-mac-arm", "NEUTRON_INTERNAL_APP_NAME", appinfo["internalAppName"])
    replaceTextInFile("src/scripts/build/launch-app-mac-arm", "NEUTRON_SHOULD_RUN_IN_BACKGROUND", str(appinfo["runInBackground"]).lower())

    replaceTextInFile("src/scripts/build/launch-app-mac-intel", "NEUTRON_OPEN_IN_DEFAULT_BROWSER", str(appinfo["openInDefaultBrowser"]).lower())
    replaceTextInFile("src/scripts/build/launch-app-mac-intel", "NEUTRON_INTERNAL_APP_NAME", appinfo["internalAppName"])
    replaceTextInFile("src/scripts/build/launch-app-mac-intel", "NEUTRON_SHOULD_RUN_IN_BACKGROUND", str(appinfo["runInBackground"]).lower())

    replaceTextInFile("src/windows/app.rc", "NEUTRON_INTERNAL_APP_NAME", appinfo["internalAppName"])

    replaceTextInFile("src/mac/Info-aarch64.plist", "NEUTRON_INTERNAL_APP_NAME", appinfo["internalAppName"])
    replaceTextInFile("src/mac/Info-aarch64.plist", "NEUTRON_APP_NAME", appinfo["appName"])
    replaceTextInFile("src/mac/Info-aarch64.plist", "NEUTRON_APP_VERSION", appinfo["version"])

    replaceTextInFile("src/mac/Info-x86_64.plist", "NEUTRON_INTERNAL_APP_NAME", appinfo["internalAppName"])
    replaceTextInFile("src/mac/Info-x86_64.plist", "NEUTRON_APP_NAME", appinfo["appName"])
    replaceTextInFile("src/mac/Info-x86_64.plist", "NEUTRON_APP_VERSION", appinfo["version"])

    if appinfo["openInDefaultBrowser"]:
        replaceTextInFile("src/open-in-default-browser/open-in-default-browser-ext/replaceLinks.js", "NEUTRON_EXCLUDE_REGEX_PATTERN", appinfo["openInDefaultBrowserRegex"])
    
    replaceTextInFile("src/windows/setup.nsi", "NEUTRON_INTERNAL_APP_NAME", appinfo["internalAppName"])
    replaceTextInFile("src/windows/setup.nsi", "NEUTRON_APP_NAME", appinfo["appName"])
    replaceTextInFile("src/windows/setup.nsi", "NEUTRON_APP_VERSION", appinfo["version"])

    replaceTextInFile("src/mozilla_dirsFromLibreWolf.patch", "NEUTRON_INTERNAL_APP_NAME", appinfo["internalAppName"])
    replaceTextInFile("src/mozilla_dirsFromLibreWolf.patch", "NEUTRON_APP_NAME", appinfo["appName"])

    replaceTextInFile("src/distribution/policies-windows.json", "NEUTRON_APP_NAME", appinfo["appName"])
    windowsExtUrls = appinfo["extensionURLs"].copy()
    windowsExtUrls.remove("NEUTRON_OPEN_IN_DEFAULT_BROWSER_EXTENSION_LOCATION")
    windowsExtUrls.append(f"file:///C:\\Program%20Files\\{appinfo['appName'].replace(' ', '%20')}\\open_in_default_browser-1.0.zip")
    replaceTextInFile("src/distribution/policies-windows.json", "NEUTRON_EXTENSION_URLS", str(windowsExtUrls).replace("'", '"'))

    replaceTextInFile("src/distribution/policies-linux.json", "NEUTRON_EXTENSION_URLS", str(appinfo["extensionURLs"]).replace("'", '"'))

    replaceTextInFile("src/distribution/policies-linux-appimage.json", "NEUTRON_EXTENSION_URLS", str(appinfo["extensionURLs"]).replace("'", '"'))

    replaceTextInFile("src/distribution/policies-flatpak.json", "NEUTRON_EXTENSION_URLS", str(appinfo["extensionURLs"]).replace("'", '"'))

    replaceTextInFile("src/scripts/build/linux", "NEUTRON_INTERNAL_APP_NAME", appinfo["internalAppName"])

    replaceTextInFile("src/scripts/build/linux-aarch64", "NEUTRON_INTERNAL_APP_NAME", appinfo["internalAppName"])

    replaceTextInFile("src/scripts/build/windows", "NEUTRON_INTERNAL_APP_NAME", appinfo["internalAppName"])

    replaceTextInFile("src/scripts/build/mac-arm", "NEUTRON_INTERNAL_APP_NAME", appinfo["internalAppName"])
    replaceTextInFile("src/scripts/build/mac-arm", "NEUTRON_APP_NAME", appinfo["appName"])

    replaceTextInFile("src/scripts/build/mac-intel", "NEUTRON_INTERNAL_APP_NAME", appinfo["internalAppName"])
    replaceTextInFile("src/scripts/build/mac-intel", "NEUTRON_APP_NAME", appinfo["appName"])

    replaceTextInFile("src/packages/appimage/neutron.AppImage/neutron.desktop", "NEUTRON_INTERNAL_APP_NAME", appinfo["internalAppName"])
    replaceTextInFile("src/packages/appimage/neutron.AppImage/neutron.desktop", "NEUTRON_APP_NAME", appinfo["appName"])

    replaceTextInFile("src/packages/appimage/neutron.AppImage/AppRun", "NEUTRON_INTERNAL_APP_NAME", appinfo["internalAppName"])
    replaceTextInFile("src/packages/appimage/neutron.AppImage/AppRun", "NEUTRON_APP_NAME", appinfo["appName"])

    replaceTextInFile("src/scripts/build/appimage", "NEUTRON_INTERNAL_APP_NAME", appinfo["internalAppName"])
    replaceTextInFile("src/scripts/build/appimage", "NEUTRON_APP_NAME", appinfo["appName"])

    replaceTextInFile("src/scripts/build/appimage-aarch64", "NEUTRON_INTERNAL_APP_NAME", appinfo["internalAppName"])
    replaceTextInFile("src/scripts/build/appimage-aarch64", "NEUTRON_APP_NAME", appinfo["appName"])

    # Finally, lets start building.
    if not build("download-firefox-source"):
        print("Couldn't download the Firefox source code.")
        exit(1)

    if appinfo["openInDefaultBrowser"]:
        if not build("open-in-default-browser"):
            print("Error building open-in-default-browser extension!")
            exit(1)

    if "linux" in appinfo["platforms"]:
        if not build("launch-app-linux"):
            print("Error building launch-app-linux!")
            exit(1)

    if "linux-aarch64" in appinfo["platforms"]:
        if not build("launch-app-linux-aarch64"):
            print("Error building launch-app-linux-aarch64!")
            exit(1)

    if "windows" in appinfo["platforms"]:
        if not build("launch-app-windows"):
            print("Error building launch-app-windows!")
            exit(1)

    if "mac-arm" in appinfo["platforms"]:
        if not build("launch-app-mac-arm"):
            print("Error building launch-app-mac-arm")
            exit(1)

    if "mac-intel" in appinfo["platforms"]:
        if not build("launch-app-mac-intel"):
            print("Error building launch-app-mac-intel")
            exit(1)
            
    # If we build appimage but not linux
    if "appimage" in appinfo["platforms"] and "linux" not in appinfo["platforms"]:
        appinfo["platforms"].insert(appinfo["platforms"].index("appimage"), "linux")

    if "appimage-aarch64" in appinfo["platforms"] and "linux-aarch64" not in appinfo["platforms"]:
        appinfo["platforms"].insert(appinfo["platforms"].index("appimage-aarch64"), "linux-aarch64")

    for component in appinfo["platforms"]:
        if not build(component):
            print(f"Error building component {component}!")
            exit(1)

    print("Done Building!")
    return

if __name__ == "__main__":
    main()
