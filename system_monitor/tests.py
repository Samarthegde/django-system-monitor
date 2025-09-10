from django.test import TestCase
from unittest.mock import patch, MagicMock
from .utils import get_all_settings, get_all_envs, get_overview, get_static_overview
from django.conf import settings
import os

class UtilsTestCase(TestCase):


    @patch('psutil.virtual_memory')
    @patch('psutil.swap_memory')
    @patch('psutil.disk_usage')
    @patch('psutil.cpu_percent', return_value=10.5)
    def test_get_overview(self, mock_cpu_percent, mock_disk_usage, mock_swap_memory, mock_virtual_memory):
        mock_virtual_memory.return_value = MagicMock(percent=50.0)
        mock_swap_memory.return_value = MagicMock(percent=25.0)
        mock_disk_usage.return_value = MagicMock(percent=75.0)

        result = get_overview()
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0]['name'], 'cpu_percent')
        self.assertEqual(result[0]['value'], 10.5)
        self.assertEqual(result[1]['name'], 'memory_percent')
        self.assertEqual(result[1]['value'], 50.0)
        self.assertEqual(result[2]['name'], 'swap_percent')
        self.assertEqual(result[2]['value'], 25.0)
        self.assertEqual(result[3]['name'], 'root_disk_percent')
        self.assertEqual(result[3]['value'], 75.0)

    @patch('platform.node', return_value='test-hostname')
    @patch('platform.uname')
    @patch('psutil.boot_time', return_value=1678886400) # March 15, 2023 00:00:00 UTC
    @patch('psutil.cpu_freq')
    @patch('psutil.cpu_count', return_value=4)
    @patch('psutil.virtual_memory')
    @patch('psutil.disk_usage')
    @patch('platform.python_version', return_value='3.9.5')
    @patch('django.get_version', return_value='4.2')
    def test_get_static_overview(self, mock_django_version, mock_python_version, mock_disk_usage,
                                 mock_virtual_memory, mock_cpu_count, mock_cpu_freq,
                                 mock_boot_time, mock_uname, mock_node):
        mock_uname.return_value = MagicMock(
            system='Linux', release='5.15.0', machine='x86_64', processor='x86_64'
        )
        mock_cpu_freq.return_value = MagicMock(max=2500)
        mock_virtual_memory.return_value = MagicMock(total=16 * 1024**3) # 16 GB
        mock_disk_usage.return_value = MagicMock(total=500 * 1024**3) # 500 GB

        result = get_static_overview()
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 8)
        self.assertEqual(result[0]['name'], 'hostname')
        self.assertEqual(result[0]['value'], 'test-hostname')
        self.assertEqual(result[1]['name'], 'OS Uname')
        self.assertEqual(result[1]['value'], 'Linux - 5.15.0  - x86_64 - x86_64')
        self.assertEqual(result[2]['name'], 'boot_time')
        self.assertEqual(result[2]['value'], '2023-03-15 05:30:00') # UTC+5.5:00
        self.assertEqual(result[3]['name'], 'cpu')
        self.assertEqual(result[3]['value'], '2500 hz x 4 cores')
        self.assertEqual(result[4]['name'], 'Memory Total')
        self.assertEqual(result[4]['value'], '16.0\xa0GB')
        self.assertEqual(result[5]['name'], 'Root Disk Total')
        self.assertEqual(result[5]['value'], '500.0\xa0GB')
        self.assertEqual(result[6]['name'], 'Python Version')
        self.assertEqual(result[6]['value'], '3.9.5')
        self.assertEqual(result[7]['name'], 'Django Version')
        self.assertEqual(result[7]['value'], '4.2')

    @patch('psutil.cpu_freq', side_effect=AttributeError)
    @patch('psutil.cpu_count', return_value=4)
    @patch('platform.uname')
    @patch('psutil.boot_time', return_value=1678886400)
    @patch('psutil.virtual_memory')
    @patch('psutil.disk_usage')
    @patch('platform.python_version', return_value='3.9.5')
    @patch('django.get_version', return_value='4.2')
    def test_get_static_overview_cpu_freq_exception(self, mock_django_version, mock_python_version, mock_disk_usage,
                                                    mock_virtual_memory, mock_cpu_count, mock_cpu_freq,
                                                    mock_boot_time, mock_uname):
        mock_uname.return_value = MagicMock(
            system='Linux', release='5.15.0', machine='x86_64', processor='x86_64'
        )
        mock_virtual_memory.return_value = MagicMock(total=16 * 1024**3)
        mock_disk_usage.return_value = MagicMock(total=500 * 1024**3)

        result = get_static_overview()
        self.assertEqual(result[3]['name'], 'cpu')
        self.assertEqual(result[3]['value'], '0 hz x 4 cores')
