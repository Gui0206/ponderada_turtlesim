from setuptools import find_packages, setup

package_name = 'turtle_draw_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Guilherme Hollanda',
    maintainer_email='guilherme.marques@sou.inteli.edu.br',
    description='Turtle drawing from image contours',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'turtle_drawer = turtle_draw_pkg.turtle_drawer:main',
            'image_processor = turtle_draw_pkg.image_processor:main',
        ],
    },
)
