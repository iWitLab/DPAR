FROM ubuntu
RUN apt update && apt install -y python3 pip nano sudo
WORKDIR /pesrank_streamlit
ADD ./requirements.txt /pesrank_streamlit/requirements.txt
WORKDIR /pesrank_streamlit
RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt
ADD . /pesrank_streamlit
CMD streamlit run /pesrank_streamlit/main.py
#CMD ["./keylogger2.sh"]
