from setuptools import setup, find_packages

setup(
    name='expense_tracker',
    version='1.0.0',
    # packages=find_packages(include=['expense_tracker', 'expense_tracker.*', 'apps', 'apps.*']),  # ✅ Include the apps namespace
    packages=find_packages(include=[
        "expense_tracker",
        "apps",
        "apps.accounts",
        "apps.expenses",
    ]),
    include_package_data=True,
    package_data={
        "expense_tracker": ["templates/*"],
        # 'apps.accounts': ['templates/accounts/*.html'],     # ✅ Use the full namespace
        # 'apps.expenses': ['templates/expenses/*.html'],
        # '': ['templates/*.html'],
    },
    install_requires=[
        'Django>=4.0',
        'pandas',
        'openpyxl',
    ],
    entry_points={
        'console_scripts': [
            # 'expense_tracker=django.core.management:execute_from_command_line',
            # 'expense_tracker=expense_tracker.main:main',
            "expense_tracker = expense_tracker.cli:main",
        ],
    },
    zip_safe=False,
)
