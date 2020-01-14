FROM python:3.7
COPY scripts/* /bin/
COPY requirements.txt /tmp/
EXPOSE 8888

RUN usermod -u 1000 www-data
RUN usermod -G staff www-data

RUN pip install -r /tmp/requirements.txt
RUN jupyter contrib nbextension install --system
RUN jt -t onedork -fs 95 -altp -tfs 11 -nfs 115 -cellw 88% -T
RUN jupyter contrib nbextension install --system
RUN jupyter nbextension enable --system codefolding/main
RUN jupyter nbextension enable --system scroll_down/main
RUN jupyter nbextension enable --system collapsible_headings/main
RUN jupyter nbextension enable --system execute_time/ExecuteTime
RUN jupyter nbextension enable --system init_cell/main

WORKDIR /code

CMD /bin/bash
