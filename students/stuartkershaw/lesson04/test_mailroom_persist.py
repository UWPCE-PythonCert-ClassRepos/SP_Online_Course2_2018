from os import listdir
from os.path import isfile, join

from mailroom import DonorList, DonorCli


def test_donor_list_persist(tmpdir, capsys):
    dl = DonorList()
    dl.add_donor("Stuart")
    dl.add_donor("Cayce")

    stuart = dl.get_donor("Stuart")
    cayce = dl.get_donor("Cayce")

    stuart.add_donation(25)
    stuart.add_donation(50)

    cayce.add_donation(100)
    cayce.add_donation(50)

    dc = DonorCli(dl)

    p = tmpdir.mkdir('sub')
    with p.as_cwd():
        dc.save_donations()
        captured = capsys.readouterr()
        assert captured.out == 'Successfully saved donors to JSON file.\n'

        tempFiles = [f for f in listdir(p) if isfile(join(p, f))]
        assert tempFiles == ['donorList.json']

        dc.load_donations()
        captured = capsys.readouterr()
        assert captured.out == 'Successfully loaded donors from JSON file.\n'

        stuart = dl.get_donor("Stuart")
        cayce = dl.get_donor("Cayce")

        assert stuart.donations == [25, 50]
        assert cayce.donations == [100, 50]
