FROM ubuntu:24.04

RUN apt update
RUN apt install python3-bs4 python3-tqdm python3-numpy python3-regex python3-urllib3 python3-glob2 -y
RUN apt install python3 python3-pip gdal-bin python3-gdal -y

WORKDIR /tmp/

COPY tac.py /tmp/
COPY *.geojson /tmp/
RUN ls /tmp/

CMD ["python3", "tac.py"]
