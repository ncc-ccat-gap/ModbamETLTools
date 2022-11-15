#!/usr/bin/env python

import pysam
import logging
import argparse

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def main():
    args = parse_option()
    input_bam = args.bam
    output_fastq = args.fastq
    output_taginfo = args.tag
    
    with pysam.AlignmentFile(input_bam, 'rb', check_sq = False) as bamfile, open(output_fastq, 'w') as hout1, open(output_taginfo, 'w') as hout2:
        for read in bamfile.fetch(until_eof = True):
                quality_info = ''.join([chr(x + 33) for x in read.query_qualities])
                print(f'@{read.query_name}\n{read.query_sequence}\n+\n{quality_info}', file = hout1)
                try:
                    MM_info = read.get_tag('MM')
                    ML_info = ','.join([str(x) for x in read.get_tag('ML').tolist()])
                    print(f'{read.query_name}\t{MM_info}\t{ML_info}', file = hout2)
                except KeyError:
                    continue

def parse_option():
    parser = argparse.ArgumentParser(description='Export fastq file and mmml tag file from bam file.')
    parser.add_argument('-b', '--bam', help="Input bam file path.")
    parser.add_argument('-f', '--fastq', help="Output fastq file name.")
    parser.add_argument('-t', '--tag', help="Output mmml_tag file name.")
    args = parser.parse_args()
    
    if (args.bam is None) and (args.fastq is None) and (args.tag is None):
        logger.error("[ERROR] Please input import bam path or export fastq/tag file")
        exit(1)
        
    return args

if __name__ == '__main__':
    main() 