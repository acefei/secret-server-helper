from setuptools import setup

setup(
    name='secret_server_helper',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    packages=['secret_server_helper'],
    install_requires=['requests'],
    entry_points={
        'console_scripts': ['secret-server-helper=secret_server_helper.__main__:main']
    }
)
