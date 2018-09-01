#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import re
from argparse import ArgumentParser
from aztarna.sros import SROSScanner
from aztarna.ros import ROSScanner


def main():
    logger = logging.getLogger(__name__)
    parser = ArgumentParser(description='Aztarna')
    parser.add_argument('-t', '--type', help='<ROS/SROS> Scan ROS or SROS hosts', required=True)
    parser.add_argument('-a', '--address', help='Single address or network range to scan.')
    parser.add_argument('-p', '--ports', help='Ports to scan (format: 13311 or 11111-11155 or 1,2,3,4)', required=True)
    parser.add_argument('-i', '--input_file', help='Input file of addresses to use for scanning')
    parser.add_argument('-o', '--out_file', help='Output file for the results')
    parser.add_argument('-e', '--extended', help='Extended scan of the hosts', action='store_true')
    args = parser.parse_args()
    try:
        if args.type == 'ROS' or args.type == 'ros':
            scanner = ROSScanner()
        elif args.type == 'SROS' or args.type == 'sros':
            scanner = SROSScanner()
        else:
            logger.critical('Invalid type selected')
            return

        if args.input_file:
            scanner.load_from_file(args.input_file)
        else:
            if args.address:
                scanner.net_range = args.address
            else:
                logger.critical('No file or addresses defined')
                return

        try:
            scanner.ports = range(int(args.ports.split('-')[0]), int(args.ports.split('-')[1]))
        except:
            try:
                scanner.ports = [int(port) for port in args.ports.split(',')]
            except:
                try:
                    scanner.ports.append(int(args.ports))
                except Exception as e:
                    print('[-] Error: ' + str(e))

        scanner.extended = args.extended
        scanner.scan()

        if args.out_file:
            scanner.write_to_file(args.out_file)
        else:
            scanner.print_results()
    except Exception as e:
        logger.critical('Exception occurred during execution')
        raise e


if __name__ == '__main__':
    main()