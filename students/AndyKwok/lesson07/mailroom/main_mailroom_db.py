import mailroom_gen_db as prog
import list_mailroom_db as tool

adddonor = [
    ('Harry', 'ID_1'),
    ('Andy', 'ID_2'),
    ('Kristen', 'ID_3'),
    ('P Four', 'ID_4')
    ]

donations = [
        (10, 1, 'ID_1'), 
        (112.00, 2, 'ID_3'),
        (2.4, 3, 'ID_2'),
        (2.30, 4, 'ID_1'),
        (0, 5, 'ID_4')
        ]
        
option = True
if __name__ == '__main__':
    prog.add_donor(adddonor)
    prog.add_donation(donations)
    while option is True:
        try:
            print(
                """
                Menu
                =============================
                1 - Report out
                2 - Add Donor
                3 - Add Donation
                4 - Edit Donation
                5 - Delete Donor
                6 - Delete donation
                7 - Quit
                """
            )
            tool.read_db()
            option = input('Please select an option> ')
            if option == '1':
                tool.read_db()
                option = True
            elif option == '2':
                name = input('Name of new donor> ')
                id = 'ID_' + input('ID Number> ')
                adddonor = [(name, id)]
                prog.add_donor(adddonor)
                print('Donor info added...')
                option = True
            elif option == '3':
                num_entry = tool.donation_count() + 1
                amount = float(input('Amount of donation> $ '))
                id = 'ID_' + input('ID of the donor> ')
                donations = [(amount, num_entry, id)]
                print(donations)
                prog.add_donation(donations)
                print('Donation info added...')
                option = True
            elif option == '4':
                id = int(input('Donation entry to edit> '))
                new_amount = input('New donation amount> $ ')
                prog.edit_donation(id, new_amount)
                print('Donation entry updated...')
                option = True
            elif option == '5':
                id = 'ID_' + input('ID of the donor> ')
                prog.delete_donor(id)
                option = True
            elif option == '6':
                entry = int(input('Donation entry to delete> '))
                prog.delete_donation(entry)
                print('Entry deleted')
                option = True
            elif option == '7':
                option = False
        except KeyError:
            print('Option does not exist...please try again')
        tool.read_db()
