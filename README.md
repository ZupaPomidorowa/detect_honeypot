# GSoC 2024: Improving the functionality of Honeyscanner

Mentors: Aristofanis Chionis, Emmanouil Vasilomanolakis

Organization: The Honeynet Project 

## About this project
This repository has been created as part of the Google Summer of Code in the "Honeyscanner - A vulnerability analyzer for Honeypots" project.
The goal of my project is to automatically detect honeypot and it's version. This repository contains tests and link to PR.

## Project goals

Enhance the scanner's functionality to automatically detect honeypots, eliminating the need for users to specify honeypot types or versions manually. Users should only need to provide the host IP address as an argument.

## What have been done

Initially, a series of tests were conducted to identify each honeypot. This started with Nmap scans, followed by manual verification. I have checked for each honeypot: open ports, services running on those ports, and the possibility of connecting to them. Methods for identifying specific honeypots:

**Cowrie**

* check port 2222 for default banner
* connect to port via SSH with default username and password
* check default configuration: os version, meminfo file, mounts file, cpu, hostname, user phil in group, shadow, passwd

**Kippo**

* check port 2222 for default banner

**Dionaea**

* check open ports
* check port 21 for default banner
* check port 443 for Dionaea ssl cert
* check port 445 for SMB server

**Conpot**
* check open ports

Next, I have developed script to identify each honeypot. This script was integrated into the main project by adding a new functionality.

## Current state
Users can simply provide the host IP address. The system will then scan the host for open ports, detect any honeypots, and identify their versions. As a result scanner provides the name of the detected honeypot and its latest version.


## Further improvments
Enhance the version detection process so that the system identifies the specific version of the honeypot running on the host, rather than just the latest version available.

[Link to forked repository](https://github.com/ZupaPomidorowa/detect_honeypot)

[Link to pull request](https://github.com/honeynet/honeyscanner/pull/38)
