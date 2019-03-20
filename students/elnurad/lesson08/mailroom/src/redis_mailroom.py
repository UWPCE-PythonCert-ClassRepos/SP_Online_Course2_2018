
import login_database
import utilities
  
      
def populate():
    """
        uses non-presistent Redis only (as a cache)

    """

    log = utilities.configure_logger('default', '../logs/redis_script.log')

    try:
        log.info('Step 1: connect to Redis')
        r = login_database.login_redis_cloud()
        log.info('Step 2: cache some data in Redis')
        r.hmset('Bill Gates', {'tel': '235-343-8934', 'e-mail': 'gates@gates.com', 'net_worth': '20 billion', 'age': '55'})
        r.hmset('Jeff Bezos', {'tel': '566-895-8522', 'e-mail': 'bezos@bezos.com', 'net_worth': '80 Billion', 'age': '60'})
        r.hmset('Hannah Smith', {'tel': '345-434-5444','e-mail': 'smith@smith.com', 'net_worth': '50 Billion', 'age': '50'})
        r.hmset('John Clarke', {'tel': '456-343-3898', 'e-mail': 'clark@clark.com', 'net_worth': '45 Million', 'age': '45'})
        r.hmset('Andrew Jones', {'tel': '234-439-8432', 'e-mail': 'jones@jones.com', 'net_worth': '33 Million', 'age': '45'})
        
     
        while True:
            name = input('Enter a donor name to look up ')
            info = int(input("'to look up telephone number of this donor: type 1', 'e-mail: type 2', 'net-worth: type 3'," 
                             " 'age: type 4', 'to quit: type 5' "))
            if r.exists(name):
                if info == 1:
                    donor_tel = r.hmget(name, 'tel')
                    print(donor_tel)
                elif info == 2:
                    donor_email = r.hmget(name, 'e-mail')
                    print(donor_email)
                elif info == 3:
                    donor_net = r.hmget(name, 'net_worth')
                    print(donor_net)
                elif info == 4:
                    donor_age = r.hmget(name, 'age')
                    print(donor_age)
                elif info == 5:
                    exit()
            else:
                print('Donor does not exist, please choose another donor')



    except Exception as e:
        print(f'Redis error: {e}')
   


if __name__ == '__main__':
    populate()
