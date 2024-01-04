#!/usr/bin/python
import json
import re
import os
import shutil
import sys

def main():
    if len(sys.argv) == 1:
        print("This will guide you through the process of configuring Neutron.")

        appinfo = {}
        appinfo["appName"] = input("Enter the name of your application (example: Datcord):\n")
        appinfo["internalAppName"] = appinfo["appName"].replace(" ", "-").lower()
        appinfo["url"] = input("Please enter the URL of your application (example: https://discord.com/app):\n")
        appinfo["logoSvgFilePath"] = os.path.abspath(input("Please provide a path to a SVG of the application's logo (example: ../src/datcord.svg):\n"))
        while True:
            try:
                appinfo["platforms"] = json.loads('{"array":' + input('List of lowercase platform names to build for (example: ["linux", "windows", "appimage", "flatpak"]):\n') + "}")["array"]
                break
            except json.JSONDecodeError:
                print("Please enter the platforms in the same format as the example.")

        try:
            appinfo["extensionURLs"] = json.loads('{"array":' + input('List URLs of extensions to install (example: ["https://example.com/extension.zip"]):\n') + "}")["array"]
        except json.JSONDecodeError:
            appinfo["extensionURLs"] = []

        appinfo["version"] = input("Enter the application version:\n")
        appinfo["projectURL"] = input("Enter the URL to your project (example: https://github.com/gamingdoom/datcord):\n")
        appinfo["projectHelpURL"] = input("Enter the help URL for your project (example: https://github.com/gamingdoom/datcord/issues):\n")

        while True:
            answer = input("Allow links to open in the default browser? [y/n]\n")
            if answer == ("y" or "Y"):
                appinfo["openInDefaultBrowser"] = True
                if not shutil.which("web-ext"):
                    print("web-ext missing! It must be installed to build support for opening links in the default browser.")
                    exit(1)

                while True:
                    appinfo["openInDefaultBrowserRegex"] = input("Please enter a regular expression that matches links that shouldn't open in the default browser (example: http[s]?://discord.com):\n")
                    try:
                        pattern = re.compile(appinfo["openInDefaultBrowserRegex"])
                        if not pattern.match(appinfo["url"]):
                            print("The provided pattern matched the url of the application!")
                            continue
                        break
                    except:
                        print("Invalid regular expression!")
                        continue
                break
            elif answer == ("n" or "N"):
                appinfo["openInDefaultBrowser"] = False
                break

        if appinfo["openInDefaultBrowser"]:
            appinfo["extensionURLs"].append("NEUTRON_OPEN_IN_DEFAULT_BROWSER_EXTENSION_LOCATION")

    elif sys.argv[1].startswith("--config-file="):
        with open(sys.argv[1].split("=")[1], "r") as f:
            appinfo = json.load(f)

    if os.path.exists("build"):
        print("Clearing build folder!")
        shutil.rmtree("build")

    os.mkdir("build")
    shutil.copyfile("src/scripts/build.py", "build/build.py")
    shutil.copytree("src", "build/src")

    with open("build/config.json", "w") as f:
        json.dump(appinfo, f, indent=4)
    
    print("Done! Run build.py in the build directory to build.")

    return

if __name__ == "__main__":
    main()