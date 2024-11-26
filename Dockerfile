FROM python:3.12.5

WORKDIR /app

COPY . /app

RUN pip install --index-url=https://pypi.tuna.tsinghua.edu.cn/simple/ --no-cache-dir -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
