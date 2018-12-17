import io
import pytest

from mailroom_json import *

def test_show_list(capsys):
    c = DonorCollection()
    c.show_list()
    captured = capsys.readouterr()
    expected = '\nJosh Hoff\nTatsiana Kisel\n'
    assert captured.out == expected
    
def test_add_new_donor():
    c = DonorCollection()
    c.add_donor('Andrew', 300)
    assert 'Andrew' in c._donors.keys()
    assert c._donors['Andrew'] == [300]
    
def test_show_list_after_adding_donor(capsys):
    c = DonorCollection()
    c.add_donor('Andrew', 300)
    c.show_list()
    captured = capsys.readouterr()
    expected = '\nJosh Hoff\nTatsiana Kisel\nAndrew\n'
    assert captured.out == expected
    
def test_add_donation_to_existing_donor():
    c = DonorCollection()
    c.add_donor('Josh Hoff', 250)
    assert 'Josh Hoff' in c._donors.keys()
#NOTE: 25 and 75 are existing values for Josh Hoff
    assert c._donors['Josh Hoff'] == [25, 75, 250]
    
def test_report(capsys):
    c = DonorCollection()
    c.report()
    expected = '\nDonor Name             | Total Given | Num Gifts | Average Gift\n\
---------------------------------------------------------------\n\
Tatsiana Kisel          $      140.55           2       70.28\n\
Josh Hoff               $      100.00           2       50.00\n'
    captured = capsys.readouterr()
    print(captured.out)
    assert captured.out == expected

    
def test_create_report_after_adding_donor(capsys):
    c = DonorCollection()    
    c.add_donor('Andrew', 300)
    c.add_donor('Josh Hoff', 250)
    c.report()
    expected = '\nDonor Name             | Total Given | Num Gifts | Average Gift\n\
---------------------------------------------------------------\n\
Josh Hoff               $      350.00           3      116.67\n\
Andrew                  $      300.00           1      300.00\n\
Tatsiana Kisel          $      140.55           2       70.28\n'
    captured = capsys.readouterr()
    print(captured.out)
    assert captured.out == expected
    
def test_letters_to_everyone_files():
    c = DonorCollection()
    c.letters()
    tab = '    '
    for i, val in c._donors.items():
        with open(f'{i}.txt', 'r') as outfile:
            donation = sum(val)
            check_text = f'Dear {i}, \n\n{tab}Thank you very much for your most recent donation \
of ${val[-1]:.2f}! \n\n{tab}You have now donated a total of ${donation:.2f}. \n\n{tab}Your support \
is essential to our success and will be well utilized. \n\n{tab*2}Sincerely, \n{tab*3}-The Company'
            expected = outfile.read()
            assert check_text == expected
                
def test_donor_average():
    d = DonorCollection()
    c = Donor('Josh Hoff', d.donors['Josh Hoff'])
    d.add_donor('Andrew', 300)
    d.add_donor('Josh Hoff', 250)
    assert c.average == 116.67
    
def test_donor_number_of_gifts():
    d = DonorCollection()
    c = Donor('Tatsiana Kisel', d.donors['Tatsiana Kisel'])
    assert c.gifts == 2

def test_donor_total_donations():
    d = DonorCollection()
    c = Donor('Josh Hoff', d.donors['Josh Hoff'])
    d.add_donor('Josh Hoff', 250)
    assert c.total_donations == 350
    
def test_most_recent_gift():
    d = DonorCollection()
    c = Donor('Josh Hoff', d.donors['Josh Hoff'])
    d.add_donor('Josh Hoff', 400)
    assert c.recent_gift == 400
    
def test_first_gift():
    d = DonorCollection()
    c = Donor('Josh Hoff', d.donors['Josh Hoff'])
    assert c.first_gift == 25
    
def test_multiply_method():
    c = Functions()
    assert c.challenge(3) == {'Josh Hoff': [75, 225], 'Tatsiana Kisel': [105, 316.65]}

def test_min_max_multiply_method():
    c = Functions()
    assert c.challenge(1) == {'Josh Hoff': [25, 75], 'Tatsiana Kisel': [35, 105.55]}
    assert c.challenge(10) == {'Josh Hoff': [250, 750], 'Tatsiana Kisel': [350, 1055.5]}
    assert c.challenge(3, 50) == {'Josh Hoff': [225, 25], 'Tatsiana Kisel': [316.65, 35]}
    assert c.challenge(3, 50, 200) == {'Josh Hoff': [225, 25], 'Tatsiana Kisel': [316.65, 35]}

def test_projections(capsys):
    c = Functions()
    c.projections()
    captured = capsys.readouterr()
    expected = '-------------------------------------------\n\
Current donations:\n\
Josh Hoff: $100\n\
Tatsiana Kisel: $140.55\n\
\n\
If you double contributions under $100:\n\
Josh Hoff: $200\n\
Tatsiana Kisel: $175.55\n\
\n\
If you triple contributions over $50:\n\
Josh Hoff: $250\n\
Tatsiana Kisel: $351.65\n\
-------------------------------------------\n'
    assert captured.out == expected
    
def test_saving():
    d = DonorCollection()
    d.add_donor('Andrew', 500)
    d.save()
    with open(f'save.txt', 'r') as outfile:
        assert outfile.read() == '{"__obj_type": "MyClass", "x": {"Josh Hoff": [25, 75], \
"Tatsiana Kisel": [35, 105.55], "Andrew": [500]}}'

def test_loading():
    d = DonorCollection()
    d.add_donor('Andrew', 300)
    d.save()
    d.add_donor('Accident', 40000)
    assert d.donors == {'Josh Hoff': [25, 75], 'Tatsiana Kisel': [35, 105.55], 'Andrew': [300], 'Accident': [40000]}
    d.load()
    assert d._donors == {'Josh Hoff': [25, 75], 'Tatsiana Kisel': [35, 105.55], 'Andrew': [300]}
