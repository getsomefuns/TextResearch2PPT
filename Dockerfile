FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    graphviz \
    nodejs \
    npm

WORKDIR /app
COPY . .

RUN npm install -g @mermaid-js/mermaid-cli && \
    pip install -r requirements.txt

CMD ["python", "main.py"]