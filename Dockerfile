FROM python:3.8-slim-buster
USER root

# Tạo thư mục và chuyển mã nguồn vào
RUN mkdir /app
COPY . /app
WORKDIR /app


RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    python3-dev \
    libffi-dev \
    libssl-dev \
    && apt-get clean


# Cài đặt các gói yêu cầu từ requirements.txt
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && \
    pip install -r /app/requirements.txt 



# Thiết lập các biến môi trường
ENV AIRFLOW_HOME="/app/airflow"
ENV AIRFLOW__CORE__DAGBAG_IMPORT_TIMEOUT=1000
ENV AIRFLOW__CORE__ENABLE_XCOM_PICKLING=True
ENV AIRFLOW__CORE__DAGS_FOLDER="/app/airflow/dags"
ENV PYTHONPATH="/app:/app/src"




# Khởi tạo cơ sở dữ liệu Airflow
RUN airflow db init && sleep 5

# Tạo người dùng Airflow
RUN airflow users create \
    --username admin \
    --password gaucho0123456 \
    --firstname anh \
    --lastname tanh \
    --role Admin \
    --email anhtt454598@gmail.com

# Đảm bảo rằng tệp khởi động có quyền thực thi
RUN chmod 777 start.sh
RUN apt update -y
# Đặt lệnh ENTRYPOINT và CMD
ENTRYPOINT [ "/bin/sh" ]
CMD [ "start.sh" ]