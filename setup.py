from setuptools import setup, find_packages
 
setup(
    name='django-ajax-feedback',
    version=__import__('feedback').__version__,
    description='Basic Django Feedback',
    author='Lauris Jullien',
    author_email='lauris@startup-from-scratch.com',
    url='http://github.com/laucia/django-ajax-feedback/',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    include_package_data=True,
    zip_safe=False,
)