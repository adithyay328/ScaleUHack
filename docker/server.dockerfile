# From base
FROM scaleu_base

# Pip install flask
RUN pip install flask

# Make workdir /
WORKDIR /

# Copy source and venv
COPY ./server.py /

# Run flask
CMD python3 server.py