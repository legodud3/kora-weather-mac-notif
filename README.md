# Local Weather Notifier

The Local Weather Notifier script is a tool for macOS that fetches real-time weather data for a specified location and provides desktop notifications for the current weather conditions.

## Description

Using the Weather Union API, this script pulls data including temperature, humidity, wind direction, wind speed, rain intensity, and total rain accumulation since midnight. It also calculates an estimated 'feels like' temperature.

## Features

- Fetches current weather data from Weather Union API
- Displays a notification with temperature, 'feels like' temperature, and rain intensity
- Runs as a scheduled job on macOS via cron

## Dependencies

- Python 3
- `requests` library for Python

## Installation

1. Clone this repository to your local machine:
    ```sh
    git clone https://github.com/legodud3/kora-weather-mac-notif.git
    ```

2. Navigate to the script directory:
    ```sh
    cd kora-weather-mac-notif
    ```

3. Install the required Python packages:
    ```sh
    pip3 install -r requirements.txt
    ```

## Configuration

1. Obtain an API Key from the Weather Union and add it to a `config.py` file in the same directory as the script.

    ```python
    # config.py
    API_KEY = "your_api_key_here"
    ```

2. Ensure the `config.py` file is not tracked by git for security reasons. Add it to `.gitignore`:
    ```
    # .gitignore
    config.py
    ```

3. Make the script executable:
    ```sh
    chmod +x fetch-weather.py
    ```

## Usage

Run the script manually to test the setup:
```sh
/Library/Frameworks/Python.framework/Versions/3.12/bin/python3 fetch-weather.py
