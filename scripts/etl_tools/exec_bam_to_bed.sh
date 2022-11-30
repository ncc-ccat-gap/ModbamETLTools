#!/bin/bash
set -o errexit
set -o nounset
set -o pipefail

input_bam=${1}
fasta_file=${2}
threads=${3}

file_name=`echo ${input_bam} | sed 's/\.[^\.]*$//'`
output_bed="${file_name}.bed"

/tools/modbam2bed/modbam2bed \
  --aggregate \
  --cpg \
  -e \
  -t ${threads} \
  ${fasta_file} \
  ${input_bam} > ${output_bed}

if [ $? -eq 0 ]; then
    mv ./mod-counts.cpg.acc.bed ./${file_name}_mod-counts.cpg.acc.bed
fi