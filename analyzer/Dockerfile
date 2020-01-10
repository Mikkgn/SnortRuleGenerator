FROM python:3.8.0-slim-buster as stage0

COPY analyzer/requirements /opt/analyzer/requrements

RUN groupadd --system snort_rule_generator && useradd --system -g snort_rule_generator analyzer

RUN set -ex ; \
    savedAptMark="$(apt-mark showmanual) libpq5 libpq-dev tshark" ; \
    apt-get update ; \
    apt-get install -y --no-install-recommends \
	    gcc \
		libc6-dev \
		tshark \
		libpq-dev \
		libssl-dev ; \
    pip3 install --no-cache-dir -r /opt/analyzer/requrements ; \
    apt-mark auto '.*' > /dev/null \
	\
	# reset apt-mark's "manual" list so that "purge --auto-remove" will remove all build dependencies
    # (which is done after we install the built packages so we don't have to redownload any overlapping dependencies)
	; \
    [ -z "$savedAptMark" ] || apt-mark manual $savedAptMark ; \
    apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false ; \
    rm -rf /var/lib/apt/lists/*

WORKDIR /opt

# ------------------- tests ------------------
#
#FROM stage0 as test_stage
#
#RUN pip3 install mypy==0.730 sqlalchemy-stubs==0.1
#
#COPY analyzer/ /opt/analyzer/
#COPY mypy.ini /opt/mypy.ini
#
#RUN mypy --config-file mypy.ini analyzer/

# -------------------- final -----------------------

FROM stage0 as final_stage

COPY analyzer /opt/analyzer
COPY common /opt/common

USER root

CMD ["python", "-m", "analyzer"]
