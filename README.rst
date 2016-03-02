=================
Metrics collector
=================


Overview
========

You'd better use some already available project like https://github.com/python-diamond/Diamond
or https://github.com/google/grr/. This project is implemented only as a demo and to test
coroutines in Python 3.4

Python version requirement
==========================

Python version >=3.4.4 is required (for ``asyncio.ensure_future``).

Intended usage
==============

Collector should collect "batches" of metrics and later push them to some external API for actual
storage and visualization

Implemented behaviour
=====================

Collector saves everything to local database and does not use any external API.
It's possible to generate html page that visualizes collected data.

All this is for demo purposes only: storage is slow and unoptimized.

Usage
=====

After installing (e.g. with ``pip install ./async-metrics-collector``) you can:

* Start collector daemon::
       
       mcollector --daemonize --interval=5
       
* Generate plaintext metrics data (usable as input for
  `Graphite <http://graphite.readthedocs.org/en/latest/feeding-carbon.html#the-plaintext-protocol>`_)::
       
       mcollector --graphite-data
       
* Dump already stored metrics data in Graphite plaintext format::
       
       mcollector --dump
       
