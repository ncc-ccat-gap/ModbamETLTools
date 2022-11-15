Modbam ETL tools
==================

# Intoroduction
This script can output the fastq file and mm/ml tag information separately from the bam file. After mapping the output fastq file with any mapper, the process of merging mm/ml tag information is executed.

# Installation
## Install G-CAT ID Manager
```sh
python setup.py install
```

## Requirement
* pysam
* Python 3.8

# Usage
## 1.Export fastq and MM/ML tag info from bam
```
export_tag -b [input_bam_file] -f [output_fastq_file] -t [output_mm/ml_tag_file]
```

## 2.Merge MM/ML tag info into the bam file
```
merge_tag -i [input_bam_file] -t [input_mm/ml_tag_file] -o [output_merge_bam_file]
```
