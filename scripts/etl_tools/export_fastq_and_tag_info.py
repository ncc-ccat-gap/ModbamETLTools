#!/usr/bin/env python

import sys
import os
import pysam
import logging
import argparse

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def main():
    args = parse_option()
    # Input bam file path (ex:/path/AAA0001.bam)
    input_bam_file_path = args.input
    # Result output directory (ex:/path/result/)
    output_dir_path = args.output
    
    # Process flag
    no_fastq_flag = args.no_fastq
    
    # Path of the fastq file resulting from the process. (ex:/path/result/AAA0001_export.fastq)
    output_fastq = output_dir_path + "/" + os.path.splitext(os.path.basename(input_bam_file_path))[0] + "_export.fastq"
    # Path of the fastq file resulting from the process. (ex:/path/result/AAA0001_export_taginfo.txt)
    output_taginfo = output_dir_path + "/" + os.path.splitext(os.path.basename(input_bam_file_path))[0] + "_export_taginfo.txt"
    
    # Read the bam file once to determine the tag type.(MM/ML or Mm/Ml)
    with pysam.AlignmentFile(input_bam_file_path, 'rb', check_sq = False) as bamfile:
        for read in bamfile.fetch(until_eof = True):
            if read.has_tag("Mm") and read.has_tag("Ml"):
                    mm_tags_key = 'Mm'
                    ml_tags_key = 'Ml'
                    break
            elif read.has_tag("MM") and read.has_tag("ML"):
                    mm_tags_key = 'MM'
                    ml_tags_key = 'ML'
                    break
            else:
                continue

    if no_fastq_flag == False:
        hout1 = open(output_fastq, 'w')
    
    with pysam.AlignmentFile(input_bam_file_path, 'rb', check_sq = False) as bamfile, open(output_taginfo, 'w') as hout2:
        # Output information to determine the type of tag when merging tags into bam.
        print("query_name\t" + mm_tags_key + "\t" + ml_tags_key, file = hout2)
        for read in bamfile.fetch(until_eof = True):
            # Check read sequence base qualities, including soft clipped bases
            if no_fastq_flag == False:
                if read.query_qualities is not None:
                    quality_info = ''.join([chr(x + 33) for x in read.query_qualities])
                    print(f'@{read.query_name}\n{read.query_sequence}\n+\n{quality_info}', file = hout1)

            # Extract tag information only for reads where tag exists
            try:
                MM_info = read.get_tag(mm_tags_key)
                ML_info = ','.join([str(x) for x in read.get_tag(ml_tags_key).tolist()])
                print(f'{read.query_name}\t{MM_info}\t{ML_info}', file = hout2)
            except KeyError:
                continue

    if no_fastq_flag == False:
        hout1.close()

def parse_option():
    parser = argparse.ArgumentParser(description='Export fastq file and mmml tag file from bam file.')
    parser.add_argument('-i', '--input', help="Enter the path of the bam file.")
    parser.add_argument('-o', '--output', help="Enter the path to output the resulting fastq file and tags info.")
    parser.add_argument('--no_fastq', action='store_true' , help="Don't output fastq file.")
    args = parser.parse_args()

    # Check bam file
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
