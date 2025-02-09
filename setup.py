from setuptools import setup, find_packages
import os

# Set the default settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expense_tracker.settings')

setup(
    name='expense_tracker',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django>=4.0',
        'pandas',
        'openpyxl',
    ],
    entry_points={
        'console_scripts': [
            'expense_tracker=django.core.management:execute_from_command_line',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
