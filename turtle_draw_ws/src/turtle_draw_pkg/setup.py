from setuptools import setup, find_packages

setup(
    name='turtle_draw_pkg',
    version='0.0.1',
    packages=find_packages(),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/turtle_draw_pkg']),
        ('share/turtle_draw_pkg', ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    author='Guilherme Hollanda',
    author_email='guilherme.marques@sou.inteli.edu.br',
    maintainer='Guilherme Hollanda',
    maintainer_email='guilherme.marques@sou.inteli.edu.br',
    url='https://github.com/guilhermeholanda/turtle_draw',
    description='Computer vision pipeline to draw image contours with ROS 2 turtlesim',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'turtle_drawer = turtle_draw_pkg.turtle_drawer:main',
            'vision_pipeline = turtle_draw_pkg.vision_pipeline:main',
        ],
    },
)
