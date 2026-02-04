#!/usr/bin/python
from datetime import datetime
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


def replace_placeholders(placeholder_files: list[str], placeholders: dict[str, str]) -> None:
    for file in placeholder_files:
        file_name = os.path.basename(file)

        for placeholder, value in placeholders.items():
            replaceTextInFile(file, placeholder, value)

            # Also replace placeholders in file names
            if placeholder in file_name:
                file_name = file_name.replace(placeholder, value)
        
        os.rename(file, os.path.join(os.path.dirname(file), file_name))
        
def make_alphanumeric(s: str, replace_spaces: bool = True) -> str:
    out = ""
    for c in s.strip():
        if c.isalnum() or c == "_":
            out += c
        if c == " " or c == "-":
            if replace_spaces:
                out += "_"
            else:
                out += c

    return out

def remove_unsafe_characters(s: str) -> str:
    out = ""
    for c in s:
        if c in "\\/:*?\"'<>|$()":
            out += "_"
        else:
            out += c

    return out

def sanitize(s: str, replace_spaces: bool = True) -> str:
    return remove_unsafe_characters(make_alphanumeric(s.strip(), replace_spaces = replace_spaces))

def main():
    with open("config.json", "r") as f:
        appinfo = json.load(f)

    appinfo["internalAppName"] = sanitize(appinfo["appName"]).lower()
    appinfo["appName"] = sanitize(appinfo["appName"], replace_spaces = False)
    appinfo["author"] = sanitize(appinfo["author"], replace_spaces = False)

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

    im = Image.open(f"src/changed/browser/branding/{appinfo['internalAppName']}/default256.png")

    for path, sizes in icoIcons.items():
        im.save(path, sizes=[(x, x) for x in sizes], bitmap_format="bmp")

    # Make banner
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
    
    # I made changes to the config format so lets fix old configs.
    if "NEUTRON_OPEN_IN_DEFAULT_BROWSER_EXTENSION_LOCATION" in appinfo["extensionURLs"]:
        appinfo["extensionURLs"].remove("NEUTRON_OPEN_IN_DEFAULT_BROWSER_EXTENSION_LOCATION")

    placeholder_files = [
        f"src/changed/browser/branding/{appinfo['internalAppName']}/pref/firefox-branding.js",
        f"src/changed/browser/branding/{appinfo['internalAppName']}/configure.sh",
        f"src/changed/browser/branding/{appinfo['internalAppName']}/locales/en-US/brand.properties",
        f"src/changed/browser/branding/{appinfo['internalAppName']}/locales/en-US/brand.dtd",
        f"src/changed/browser/branding/{appinfo['internalAppName']}/locales/en-US/brand.ftl",
        f"src/changed/browser/branding/{appinfo['internalAppName']}/branding.nsi",
        
        "src/changed/build/application.ini.in",

        "src/mozconfig.linux",
        "src/mozconfig.linux-aarch64",
        "src/mozconfig.windows",
        "src/mozconfig.mac-arm",
        "src/mozconfig.mac-intel",
        "src/mozconfig.flatpak",

        "src/scripts/build/launch-app-linux",
        "src/scripts/build/launch-app-linux-aarch64",
        "src/scripts/build/launch-app-windows",
        "src/scripts/build/launch-app-mac-arm",
        "src/scripts/build/launch-app-mac-intel",
        "src/scripts/build/launch-app-flatpak",

        "src/windows/app.rc",
        "src/windows/setup.nsi",

        "src/mac/Info-aarch64.plist",
        "src/mac/Info-x86_64.plist",

        "src/patches/mozilla_dirsFromLibreWolf.patch",
        "src/patches/desktop_file_generator.patch",

        "src/distribution/policies-windows.json",
        "src/distribution/policies-linux.json",
        "src/distribution/policies-linux-appimage.json",
        "src/distribution/policies-flatpak.json",

        "src/scripts/build/linux",
        "src/scripts/build/linux-aarch64",
        "src/scripts/build/windows",
        "src/scripts/build/mac-arm",
        "src/scripts/build/mac-intel",
        "src/scripts/build/flatpak",

        "src/scripts/build/launch-app-linux",
        "src/scripts/build/launch-app-linux-aarch64",
        "src/scripts/build/launch-app-windows",
        "src/scripts/build/launch-app-mac-arm",
        "src/scripts/build/launch-app-mac-intel",
        "src/scripts/build/launch-app-flatpak",

        "src/packages/appimage/neutron.AppImage/neutron.desktop",
        "src/packages/appimage/neutron.AppImage/AppRun",

        "src/packages/debian/install.in",
        "src/packages/debian/control.in",
        "src/packages/debian/distribution.ini",

        "src/packages/flatpak/io.github.NEUTRON_AUTHOR_STRIPPED.NEUTRON_APP_NAME_STRIPPED.yml",
        "src/packages/flatpak/io.github.NEUTRON_AUTHOR_STRIPPED.NEUTRON_APP_NAME_STRIPPED.metainfo.xml",
        "src/packages/flatpak/io.github.NEUTRON_AUTHOR_STRIPPED.NEUTRON_APP_NAME_STRIPPED.desktop",

        "src/scripts/build/package-linux",
        "src/scripts/build/package-linux-aarch64",
        "src/scripts/build/package-appimage",
        "src/scripts/build/package-appimage-aarch64",
        "src/scripts/build/package-deb",
        "src/scripts/build/package-deb-aarch64",
        "src/scripts/build/package-windows",
        "src/scripts/build/package-mac-arm",
        "src/scripts/build/package-mac-intel",
        "src/scripts/build/package-flatpak",
    ]

    placeholders = {
        "NEUTRON_INTERNAL_APP_NAME": appinfo["internalAppName"],
        "NEUTRON_APP_NAME_STRIPPED": appinfo["appName"].replace(" ", ""),
        "NEUTRON_APP_NAME": appinfo["appName"],
        "NEUTRON_APP_URL": appinfo["url"],
        "NEUTRON_PROJECT_URL": appinfo["projectURL"],
        "NEUTRON_PROJECT_HELP_URL": appinfo["projectHelpURL"],
        "NEUTRON_OPEN_IN_DEFAULT_BROWSER": str(appinfo["openInDefaultBrowser"]).lower(),
        "NEUTRON_SHOULD_RUN_IN_BACKGROUND": str(appinfo["runInBackground"]).lower(),
        "NEUTRON_APP_VERSION": appinfo["version"],
        "NEUTRON_EXTENSION_URLS": str(appinfo["extensionURLs"]).replace("'", '"'),
        "NEUTRON_SHOULD_OPEN_IN_DEFAULT_BROWSER": str(int(appinfo["openInDefaultBrowser"])),
        "NEUTRON_AUTHOR_STRIPPED": appinfo["author"].replace(" ", ""),
        "NEUTRON_AUTHOR": appinfo["author"],
        "NEUTRON_PROJECT_DESCRIPTION": appinfo["projectDescription"],
        "NEUTRON_CURRENT_DATE": datetime.now().strftime("%Y-%m-%d"),
    }

    if appinfo["openInDefaultBrowser"]:
        placeholder_files.append("src/open-in-default-browser/open-in-default-browser-ext/extension/replaceLinks.js")
        placeholders["NEUTRON_EXCLUDE_REGEX_PATTERN"] = appinfo["openInDefaultBrowserRegex"]

    replace_placeholders(placeholder_files, placeholders)

    # Finally, lets start building.
    if not build("download-firefox-source"):
        print("Couldn't download the Firefox source code.")
        exit(1)

    if appinfo["openInDefaultBrowser"]:
        if not build("open-in-default-browser"):
            print("Error building open-in-default-browser extension!")
            exit(1)

    buildable_platforms = []
    for platform in appinfo["platforms"]:
        if platform == "appimage":
            buildable_platforms.append("linux")
            buildable_platforms.append("launch-app-linux")
            buildable_platforms.append("package-appimage")
        elif platform == "appimage-aarch64":
            buildable_platforms.append("linux-aarch64")
            buildable_platforms.append("launch-app-linux-aarch64")
            buildable_platforms.append("package-appimage-aarch64")
        elif platform == "deb":
            buildable_platforms.append("linux")
            buildable_platforms.append("launch-app-linux")
            buildable_platforms.append("package-deb")
        elif platform == "deb-aarch64":
            buildable_platforms.append("linux-aarch64")
            buildable_platforms.append("launch-app-linux-aarch64")
            buildable_platforms.append("package-deb-aarch64")
        else:
            buildable_platforms.append(platform)
            if not platform.startswith("launch-app-"):
                buildable_platforms.append(f"launch-app-{platform}")
                buildable_platforms.append(f"package-{platform}")

    buildable_platforms_dedup = []
    [buildable_platforms_dedup.append(x) for x in buildable_platforms if x not in buildable_platforms_dedup]

    for component in buildable_platforms_dedup:
        if not build(component):
            print(f"Error building component {component}!")
            exit(1)

    print("Done Building!")
    return

if __name__ == "__main__":
    main()
