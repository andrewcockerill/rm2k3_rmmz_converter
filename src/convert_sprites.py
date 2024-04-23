# Packages
import os
import argparse
from utils import SpriteConverter
import re

# Constants
INPUT_DIR = "input_files"
OUTPUT_DIR = "output_files"
OUTPUT_SUFFIX = "_converted.png"
INPUT_FILES = [os.path.join(INPUT_DIR, file) for file in os.listdir(
    INPUT_DIR) if bool(re.search("png$", file))]
OUTPUT_FILES = [os.path.join(OUTPUT_DIR, re.sub(r"\.png", OUTPUT_SUFFIX, file)) for file in os.listdir(
    INPUT_DIR) if bool(re.search("png$", file))]

# Args
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--scale")
args = parser.parse_args()
scale_factor = int(args.scale) if args.scale else 1

# Conversions
conversions_to_do = list(zip(INPUT_FILES, OUTPUT_FILES))
num_conversions = len(conversions_to_do)
if num_conversions > 0:
    print(f"Running conversions for {str(num_conversions)} file(s):")
    for c in conversions_to_do:
        SpriteConverter(c[0]).scale(
            scale_factor).reposition_rm2k_to_mz().remove_bg().save_image(c[1])
    print('Done.')
else:
    print('No .png files found in input_files directory')
