from setuptools import setup

setup(
    name='snake_gym_grid',
    version='0.0.5',
    description="An implementation on Snake game with grid display",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=['gym==0.25.0', 'pygame==2.1.2', 'numpy>=1.12.0']
)