# Fahis - Anti-Phishing Tool

![Fahis Logo](https://via.placeholder.com/400x200?text=Fahis+Logo) <!-- Placeholder for a future logo -->

## Overview

**Fahis** is a powerful and effective Anti-Phishing tool designed to help users identify suspicious and malicious links. The tool provides two interfaces: an attractive and interactive Graphical User Interface (GUI) for ease of use, and a Command Line Interface (CLI) for advanced users and automation. Fahis aims to protect users from phishing attacks by analyzing links and providing a comprehensive assessment of their risks.

## Key Features

*   **Comprehensive Link Analysis:** The tool analyzes links based on several criteria to determine their safety.
*   **Homoglyph Detection:** Identifies links that use visually similar characters to deceive users (e.g., `google.com` vs. `googIe.com`).
*   **Typosquatting Detection:** Detects links that exploit common misspellings of well-known domains (e.g., `facebok.com` instead of `facebook.com`).
*   **Suspicious Keyword Check:** Searches for common phishing keywords within the link.
*   **HTTPS Usage Check:** Verifies if the link uses the secure HTTPS protocol.
*   **IP Address Usage Check:** Alerts if the link uses an IP address instead of a domain name.
*   **Graphical User Interface (GUI):** An easy-to-use and visually appealing interface for interactive link analysis.
*   **Command Line Interface (CLI):** A flexible option for users who prefer to interact with the tool via the command line, supporting an interactive mode.

## Methodology

Fahis relies on a set of techniques and algorithms to analyze links and assess their risks:

1.  **Feature Extraction:** A set of features is extracted from each link, such as URL length, presence of HTTPS, use of IP addresses, number of subdomains, and presence of special characters.
2.  **Known Databases:** The tool uses pre-defined lists of safe domains (e.g., `google.com`) and known phishing domains (e.g., `googIe.com` which uses homoglyphs).
3.  **Homoglyph Analysis:** A dictionary of visually similar characters (homoglyphs) is used to compare domain characters with suspicious characters in other languages (e.g., Cyrillic or Greek) to detect deception attempts.
4.  **Typosquatting Analysis:** The similarity between the input domain and known safe domains is calculated using a simplified similarity algorithm (e.g., Jaccard similarity). If the similarity is high, a potential typosquatting is reported.
5.  **Risk Scoring:** Risk points are assigned to each suspicious feature. For example, the absence of HTTPS increases risk points, as does the presence of homoglyphs or suspicious keywords. These points are aggregated to determine the overall risk level (low, medium, high) and provide recommendations.

## Installation

To get started with Fahis, follow these steps:

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/kush-king249/Fahis.git
    cd Fahis
    ```

2.  **Install Dependencies:**
    The tool requires Python 3.x and some libraries. You can install them using `pip`:
    ```bash
    pip install -r requirements.txt
    ```
    **Note:** If you plan to use the Graphical User Interface (GUI) on Linux, you might need to install `python3-tk`:
    ```bash
    sudo apt-get update
    sudo apt-get install python3-tk
    ```

## Usage

You can run Fahis with two different interfaces:

### 1. Graphical User Interface (GUI)

To run the GUI, execute the main file without any arguments or with `--gui`:

```bash
python3 fahis.py
# or
python3 fahis.py --gui
```

A simple graphical window will appear where you can enter the link and click the button to analyze it.
