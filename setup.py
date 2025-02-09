from setuptools import setup, find_packages

setup(
    name='expense_tracker',
    version='1.0.0',
    packages=find_packages(include=['expense_tracker', 'expense_tracker.*', 'apps.*']),  # ✅ Include the apps namespace
    include_package_data=True,
    package_data={
        'apps.accounts': ['templates/accounts/*.html'],     # ✅ Use the full namespace
        'apps.expenses': ['templates/expenses/*.html'],
        '': ['templates/*.html'],
    },
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
    zip_safe=False,
)
