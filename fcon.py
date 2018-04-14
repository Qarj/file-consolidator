#!/usr/bin/env python3
version="0.1.0"

import sys, argparse, os, stat, time, shutil

# Flags
verbose_output = None
output_immediately = None
trial_move = None

# Globals
stdout = ''
failed_move_count = 0

def clear_globals_for_unittests():
    global stdout
    stdout = ''

def set_verbose_output(b):
    global verbose_output
    verbose_output = b

def set_output_immediately(b):
    global output_immediately
    output_immediately = b

def set_trial_move(b):
    global trial_move
    trial_move = b

def verbose(out):
    if (verbose_output):
        return output(out)
    return

def output(out):
    global stdout
    if (output_immediately):
        try:
            print(out, flush=True)
        except UnicodeEncodeError:
            try:
                print(out.encode('utf8').decode(sys.stdout.encoding))
            except UnicodeDecodeError:
                print('Sorry Unicode error...')
    else:
        stdout += out + "\n"

def fcon(path):
    output('\n' + time.strftime('%X : ') +  'Consolidating files in subfolders of ' + path + '\n')
    start_time = time.time()

    file_count = 0

    processed_root = False
    for root, dirs, files in os.walk(path):
        if (processed_root == False):
            processed_root = True
            continue
        files.sort()
        for file_name in files:
            file_count += 1
            current_file_path = os.path.join(root,file_name)
            verbose('Processing file ' + current_file_path)
            consolidate_file(root,file_name,path)

    output('\n' + time.strftime('%X : ') + str(file_count) + ' files moved, in ' + str(round(time.time()-start_time, 3)) + ' seconds')

    if (failed_move_count):
        output('\n' + 'failed to move ' + str(failed_move_count))

    return stdout

def consolidate_file(root,file_name,destination_path):
    destination_file_path = determine_unique_destination_file_path(root,file_name,destination_path)

    current_file_path = os.path.join(root,file_name)
    if (not trial_move):
        shutil.move(current_file_path, destination_file_path)

    rename_message = ''
    destination_basename = os.path.basename(destination_file_path)
    if (file_name != destination_basename):
        rename_message = ' --> ' + destination_basename
    
    output('... moved ' + file_name + rename_message)

def determine_unique_destination_file_path(root,file_name,destination_folder):
    destination_file_basename, destination_file_extension = os.path.splitext(file_name)
    while (True):
        destination_file_path = os.path.join(destination_folder,destination_file_basename+destination_file_extension)
        if (not os.path.isfile(destination_file_path)):
            return destination_file_path
        destination_file_basename += '-1'

parser = argparse.ArgumentParser(description='Consolidate files in sub folders at path directly into folder at path')
parser.add_argument('--path', dest='path', required=False, action='store', help='Target path')
parser.add_argument('--version', action='version', version=version)
parser.add_argument('--verbose', action='store_true', dest='verbose', default=False, help='Will output extra info on logic')
parser.add_argument('--delayed', action='store_true', dest='output_delayed', default=False, help='Will display stdout at end instead of immediately')
parser.add_argument('--trial', action='store_true', dest='trial_move', default=False, help='Displays files to move without actually moving them')

args = parser.parse_args()
set_verbose_output(args.verbose)
set_output_immediately(not args.output_delayed)
set_trial_move(args.trial_move)

if (args.path):
    fcon(args.path)
    if (not output_immediately):
        print('\nConsolidating...\n')
        try:
            print(stdout)
        except UnicodeEncodeError:
            print(stdout.encode('utf8').decode(sys.stdout.encoding))
    sys.exit()