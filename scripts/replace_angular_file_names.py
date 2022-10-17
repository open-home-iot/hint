import argparse
import re

from os import listdir
from os.path import isfile, join

from bs4 import BeautifulSoup


argparser = argparse.ArgumentParser(description="""
Takes the input Angular bundle and index file and ensures that the bundle 
contents are referenced correctly in the index.html file. It also handles
production/non-production builds, excluding/including, the vendor.js bundle.

The whole idea is that this script is used on the index.html found in the 
Django templates directory when a ready build exists that is about to go into
production. Use the script to replace the static filenames (used during 
development) with the new cache-busting names.

The script outputs a 'built_index.html' file in the same directory as the input
index.html.
""")
argparser.add_argument("built_angular_path",
                       type=str,
                       help="Path to the built Angular bundle.")
argparser.add_argument("index_file",
                       type=str,
                       help="Path to the index file to update with Angular "
                            "file names")
args = argparser.parse_args()
print(args)
print(f"Built Angular path = {args.built_angular_path}")
print(f"Index file = {args.index_file}")

files = [file for file in listdir(args.built_angular_path)
         if isfile(join(args.built_angular_path, file))
         and file.endswith(".js") or file.endswith(".css")]
print(f"Found Angular files: {files}")


def staticwrap(filepath: str) -> str:
    """Wraps a filename in a Django static template tag."""
    return "{% static 'ang/" + filepath + "' %}"


filename_main = staticwrap(
    [file for file in files if file.startswith("main")][0]
)
filename_poly = staticwrap(
    [file for file in files if file.startswith("polyfills")][0]
)
filename_runtime = staticwrap(
    [file for file in files if file.startswith("runtime")][0]
)

vendor_list = [file for file in files if file.startswith("vendor")]
optional_filename_vendor = \
    staticwrap(vendor_list[0]) if len(vendor_list) > 0 else None

filename_styles = staticwrap(
    [file for file in files if file.startswith("styles")][0]
)

print("\nLoad up the original index and replace main, runtime, polyfills and "
      "styles...")
with open(args.index_file, "r") as index_file:
    soup = BeautifulSoup(index_file, "html.parser")
    # Main
    print("\nLooking for main script tag")
    found = soup.find(name="script", attrs={"src": re.compile("main.*[.]js")})
    print("Found:", found)
    print("Replacing 'src' with:", filename_main)
    found.attrs["src"] = filename_main

    # Poly
    print("\nLooking for poly script tag")
    found = soup.find(name="script", attrs={"src": re.compile("polyfills.*[.]js")})
    print("Found:", found)
    print("Replacing 'src' with:", filename_poly)
    found.attrs["src"] = filename_poly

    # Runtime
    print("\nLooking for runtime script tag")
    found = soup.find(name="script", attrs={"src": re.compile("runtime.*[.]js")})
    print("Found:", found)
    print("Replacing 'src' with:", filename_runtime)
    found.attrs["src"] = filename_runtime

    # Styles
    print("\nLooking for styles link tag")
    found = soup.find(name="link", attrs={"href": re.compile("styles.*[.]css")})
    print("Found:", found)
    print("Replacing 'href' with:", filename_styles)
    found.attrs["href"] = filename_styles

    # Vendor
    print("\nFinding if original has a vendor script tag")
    found = soup.find(name="script", attrs={"src": re.compile("vendor.*[.]js")})
    if found:
        print("Found:", found)
        if optional_filename_vendor is None:
            print("No vendor in bundle, removing")
            found.extract()
        else:
            print("Vendor in bundle, replacing")
            found.attrs["src"] = optional_filename_vendor
    elif optional_filename_vendor:
        print("Not found and vendor exists in bundle, adding")
        soup.body.append(soup.new_tag("script", src=optional_filename_vendor,
                                      type="module"))

    print("#################################################################")
    print("Resulting template:")
    print(soup)

    with open(args.index_file.replace("index.html", "built_index.html"), "w") \
            as new_index_file:
        new_index_file.write(soup.prettify())
