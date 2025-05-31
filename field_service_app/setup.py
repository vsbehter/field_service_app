from setuptools import setup, find_packages

setup(
    name='field_service_app',
    version='0.0.1',
    description="Field service workflow for appliance repair",
    author="Vladimir",
    author_email="vladimir@yourcompany.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'frappe>=14.0.0'
    ],
    zip_safe=False
)