#!/usr/bin/env python

import re
import yaml
import sys
import subprocess
import os
import argparse
import logging

YAML_CONFIG_FILE = '/Users/nsonti/.gcal_automator_config.yaml'


def logging_init():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)


def init():
    init_data = \
'''Type 1:
- Task 1: "11am to 12 pm"
- Task 2: "3pm to 4pm"
- Task 3: "8pm to 9pm"
Type 2:
- Task 1: "11am to 12 pm"
- Task 2: "3pm to 4pm"
- Task 3: "8pm to 9pm"'''


    fh = open(YAML_CONFIG_FILE, 'w+')
    fh.write(init_data)
    fh.close()
    logging.info('config file initialzed at ' + YAML_CONFIG_FILE)

def execute_cmd(cmd):
    print 'Executing command: ', cmd
    os.system(cmd)


def parse(file_name):
    fh = open(file_name,'Ur')
    yaml_data = yaml.load(fh)
    fh.close()
    return yaml_data


def choose_type(yaml_data):
    print 'Choose one of the following types:'

    i = 1
    tmp_dict = dict()
    for type in yaml_data:
        print str(i) + ") " + str(type)
        tmp_dict[i] = str(type)
        i += 1

    opt = int(raw_input())
    if opt <= i:
        chosen_type = tmp_dict[opt]
        return chosen_type
    else:
        print 'Invalid option'
        sys.exit(1)


def create_calendar(task_data):
    # gcalcli quick 'study today from 7pm to 8pm' --calendar="nikhil"
    print task_data
    for task in task_data:
        for data in task:
            cmd = 'gcalcli quick --calendar="nikhil" \'' + str(data) + ' today from ' + str(task[data]) + '\''

            execute_cmd(cmd)

def main():
    logging_init()

    # argument parser
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-i", "--init", help="creates a sample yaml configuration file", action="store_true")
    arg_parser.add_argument("-r", "--run", help="execute gcal_automator", action="store_true")
    arg_parser.add_argument("-a", "--agenda", help="print agenda", action="store_true")
    arg_parser.add_argument("-w", "--week", help="print week calendar", action="store_true")
    arg_parser.add_argument("-m", "--month", help="print month calendar", action="store_true")
    args = arg_parser.parse_args()

    if args.init:
        init()
    elif args.run:
        yaml_data = parse(YAML_CONFIG_FILE)
        chosen_type = choose_type(yaml_data)
        create_calendar(yaml_data[chosen_type])
    elif args.agenda:
        cmd = "gcalcli agenda"
        execute_cmd(cmd)
    elif args.week:
        cmd = "gcalcli calw"
        execute_cmd(cmd)
    elif args.month:
        cmd = "gcalcli calm"
        execute_cmd(cmd)
    else:
        arg_parser.print_help()

if __name__ == '__main__':
    main()

