FROM python:3.8-slim-buster

# Tạo thư mục và chuyển mã nguồn vào
RUN mkdir /app
COPY . /app
WORKDIR /app

# Cài đặt các gói yêu cầu từ requirements_dev.txt
RUN pip install -r requirements_dev.txt 

# Cài đặt các gói cần thiết
RUN apt update -y && apt install -y --no-install-recommends \
    libpq-dev \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Cài đặt phiên bản cụ thể của pendulum trước khi cài đặt Airflow
RUN pip install pendulum==2.1.2

# Cài đặt Flask-Session trước khi cài đặt Airflow
RUN pip install Flask-Session

# Cài đặt Airflow
RUN pip install apache-airflow

# Thiết lập các biến môi trường
ENV AIRFLOW_HOME="/app/airflow"
ENV AIRFLOW__CORE__DAGBAG_IMPORT_TIMEOUT=1000
ENV AIRFLOW__CORE__ENABLE_XCOM_PICKLING=True

# Khởi tạo cơ sở dữ liệu Airflow
RUN airflow db migrate  && sleep 5

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

# Đặt lệnh ENTRYPOINT
ENTRYPOINT [ "/bin/sh" ]
CMD [ "start.sh" ]
