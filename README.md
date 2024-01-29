[![Build and Release](https://github.com/pastorhudson/ProPresenter-PCO-Live-Auto-Control/actions/workflows/main.yml/badge.svg)](https://github.com/pastorhudson/ProPresenter-PCO-Live-Auto-Control/actions/workflows/main.yml)
# Clean Cloudflare
### What is this?
This is a script to delete videos from cloudflare streaming that are one year old or older.

[//]: # (### Demo Video)

[//]: # (Add video here)


### Download
- #### The latest download is always [here](https://github.com/pastorhudson/clean_cloudflare/releases/latest)
- #### You can see the changelog [here](https://github.com/pastorhudson/clean_cloudflare/blob/main/CHANGELOG.md)


A config.ini is provided in the src/utils.py

```editorconfig
[app]
;your cloudflare account email
email = you@email.com
;your cloudflare api key
api_key = 123
;your cloudflare account id found on right side of stream page
account_id = 123
;A list of whitelisted video ids that will be skipped and not deleted
whitelist = ['123', '456']
```

## Command-Line Options

This utility provides several options for interacting with the PCO Live service. You can use these options to perform various operations like testing the utility, specifying a service type ID, or a plan ID.

### Usage

```bash
clean_cloudflare [options]
```

### Options

- `-t`, `--test`  
  **Description:** Enables the test mode.  
  **Behavior:** Returns the string 'SUCCESS' and exits.  
  **Example:** `python main.py --test`

### DEV Setup

- Add versions to CHANGELOG.md like this:
```editorconfig
# Changelog
All notable changes to this project will be documented in this file.

## v1.0.0
### Changes
 - First Release
```

TO add a release put:
Release: vX.X.X in the commit message



Edit the workflow to change the executable name