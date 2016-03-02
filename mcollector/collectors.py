# -*- coding: utf-8 -*-
import asyncio
import os
import psutil
import time
import socket


HOSTNAME = socket.gethostname()


class BaseCollector(object):

    def __init__(self, verbosity=2, print_graphite_data=False, storage=None):
        self.verbosity = verbosity
        self.storage = storage
        self.print_graphite_data = print_graphite_data

    @asyncio.coroutine
    def collect_metric_usage(self, metric_name, metric_interval=5, *args, **kwargs):
        """Coroutine to collect some metric each `metric_interval` seconds."""
        method = getattr(self, 'get_{0}_usage'.format(metric_name))

        metric_path_parts = [HOSTNAME, metric_name] + list(args)
        for key in sorted(list(kwargs.keys())):
            metric_path_parts.append('{0}_{1}'.format(key, kwargs[key]))
        metric_path_parts = [path_part.replace('.', '_dot_').replace(' ', '_') for path_part in metric_path_parts]

        metric_path = '.'.join(metric_path_parts)
        while True:
            graphite_entries = []
            current_time = time.time()
            next_time = current_time + metric_interval
            result = method(*args, **kwargs)

            if isinstance(result, (list, tuple)):
                graphite_entries = [
                    {
                        'metric_path': '{0}.{1}'.format(metric_path, 'total'),
                        'result': result[0],
                        'timestamp': current_time,
                    },
                    {
                        'metric_path': '{0}.{1}'.format(metric_path, 'free'),
                        'result': result[1],
                        'timestamp': current_time,
                    }
                ]
            elif result:
                graphite_entries = [{
                    'metric_path': metric_path,
                    'result': result,
                    'timestamp': current_time,
                }]

            if self.print_graphite_data or self.storage:
                for graphite_entry in graphite_entries:
                    if self.storage:
                        self.storage.store(graphite_entry)
                    if self.print_graphite_data:
                        print('{metric_path} {result} {timestamp}'.format(**graphite_entry))

            wait_time = next_time - time.time()
            if wait_time <= 0:
                wait_time = 0.1
            yield from asyncio.sleep(wait_time)

    def get_cpu_percent_usage(self, interval=1, iterations=1):
        """Return average CPU usage.

        Run `iterations` number of tests each taking `interval` seconds.

        """
        aggregated = 0
        for i in range(0, iterations):
            aggregated += self.get_cpu_percent(interval=interval)
        return aggregated / iterations

    def get_memory_percent_usage(self, interval=1, iterations=1):
        """Return average memory usage percent.

        Run `iterations` number of tests with `interval` seconds pause between them.

        """
        aggregated = 0
        for i in range(0, iterations):
            aggregated += self.get_memory_percent()
            time.sleep(interval)
        return aggregated / iterations

    def get_disk_bytes_usage(self, partition_path):
        return (self.get_disk_total(partition_path), self.get_disk_free(partition_path))

    def get_cpu_percent(self, interval=1):
        raise NotImplementedError()

    def get_memory_percent(self):
        raise NotImplementedError()

    def get_partition_paths(self):
        raise NotImplementedError()

    def get_disk_total(self, partition_path):
        raise NotImplementedError()

    def get_disk_free(self, partition_path):
        raise NotImplementedError()


class PsutilCollector(BaseCollector):

    def get_cpu_percent(self, interval=1):
        return psutil.cpu_percent(interval=interval)

    def get_memory_percent(self):
        return psutil.virtual_memory().percent

    def get_partition_paths(self):
        for part in psutil.disk_partitions(all=False):
            if os.name == 'nt':
                if 'cdrom' in part.opts or part.fstype == '':
                    # skip cd-rom drives with no disk in it; they may raise
                    # ENOENT, pop-up a Windows GUI error for a non-ready
                    # partition or just hang.
                    continue
            if part.fstype in ('udf', 'iso9660'):
                continue
            if (part.opts == 'ro') or (',ro,' in part.opts) or part.opts.startswith('ro,') or part.opts.endswith(',ro'):
                continue
            yield part.mountpoint

    def get_disk_total(self, partition_path):
        return psutil.disk_usage(partition_path).total

    def get_disk_free(self, partition_path):
        return psutil.disk_usage(partition_path).free
