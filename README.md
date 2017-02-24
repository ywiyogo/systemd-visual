# Systemd Visualization

A Python script for visualizing the dependencies of systemd unit files in a running Linux machine.

## Requirements

* Python 2.7
* d3plus.v1.9.8

## Usage

Generate dot file from a running linux system by:

    systemd-analyze dot > <filename>

Run the Python script on your local computer:

    python visualizeDot_d3plus.py <generated_dot_file> > <html_output_file>

##Screenshot

![alt text](./screenshot.png "systemd visualization")
