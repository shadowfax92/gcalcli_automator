import re
import yaml
import sys
import subprocess
import os

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
    if len(sys.argv) >1:
        yaml_config = sys.argv[1]
    else:
        print 'specify yaml config file as parameter'
        sys.exit(1)

    yaml_data = parse(yaml_config)
    chosen_type = choose_type(yaml_data)
    create_calendar(yaml_data[chosen_type])

if __name__ == '__main__':
    main()

