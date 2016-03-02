# -*- coding: utf-8 -*-
from mcollector.collectors import PsutilCollector
from mcollector.storages import TinyDBStorage
from mcollector.renderers import NVD3Rendered
import argparse
import asyncio
import contextlib
import daemon


def run(args):
    # with daemon.DaemonContext():
    metric_interval = args.metric_interval

    storage = TinyDBStorage(args.storage_path)
    collector = PsutilCollector(verbosity=args.verbosity, print_graphite_data=args.graphite_data, storage=storage)

    if args.dump:
        for data in storage.all_sorted():
            print('{metric_path} {result} {timestamp}'.format(**data))
    elif args.visualize:
        print(NVD3Rendered().render(storage.all_sorted()))
    else:
        if args.clear_storage:
            storage.clear()

        partition_paths = list(collector.get_partition_paths())

        tasks = [
            asyncio.ensure_future(collector.collect_metric_usage('cpu_percent', metric_interval)),
            asyncio.ensure_future(collector.collect_metric_usage('memory_percent', metric_interval)),
        ]
        for path in partition_paths:
            tasks.append(collector.collect_metric_usage('disk_bytes', metric_interval, path))

        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(asyncio.wait(tasks))
        finally:
            loop.close()


@contextlib.contextmanager
def dummy_context_manager():
    yield


def main():
    parser = argparse.ArgumentParser(description='Run metric collector.')
    parser.add_argument(
        '--daemonize',
        dest='daemonize',
        action='store_const',
        const=True,
        default=False,
        help='daemonize (default: run in foreground)'
    )
    parser.add_argument(
        '--graphite-data',
        dest='graphite_data',
        action='store_const',
        const=True,
        default=False,
        help='output data compatible with Graphite plaintext format (default: No)'
    )
    parser.add_argument(
        '--interval',
        dest='metric_interval',
        default=5,
        type=int,
        help='interval in seconds for metrics collecting (default: 5)'
    )

    parser.add_argument(
        '--verbosity',
        dest='verbosity',
        default=2,
        type=int,
        help='verbosity level (default: 2)'
    )

    parser.add_argument(
        '--clear-storage',
        dest='clear_storage',
        action='store_const',
        const=True,
        default=False,
        help='clear tinydb storage'
    )

    parser.add_argument(
        '--storage-path',
        dest='storage_path',
        type=str,
        default='./mcollector.tinydb',
        help='path for tinydb'
    )

    parser.add_argument(
        '--dump',
        dest='dump',
        action='store_const',
        const=True,
        default=False,
        help='dump stored data in Graphite compatible format and exit'
    )

    parser.add_argument(
        '--visualize',
        dest='visualize',
        action='store_const',
        const=True,
        default=False,
        help='store html file with data visualization'
    )

    args = parser.parse_args()

    if args.daemonize:
        context_manager = daemon.DaemonContext
    else:
        context_manager = dummy_context_manager

    with context_manager():
        run(args)


if __name__ == '__main__':
    main()
