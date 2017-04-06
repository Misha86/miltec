# -*- encoding: utf-8 -*-
"""This fabric module."""

from __future__ import unicode_literals

from fabric.api import local, env, cd, sudo


def run_tests_coverage():
    local('coverage run manage.py test')
    local('coverage html')
    local('firefox htmlcov/index.html')


def run_tests_pep8():
    local('pep8 --show-source --show-pep8 apps/ fortytwo_test_task/')


def run_tests_pylint():
    local('pylint --load-plugins pylint_django apps/ fortytwo_test_task/')


def run_tests_flake8():
    local('flake8 --exclude *migrations*,'
          'fortytwo_test_task/settings/__init__.py,'
          '*test_common.py --max-complexity=6 apps fortytwo_test_task')


def run_git_merge():
    local('git checkout master', 'git merge')
