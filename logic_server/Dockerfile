# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Compilation Image
#
FROM python:3-alpine AS compile

# Install dependencies required to compile Python packages
RUN apk add --no-cache postgresql-dev libffi-dev musl-dev gcc build-base rust cargo

# Create Python virtualenv and use it
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Add requirements file
ADD requirements.txt .

# Install requirements (save space by not caching)
RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Runtime Image
#
# Note: Python base is unfortunately large, but required
FROM python:3-alpine 

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install required runtime dependencies
RUN apk add --no-cache postgresql-libs gettext supervisor

# Copy code into image
# TIP: use .dockerignore to exclude large items or secrets
COPY . /workspace
# Copy dependencies from virtualenv and use it
COPY --from=compile /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# ENV USER=docker
# ENV UID=1000
# ENV GID=$UID

# RUN addgroup -S $USER && adduser \
#     --disabled-password \
#     --gecos "" \
#     --home "$(pwd)" \
#     --ingroup "$USER" \
#     --no-create-home \
#     --uid "$UID" \
#     "$USER"

WORKDIR /workspace

RUN touch supervisord.log supervisord.pid

# RUN chown -R $USER:$USER public logs fixtures locale supervisord.log supervisord.pid .vscode*

# RUN chmod +x docker-entrypoint.sh

# Set the default user
# USER $USER

ENV SHELL /bin/sh

# CMD [ "./docker-entrypoint.sh" ]