#!/usr/bin/python
import json
import argparse
import requests
import os

import vtracer

parser = argparse.ArgumentParser(
    description="This program generates a Neutron config.json and icon files from a PWA manifest.json URL. Output will be written to the specified directory."
)

parser.add_argument(
    "manifest",
    help="URL of a PWA manifest.json file."
)

parser.add_argument(
    "output",
    help="Output directory."
)

def main(args: argparse.Namespace):
    manifest = requests.get(args.manifest).json()
    base_dir = "/".join(args.manifest.split("/")[:-1])
    
    config = {}

    config["appName"] = manifest["name"] if "name" in manifest else manifest["short_name"]
    config["internalAppName"] = manifest["short_name"].replace(" ", "-").lower() if "short_name" in manifest else manifest["name"].replace(" ", "-").lower()
    config["url"] = base_dir + ("/" if not manifest["start_url"].startswith("/") else "") + manifest["start_url"]

    config["version"] = "1.0.0"
    config["author"] = "undefined"
    config["projectDescription"] = "undefined"
    config["projectURL"] = "undefined"
    config["projectHelpURL"] = "undefined"
    
    scopes = []
    if "scope" in manifest:
        scopes.append(manifest["scope"].replace("https://", "http[s]?://"))

    if "scope_extensions" in manifest:
        for ext in manifest["scope_extensions"]:
            if ext["type"] == "origin":
                scopes.append(ext["origin"].replace("https://", "http[s]?://"))
    
    config["openInDefaultBrowser"] = len(scopes) > 0
    config["openInDefaultBrowserRegex"] = "|".join(scopes)

    config["runInBackground"] = True
    
    config["platforms"] = [
        "linux",
        "deb",
        "appimage",
        "linux-aarch64",
        "appimage-aarch64",
        "deb-aarch64",
        "windows",
        "mac-arm",
        "mac-intel"
    ]

    config["logoSvgFilePath"] = f"../{args.output}/icon.svg"

    if manifest["display"] != "standalone":
        print(f"PWA manifest property \"display\" is \"{manifest['display']}\", but Neutron only supports \"standalone\". Skipping...")

    for k in manifest.keys():
        if k not in ["name", "short_name", "start_url", "scope", "icons", "display"]:
            print(f"PWA manifest property {k} not supported in Neutron! Skipping...")

    os.makedirs(args.output, exist_ok=True)

    with open(f"{args.output}/config.json", "w") as f:
        json.dump(config, f, indent=4)

    # Generate icon
    best_candidate = None
    best_size = 0
    is_svg = False
    for icon in manifest["icons"]:
        if icon["src"].endswith(".svg"):
            is_svg = True
            best_candidate = icon

        if "sizes" in icon:
            sizes = icon["sizes"].split(" ")
            highest_sz = 0
            for sz in sizes:
                if int(sz.split("x")[0]) > highest_sz:
                    highest_sz = int(sz.split("x")[0])
            
            if highest_sz > best_size and not is_svg:
                best_candidate = icon
                best_size = highest_sz
                
        if best_candidate is None and icon["src"].endswith(".png"):
            best_candidate = icon

        if best_candidate is None:
            best_candidate = icon

    if is_svg:
        r = requests.get(base_dir + "/" + best_candidate["src"])
        with open(f"{args.output}/icon.svg", "w") as f:
            f.write(r.text)
    else:
        r = requests.get(base_dir + "/" + best_candidate["src"])
        fname = best_candidate["src"].split("/")[-1]
        with open(f"{args.output}/" + fname, "wb") as f:
            f.write(r.content)
        
        vtracer.convert_image_to_svg_py(f"{args.output}/{fname}", f"{args.output}/icon.svg")

        os.remove(f"{args.output}/" + fname)

    print(f"Done! To build run:\npython configurator.py -c {args.output}/config.json")

if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
