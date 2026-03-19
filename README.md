<p align="center">
  <a href="https://specterops.io" target="_blank">
    <img alt="A project powered by SpecterOps - Creators of BloodHound" src=".github/GitHub-Header.png" width="100%" style="max-width: 100%;">
  </a>
</p>

<h4 align="center">
  A OpenHound template to create your own OpenGraph collector 
</h4>

<!-- Standard shields, please do not remove -->
<p align="center">
  <a href="https://slack.specterops.io"><img src="https://custom-icon-badges.demolab.com/badge/Slack-BloodHound%20Gang-4A154B?logo=slack&logoColor=fff" alt="Slack"/></a>
  <a href="https://reddit.com/r/SpecterOpsCommunity"><img src="https://img.shields.io/badge/Reddit-r/SpecterOpsCommunity-FF4500?logo=reddit&logoColor=white" alt="SpecterOps on Reddit"/></a>
  <a href="https://community.specterops.io"><img src="https://img.shields.io/badge/Discord-SpecterOps-%235865F2.svg?&logo=discord&logoColor=white" alt="SpecterOps on Discord"/></a>
  <a href="https://github.com/specterops"><img src="https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fspecterops%2F.github%2Fmain%2Fconfig%2Fshield.json&style=flat" alt="Sponsored by SpecterOps"/></a>
</p>


<p align="center">
  <a href="https://x.com/SpecterOps"><img src="https://img.shields.io/twitter/follow/SpecterOps?style=social" alt="@SpecterOps on Twitter"/></a>
  <a href="https://www.linkedin.com/company/specterops/"><img src="https://custom-icon-badges.demolab.com/badge/LinkedIn-0A66C2?logo=linkedin-white&logoColor=fff" alt="Connect on LinkedIn"/></a>
  <a href="https://infosec.exchange/@specterops"><img src="https://img.shields.io/mastodon/follow/109314317500800201?domain=https%3A%2F%2Finfosec.exchange&style=social" alt="Connect on Mastodon"/></a>
</p>

---

## About
OpenHound is a standardized framework for building OpenGraph collectors and converters. Built on [DLT](https://dlthub.com/docs/intro) (Data Load Tool) and [Typer](https://typer.tiangolo.com/), it provides a consistent workflow for collecting, processing, and converting data from any source into BloodHound-compatible graphs. This repository contains a cookiecutter template to get started building your own OpenGraph collector using OpenHound. 


## Getting started

OpenHound installs as a CLI tool and is typically executed inside a Python virtual environment. The steps below create an isolated environment and installs the package directly from GitHub.

Once installed, you can explore the available commands with `openhound --help`. The [CLI](cli.md) page covers all the available commands and collection and convert pipelines.

### 1. Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)

### 2. Install OpenHound

> **Note**: OpenHound is currently under active development. Installation requires Git-based installation until the package is officially published to PyPI.

```console
uv tool install "openhound @ git+https://github.com/SpecterOps/openhound.git"
```

### 3. Create a collector
To create a new collector, run the following command after installing openhound (it may take +- 20 seconds when openhound is started for the first time).

```console
openhound create collector <path_where_to_create_collector>
```

This will create a new collector based on this repository's cookiecutter template. The generated collector will include a sample collection and conversion pipeline, as well as a README to get you started.



