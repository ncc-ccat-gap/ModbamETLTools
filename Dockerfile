FROM python:3.8.6

RUN pip install --upgrade pip && \
    pip install pysam==0.20.0 && \
    pip install modbampy

RUN git clone -b v0.6.3 --recursive https://github.com/epi2me-labs/modbam2bed.git && \
    mkdir /tools/ && mv /modbam2bed /tools/modbam2bed && \
    cd /tools/modbam2bed && make 

RUN wget https://github.com/samtools/samtools/releases/download/1.16.1/samtools-1.16.1.tar.bz2 && \
    tar jxf samtools-1.16.1.tar.bz2 && rm samtools-1.16.1.tar.bz2 && \
    mv ./samtools-1.16.1 /tools/samtools && \
    cd /tools/samtools && /tools/samtools/configure && make && make install

RUN git clone https://github.com/ncc-ccat-gap/ModbamETLTools.git && \
    cd ModbamETLTools && \
    python setup.py install