#!/usr/bin/env python3

import sys
from io import StringIO
import unittest
import pytest
from unittest import mock
from mock import patch
import mailroom_db as mailroom
import os
import logging
from peewee import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
myDB = mailroom.DonorDB(SqliteDatabase('donor_list.db'))

def test_select_action_dictionary_exit(capsys):
    test_input = ['1']
    with mock.patch('builtins.input', side_effect=test_input):
        mailroom.select_action_dictionary('1', mailroom.switch_func_dict)
        captured = capsys.readouterr()
        out = captured.out.strip()
        assert out == "Before quitting."

def test_select_action_dictionary_lower_bound_invalid(capsys):
    test_input = ['0', '1']
    with mock.patch('builtins.input', side_effect=test_input):
        mailroom.select_action_dictionary('0', mailroom.switch_func_dict)
        captured = capsys.readouterr()
        out = captured.out.strip()
        assert out == ("Please enter only one of the listed options.\n" + "Before quitting.")


def test_select_action_dictionary_upper_bound_invalid(capsys):
    test_input = ['11', '1']
    with mock.patch('builtins.input', side_effect=test_input):
        mailroom.select_action_dictionary('1', mailroom.switch_func_dict)
        captured = capsys.readouterr()
        out = captured.out.strip()
        assert out.startswith("Please enter only one of the listed options.")


def test_sending_thank_you(capsys):
    test_input = ['4', 'Toni Orlando', 100, '1']
    with mock.patch('builtins.input', side_effect=test_input):
        mailroom.select_action_dictionary('1', mailroom.switch_func_dict)
        captured = capsys.readouterr()
        out = captured.out.strip()
        err = captured.err.strip()
        assert ('Dear {}, Thank you for your generous contribution of ${'
                ':.2f} to our program.'.format(test_input[1],test_input[2])) in out


def test_add_new_donor(capsys):
    test_input = ['5', "Bruno Mars", "Seattle", '1']
    with mock.patch('builtins.input', side_effect=test_input):
        mailroom.select_action_dictionary('1', mailroom.switch_func_dict)
        captured = capsys.readouterr()
        out = captured.out.strip('\n')
        err = captured.err.strip()
        assert(test_input[1] + " was succesfully added") in out

def test_delete_donor(capsys):
    test_input = ['7', "Bruno Mars", '1']
    with mock.patch('builtins.input', side_effect=test_input):
        mailroom.select_action_dictionary('1', mailroom.switch_func_dict)
        captured = capsys.readouterr()
        out = captured.out.strip('\n')
        err = captured.err.strip()
        assert(test_input[1] + " was succesfully deleted") in out


def test_add_donation(capsys):
    test_input = ['6', "Toni Orlando", '500', '1']
    with mock.patch('builtins.input', side_effect=test_input):
        mailroom.select_action_dictionary('1', mailroom.switch_func_dict)
        captured = capsys.readouterr()
        out = captured.out.strip('\n')
        err = captured.err.strip()
        assert(" was succesfully added") in out


def test_calculate_report(capsys):
    test_input = ['2', '1']
    with mock.patch('builtins.input', side_effect=test_input):
        mailroom.select_action_dictionary('1', mailroom.switch_func_dict)
        captured = capsys.readouterr()
        out = captured.out.strip('\n')
        err = captured.err.strip()
        assert "Robin Hood" in out

def test_donor_list(capsys):
    test_input = ['10', '1']
    with mock.patch('builtins.input', side_effect=test_input):
        mailroom.select_action_dictionary('1', mailroom.switch_func_dict)
        captured = capsys.readouterr()
        out = captured.out.strip('\n')
        err = captured.err.strip()
        file_list = ['Amanda Clark', 'Toni Orlando', 'Robin Hood',
                 'Gina Travis', 'Mark Johnson']
        for name in file_list:
            assert name in out


def test_send_everyone_letters_directly(capsys):
    myDB.send_everyone_letters()
    captured = capsys.readouterr()
    out = captured.out.strip('\n')
    err = captured.err.strip()
    file_name_extension = ".txt"
    current_directory = os.getcwd()
    file_list = ['Amanda Clark', 'Toni Orlando', 'Robin Hood',
                 'Gina Travis', 'Mark Johnson']
    for f_name in file_list:
        target_file_path = os.path.join(current_directory,
                                        str(f_name).replace(' ', '_') + mailroom.calculate_date() + file_name_extension)
        assert out == 'Done'
        assert os.path.exists(target_file_path)
