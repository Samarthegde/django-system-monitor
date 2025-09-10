# Mini System Monitor

## System Status in Django Admin

This application provides a real-time system monitor integrated into the Django Admin interface, accessible only to superusers. It has been recently updated with several improvements, including a more modern UI, configurable refresh intervals, and a cleaner codebase.

## Features

*   **Real-time System Metrics:** Displays CPU, Memory, Swap, and Root Disk usage.
*   **Static System Information:** Shows hostname, OS details, boot time, CPU information, total memory, total root disk space, Python version, and Django version.
*   **Modern UI:** Utilizes Chart.js for interactive and visually appealing charts.
*   **Configurable Refresh Interval:** Easily adjust the data refresh rate via Django settings.
*   **Clean Codebase:** Refactored logic into utility functions for better organization and maintainability.
*   **Unit Tests:** Comprehensive unit tests for core utility functions.

## Installation

1.  **Install `django-mini-system-monitor` with pip:**
    ```shell
    pip install git+https://github.com/Samarthegde/django-system-monitor.git

    ```
    *(Note: Ensure `Django` and `psutil` are installed. The `requirements.txt` now pins specific versions for consistency.)*

2.  **Add "system_monitor" to your `INSTALLED_APPS` setting:**
    In your Django project's `settings.py` file:
    ```python
    INSTALLED_APPS = [
        # ...
        'system_monitor',
    ]
    ```

3.  **Configure Refresh Interval (Optional):**
    You can customize the refresh interval for the system monitor in your `settings.py`. The value is in milliseconds.
    ```python
    SYSTEM_MONITOR_REFRESH_INTERVAL = 10000 # Refresh every 10 seconds (default is 5000ms)
    ```

4.  **Run migrations:**
    ```shell
    python manage.py migrate
    ```


5.  **Start the development server and visit the Admin:**
    ```shell
    python manage.py runserver
    ```
    Then, navigate to `http://127.0.0.1:8000/admin/` (you'll need the Admin app enabled and a superuser account). You will find the "System Monitor" section in the admin interface.

## Development

### Running Tests

To run the unit tests for the `system_monitor` app:
```shell
python manage.py test system_monitor
```

## Screenshots

*(Note: Old screenshots are no longer relevant due to UI changes. New screenshots would need to be generated.)*

## Authors

*   **Dann Luciano** - *Initial work* - [@dannluciano](https://twitter.com/dannluciano)
*   **[Samarth Hegde]** - *Improvements and Refactoring*


## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details
