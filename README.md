# IP Data Collector

This Python script collects detailed information about an IP address using BrowserLeaks and optionally saves the results as JSON and an interactive map.

## Features

- Fetches browser and network-related data for a given IP.

- Cleans irrelevant or empty values automatically.

- Displays information in the console.

## Optionally saves:

JSON file with all collected data.

HTML map showing IP location using Folium.

## Requirements

Python 3.10+

## Packages:

`pip install requests beautifulsoup4 folium`

## Notes

- Some IP addresses may not have geographic coordinates available.

- Trash or placeholder values (e.g., "n/a (no js)", "*/*") are automatically ignored.

- The script works with publicly accessible IP data on BrowserLeaks; a working internet connection is required.
