from setuptools import setup

package_name = 'robot_vision'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ivan',
    maintainer_email='ivan@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "test_node = robot_vision.my_first_node:main",
            "pose_subscriber = robot_vision.pose_subscriber:main",
            "draw_circle = robot_vision.draw_circle:main",
            "vision_node = robot_vision.vision:main",
            "vision_subscriber = robot_vision.vision_subscriber:main",
        ],
    },
)
