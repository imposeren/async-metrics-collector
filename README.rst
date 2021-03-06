=================
Metrics collector
=================


Overview
========

You'd better use some already available and mature project like http://www.zabbix.com/, http://www.cacti.net/, http://argus.tcp4me.com/, https://github.com/python-diamond/Diamond
or https://github.com/google/grr/ or even ELK (Kibana + Logstash + ElasticSearch).

This project is implemented only as a demo and to test coroutines in Python 3.4

Python version requirement
==========================

Python version >=3.4.4 is required (for ``asyncio.ensure_future``).

Intended usage
==============

Collector should collect "batches" of metrics like CPU usage, memory usage and disk utilization,
and later push them to some external API for actual storage and visualization

Implemented behaviour
=====================

Collector uses `psutil <https://pypi.python.org/pypi/psutil>`_ to get come system stats and saves
everything to local database and does not use any external API.

All code is for demo purposes only: storage (`tinydb <https://pypi.python.org/pypi/tinydb>`_) is slow and unoptimized.

Usage
=====

After installing (e.g. with ``pip install ./async-metrics-collector``) you can:

* Start collector daemon (using `python-daemon <https://pypi.python.org/pypi/python-daemon/>`_ 
  that implements `PEP 3143 <https://www.python.org/dev/peps/pep-3143/>`_ without
  specifying any configuration options)::
       
       mcollector --daemonize --interval=5
       
* Generate plaintext metrics data (usable as input for
  `Graphite <http://graphite.readthedocs.org/en/latest/feeding-carbon.html#the-plaintext-protocol>`_)::
       
       mcollector --graphite-data
       
* Dump already stored metrics data in Graphite plaintext format::
       
       mcollector --dump
       
