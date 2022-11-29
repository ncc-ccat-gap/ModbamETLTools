#!/usr/bin/env python

import sys
import pysam
import logging
import argparse
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def main():
    args = parse_option()
    input_bam_filepath = args.input
    output_dir_path = args.output

    basename_without_ext = os.path.splitext(os.path.basename(input_bam_filepath))[0]
    output_split_hp1_bam = output_dir_path + "/" + basename_without_ext + "_HP1.bam"
    output_split_hp2_bam = output_dir_path + "/" + basename_without_ext + "_HP2.bam"
    output_split_hp_none_bam = output_dir_path + "/" + basename_without_ext + "_HP_none.bam"

    
    input_bam = pysam.AlignmentFile(input_bam_filepath, "rb")
    output_bam_hp1 = pysam.AlignmentFile(output_split_hp1_bam, "wb", template = input_bam)
    output_bam_hp2 = pysam.AlignmentFile(output_split_hp2_bam, "wb", template = input_bam)
    output_bam_hp_none = pysam.AlignmentFile(output_split_hp_none_bam, "wb", template = input_bam)

    for read in input_bam.fetch(until_eof = True):
        if read.has_tag("HP"):
            if read.get_tag("HP") == 1:
                output_bam_hp1.write(read)
            elif read.get_tag("HP") == 2:
                output_bam_hp2.write(read)
            else:
                output_bam_hp_none.write(read)
        else:
            output_bam_hp_none.write(read)

    input_bam.close()
    output_bam_hp1.close()
    output_bam_hp2.close()
    output_bam_hp_none.close()

    pysam.index(output_split_hp1_bam)
    pysam.index(output_split_hp2_bam)
    pysam.index(output_split_hp_none_bam)
    
def parse_option():
    parser = argparse.ArgumentParser(description='Export bam file split by HP tag')
    parser.add_argument('-i', '--input', help="Input bam file path.")
    parser.add_argument('-o', '--output', help="Enter the path to output dirctory")

    args = parser.parse_args()

    if not os.path.exists(args.input):
        logger.error("[ERROR] Bam file does not exist.")
        exit(1)
        
    # Check output dir
    if args.output is None:
        args.output = os.getcwd()
    else:
        if not os.path.exists(args.output):
            os.mkdir(args.output)
            
    return args

if __name__ == '__main__':
    main()
