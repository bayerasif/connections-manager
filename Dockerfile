FROM python:3-alpine
COPY app /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 7080
CMD ["python", "app.py"]
