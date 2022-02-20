#!/usr/bin/env python3
import argparse
import os
import re
import shutil
import sys
import time

version = "0.2.1"


# Flags
verbose_output = None
output_immediately = None
trial_move = None

# Globals
stdout = ""
failed_move_count = 0


def clear_globals_for_unittests():
    global stdout
    stdout = ""


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
    if verbose_output:
        return output(out)
    return


def output(out):
    global stdout
    if output_immediately:
        unicode_output(out)
    else:
        stdout += out + "\n"


def unicode_output(out):
    # when printing directly to the windows console stdout, unicode errors tend to be ignored automatically
    # if the user redirects stdout to a file, unicode errors can occur
    # this code outputs the best it can and flags errors in the output
    try:
        print(out, flush=True)
    except UnicodeEncodeError:
        try:
            print(out.encode("utf8").decode(sys.stdout.encoding))
        except UnicodeDecodeError:
            print(out.encode("utf8").decode(sys.stdout.encoding, errors="ignore") + " <-- UnicodeDecodeError")


def fcon(path):
    output("\n" + time.strftime("%X : ") + "Consolidating files in subfolders of " + path + "\n")
    start_time = time.time()

    file_count = 0
    folder_count = 0

    # files in root path do not need to be moved to where they already are
    processed_root = False
    for root, folders, files in os.walk(path):
        if processed_root == False:
            processed_root = True
            continue

        files.sort()

        for basename in files:
            file_count += 1
            current_file_path = os.path.join(root, basename)
            verbose("Processing file " + current_file_path)
            consolidate_file(root, basename, path, folder_count)
        folder_count += 1

    output(
        "\n"
        + time.strftime("%X : ")
        + str(file_count)
        + " files moved, in "
        + str(round(time.time() - start_time, 3))
        + " seconds"
    )

    if failed_move_count:
        output("\n" + "failed to move " + str(failed_move_count))

    return stdout


def consolidate_file(root, source_basename, destination_path, folder_count):
    prefix = (str(folder_count) + "-").zfill(4)
    destination_file_path = determine_unique_destination_file_path(source_basename, destination_path, prefix)

    source_file_path = os.path.join(root, source_basename)
    if not trial_move:
        shutil.move(source_file_path, destination_file_path)

    rename_message = ""
    destination_basename = os.path.basename(destination_file_path)
    if source_basename != destination_basename:
        rename_message = " --> " + destination_basename

    output("... moved " + source_basename + rename_message)


def determine_unique_destination_file_path(source_basename, destination_folder, prefix):
    destination_file_basename, destination_file_extension = os.path.splitext(source_basename)
    while True:
        destination_file_path = os.path.join(
            destination_folder, prefix + destination_file_basename + destination_file_extension
        )
        if not os.path.isfile(destination_file_path):
            return destination_file_path
        count_found = re.search(r"-([0-9]+)$", destination_file_basename)
        if count_found:
            count = int(count_found.group(1)) + 1
            basename_without_count = re.search(r"^(.*)-[0-9]+$", destination_file_basename)
            destination_file_basename = basename_without_count.group(1) + "-" + str(count)
        else:
            destination_file_basename += "-1"


parser = argparse.ArgumentParser(description="Consolidate files in sub folders at path directly into folder at path")
parser.add_argument("--path", dest="path", required=False, action="store", help="Target path")
parser.add_argument("--version", action="version", version=version)
parser.add_argument(
    "--verbose", action="store_true", dest="verbose", default=False, help="Will output extra info on logic"
)
parser.add_argument(
    "--delayed",
    action="store_true",
    dest="output_delayed",
    default=False,
    help="Will display stdout at end instead of immediately",
)
parser.add_argument(
    "--trial",
    action="store_true",
    dest="trial_move",
    default=False,
    help="Displays files to move without actually moving them",
)

args = parser.parse_args()
set_verbose_output(args.verbose)
set_output_immediately(not args.output_delayed)
set_trial_move(args.trial_move)

if args.path:
    fcon(args.path)
    if not output_immediately:
        print("\nConsolidating...")
        unicode_output(stdout)
    sys.exit()
