import setuptools

if __name__ == "__main__":
  setuptools.setup(
    name = 'etl_tools',
    version = '0.2',
    author = 'Yuto Ohira',
    license = 'GPLv3',

    package_dir = {'': 'scripts'},
    packages = setuptools.find_packages("scripts"),
    entry_points = {
      'console_scripts': [
        'export_tag = etl_tools.export_fastq_and_tag_info:main',
        'merge_tag = etl_tools.merge_tags_info_to_bam:main',
        'split_bam = etl_tools.export_split_bam_with_hp_tags:main'

      ],
    },
    install_requires = [
      'pysam',
    ],
  )
