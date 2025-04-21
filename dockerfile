FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies for SQLite
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wget \
    build-essential \
    libsqlite3-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Download and install SQLite 3.47.2
RUN wget https://www.sqlite.org/2024/sqlite-autoconf-3470200.tar.gz && \
    tar xzf sqlite-autoconf-3470200.tar.gz && \
    cd sqlite-autoconf-3470200 && \
    ./configure --prefix=/usr && \
    make && \
    make install && \
    cd .. && \
    rm -rf sqlite-autoconf-3470200 sqlite-autoconf-3470200.tar.gz

# Set the working directory
WORKDIR /app

# Copy requirements to container
COPY ./requirements /app/requirements

# Upgrade pip and install requirements
RUN pip install --upgrade pip && \
    pip install --default-timeout=1000 --no-cache-dir -r requirements/dev.txt
# Copies local `docs` directory into the container's `/app/docs`

COPY ./core/docs /app/docs  

# -----------------------------------------------
# Add the Sphinx build command
# -----------------------------------------------
CMD ["sphinx-build", "-b", "html", "docs/source", "docs/build"]
