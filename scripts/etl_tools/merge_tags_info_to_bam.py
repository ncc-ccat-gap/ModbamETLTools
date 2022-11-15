#!/usr/bin/env python

import array
import pysam
import logging
import argparse

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def main():
    args = parse_option()
    input_bam = args.input
    output_bam = args.output
    mm_info = args.tag
    
    rid2mm = {}
    rid2ml = {}
    with open(mm_info, 'r') as hin:
        for line in hin:
            F = line.rstrip('\n').split('\t')
            rid2mm[F[0]] = F[1]
            rid2ml[F[0]] = F[2]

    source_bamfile = pysam.AlignmentFile(input_bam, 'rb')
    dest_bamfile = pysam.AlignmentFile(output_bam, 'wb', template = source_bamfile)

    for read in source_bamfile.fetch(until_eof = True):
        # Whether query_name exists in the key of dic (if not, skip it because it is not methylated)
        if read.query_name not in rid2mm or read.query_name not in rid2ml:
            dest_bamfile.write(read)
            continue

        mm_info = rid2mm[read.query_name]
        ml_info = rid2ml[read.query_name]

        # debug
        #import pdb; pdb.set_trace()

        # MMset
        if len(mm_info) != 0:
            read.set_tag('MM', mm_info)
        else:
            read.set_tag('MM', '')

        # MLset
        if len(ml_info) != 0:
            read.set_tag('ML', array.array('B', [int(x) for x in ml_info.split(',')]))
        else:
            read.set_tag('ML', array.array('B'))

        dest_bamfile.write(read)

    source_bamfile.close()
    dest_bamfile.close()

def parse_option():
    parser = argparse.ArgumentParser(description='Export fastq file and mmml tag file from bam file.')
    parser.add_argument('-i', '--input', help="Input bam file path.")
    parser.add_argument('-o', '--output', help="Output bam file path.")
    parser.add_argument('-t', '--tag', help="input mmml_tag file path.")
    args = parser.parse_args()
    
    if (args.input is None) and (args.output is None) and (args.tag is None):
        logger.error("[ERROR] Please input import bam path or export bam/tag file")
        exit(1)
        
    return args

if __name__ == '__main__':
    main() 