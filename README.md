# GSoC 2024: Improving the functionality of Honeyscanner

Mentors: Aristofanis Chionis, Emmanouil Vasilomanolakis

Organization: The Honeynet Project 

## About this project

This repository has been  developed as part of the  Google Summer of Code initiative, under the "Honeyscanner - A Vulnerability Analyzer for Honeypots" project. The primary objective of this project is to create an automated system capable of detecting honeypots and accurately identifying their versions.

Honeypots, which are decoy systems designed to attract and monitor malicious activities, play a crucial role in cybersecurity. Detecting and analyzing these honeypots, including determining their versions, is essential for understanding their vulnerabilities and enhancing defensive measures.

This repository contains tests to detect each honeypot, script which detects supported honeypots by Honeyscanner (Cowrie, Kippo, Dionaea, Conpot) and a link to the pull request (PR) documenting the project's contributions.


## Project goals

Enhance the scanner's functionality to automatically detect honeypots without requiring users to manually specify the types or versions. Users should only need to provide the host IP address as an argument. This improvement will simplify the process, making it easier and more efficient for users to identify honeypots accurately.

## What have been done

Initially, a series of tests were conducted to identify each honeypot. This started with Nmap scans for each honeypot to detect running services on open ports, followed by manual verification. I have checked for each honeypot: open ports, services running on those ports, and the possibility of connecting to them. Methods for identifying specific honeypots:

**Cowrie**

* check port 2222 for default banner 'SSH-2.0-OpenSSH_6.0p1 Debian-4+deb7u2'
* connect to port via SSH with default username  (root) and password (1234)
* check default configuration:
* * os version: Linux version 3.2.0-4-amd64 (debian-kernel@lists.debian.org),
  * /proc/meminfo file for static memory information,
  * /proc/mounts file for static information,
  * /proc/cpu for static cpu information: model name\t: Intel(R) Core(TM)2 Duo CPU     E8200  @ 2.66GHz,
  * hostname: svr0,
  * if user phil exists in group, shadow, passwd files

**Kippo**

* check port 2222 for default banner 'SSH-2.0-OpenSSH_5.1p1 Debian-5'

**Dionaea**

* check if all dionea ports (21, 23, 42, 53, 80, 135, 443, 445, 1433, 1723, 1883, 3306, 5060, 9100, 11211, 27017) are open
* check port 21 for default banner: 220 DiskStation FTP server ready
* check if ssl cert on port contains: dionaea.carnivore.it1
* check port 445 for SMB server by sending specific bytes as used in nmap and expect in response text 'SMBr'

**Conpot**
* check if all conpots ports (2121, 5020, 10201, 44818) are open

Then, I have developed a script to identify different honeypots. This script has been integrated into the main project as a new functionality.

## Current state

Users can simply provide the host IP address as input. The system will then proceed to scan the host for open ports. Upon detecting a honeypot, the system will further analyze it to determine its specific type and newest version. The scanner will output the name of the detected honeypot and its corresponding version. Example response:

`This host is probably Conpot honeypot`
`Conpot version Release_0.6.0`

## Further improvments
Enhance the version detection process so that the system identifies the specific version of the honeypot running on the host, rather than just the latest version available.

## Challanges and valuable lessons

During my participation in the Google Summer of Code, I had the opportunity to learn and work with several new technologies and tools. I have learned Docker, which allowed me to containerize honeypots, ensuring consistency across different environments and simplifying the deployment process. I also gained a deep understanding of Nmap, a powerful network scanning tool, which I used to identify open ports and gather information about networked devices. This knowledge was crucial for detecting honeypots systems designed to attract and analyze potential cyber attackers. Additionally, I explored new Python libraries: argparse, socket, requests, ssl, paramiko, ftplib, http.client that enhanced the functionality of my project, enabling efficient data processing, network communication, and automation. These experiences not only expanded my technical skill set but also provided practical insights into network security and vulnerability analysis.

[Link to forked repository](https://github.com/ZupaPomidorowa/detect_honeypot)

[Link to pull request](https://github.com/honeynet/honeyscanner/pull/38)
