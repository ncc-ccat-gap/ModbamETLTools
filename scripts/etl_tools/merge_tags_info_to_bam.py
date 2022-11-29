#!/usr/bin/env python

import os
import array
import pysam
import logging
import argparse

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def main():
    args = parse_option()
    # Input bam file path (ex:/path/AAA0001.bam)
    input_bam_file_path = args.input
    # Input tag file path (ex:/path/AAA0001.info)
    input_tag_info_file_path = args.tag
    # Result output directory (ex:/path/result/)
    output_dir_path = args.output
    # threads
    use_threads = args.threads
    
    # Get input bam file name (ex:AAA0001)
    input_bam_file_name = os.path.splitext(os.path.basename(input_bam_file_path))[0]
    # Path of the bam file resulting from the process[unsort]. (ex:/path/result/AAA0001_merge_tags.bam)
    output_bam_file_path = output_dir_path + "/" + input_bam_file_name + "_merge_tags.bam"
    # Path of the bam file resulting from the process[sort]. (ex:/path/result/AAA0001_merge_tags.bam)
    sorted_bam_file_path = output_dir_path + "/" + input_bam_file_name + "_merge_tags_sorted.bam"
    
    # Process flag
    no_sort_flag = args.no_sort
    
    # Tags dic Format
    rid2mm = {}
    rid2ml = {}
    
    # Tag key format(default)
    mm_tags_key = "MM"
    ml_tags_key = "ML"
    
    # Reading tag file.
    with open(input_tag_info_file_path, 'r') as hin:
        for line in hin:
            F = line.rstrip('\n').split('\t')
            # Stores header information
            if F[0] == "query_name":
                mm_tags_key = F[1]
                ml_tags_key = F[2]
            else:
                rid2mm[F[0]] = F[1]
                rid2ml[F[0]] = F[2]

    source_bamfile = pysam.AlignmentFile(input_bam_file_path, 'rb')
    dest_bamfile = pysam.AlignmentFile(output_bam_file_path, 'wb', template = source_bamfile)

    for read in source_bamfile.fetch(until_eof = True):
        # Whether query_name exists in the key of dic (if not, skip it because it is not methylated)
        if read.query_name not in rid2mm or read.query_name not in rid2ml:
            dest_bamfile.write(read)
            continue

        mm_info = rid2mm[read.query_name]
        ml_info = rid2ml[read.query_name]

        # MMtag key and value set
        if len(mm_info) != 0:
            read.set_tag(mm_tags_key, mm_info)
        else:
            read.set_tag(mm_tags_key, '')

        # MLtag key and value set
        if len(ml_info) != 0:
            read.set_tag(ml_tags_key, array.array('B', [int(x) for x in ml_info.split(',')]))
        else:
            read.set_tag(ml_tags_key, array.array('B'))

        dest_bamfile.write(read)

    source_bamfile.close()
    dest_bamfile.close()
    
    if no_sort_flag == False:
        pysam.sort("-@", use_threads ,"-o", sorted_bam_file_path, output_bam_file_path)
        # create index file(=[samtools index sorted_bam_file_path])
        pysam.index(sorted_bam_file_path)
    else:
        # create index file(=[samtools index sorted_bam_file_path])
        pysam.index(output_bam_file_path)


def parse_option():
    parser = argparse.ArgumentParser(description='Export bam file merging mmml tags.')
    parser.add_argument('-i', '--input', help="Enter the path of the bam file.")
    parser.add_argument('-t', '--tag', help="Enter the path of the mm/ml tags info file.")
    parser.add_argument('-o', '--output', help="Enter the path to output directory.")
    parser.add_argument('--no_sort', action='store_true' , help="Don't perform sorting of bam files after tagging.")
    parser.add_argument('--threads', default='8', help="Enter the number of CPU cores to be used.")
    args = parser.parse_args()
    
    if (args.input is None) or (args.tag is None):
        logger.error("[ERROR] Please input import bam path and merging tag file.")
        exit(1)
    
    if not os.path.exists(args.input):
        logger.error("[ERROR] Bam file does not exist.")
        exit(1)
        
    if not os.path.exists(args.tag):
        logger.error("[ERROR] Tag file does not exist.")
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

