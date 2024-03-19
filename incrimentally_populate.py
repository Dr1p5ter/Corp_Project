import generator as gen
import random
import time as time
import signal as sig

from math import floor

from user_info_helpers import * # helpers from the user schema file

known_records_path = "records.tsv"  # path to file holding all stored populated records from previous runtimes
known_records = {}                  # dictionary that holds in all of the records

dpx = 5     # percentage of deletions
upx = 15    # percentage of updates
ipx = 80    # percentage of insertions

tfx = 4    # coeficient that dictates rate of population time gaps differ from [0, tfx)

# set up handler to safely end the program
loop_end = True
def SIGINT_handler(sig, frame) :
    global loop_end
    loop_end = False
sig.signal(sig.SIGINT, SIGINT_handler)

# load in previous records for populaton
try :
    with open(known_records_path, "r", buffering=True, ) as file:
        records = file.readlines()
        for entry in records :
            vals = entry.strip().split('\t')
            known_records[str(vals[0])] = {
                    "user_id" : vals[0],
                    "fname" : vals[1],
                    "minit" : vals[2],
                    "lname" : vals[3],    
                    "login_username" : vals[4],
                    "login_password" : vals[5]
                }
except FileNotFoundError :
    logger.info(colored("known_records_path doesn't exist within current directory, nothing added to known records\n", COL_CONTEXT))

# main loop for population
while loop_end :
    # determine the behavior of randomized percentages
    x = floor(random.random() * 100)
    if (x >= 0) and (x < dpx) : # delete
        print("delete")
        if len(known_records) != 0 :
            user_key = random.choice(list(known_records.keys()))
            res = delete_user_credentials(known_records[user_key]["user_id"],
                                          known_records[user_key]["login_username"],
                                          known_records[user_key]["login_password"])
            if res == None :
                known_records.pop(user_key)
    elif (x >= dpx) and (x < (dpx + upx)) : # update
        print("update")
        if len(known_records) != 0 :
            user_key = random.choice(list(known_records.keys()))
            new_username = random.choice([None,
                                          gen.gen_username(known_records[user_key]["fname"],
                                                           known_records[user_key]["lname"],
                                                           minit=known_records[user_key]["minit"],
                                                           random_int_included=True)])
            new_password = random.choice([None, gen.gen_password()])
            res = update_user_credentials(known_records[user_key]["login_username"],
                                          new_username=new_username,
                                          new_password=new_password)
            if res == None :
                if known_records[user_key]["login_username"] != new_username and new_username != None :
                    known_records[user_key]["login_username"] = new_username
                if known_records[user_key]["login_password"] != new_password and new_password != None :
                    known_records[user_key]["login_password"] = new_password
    elif (x >= (dpx + upx)) and (x < (dpx + upx + ipx)) : # insert
        print("insert")
        fname, minit, lname = gen.gen_name()
        username = gen.gen_username(fname, lname, minit=minit, random_int_included=False)
        password = gen.gen_password()
        res = insert_user_credentials(username, password)
        if res == None :
            user_id = find_user_info(username)[0]
            known_records[str(user_id)] = {
                "user_id" : user_id,
                "fname" : fname,
                "minit" : minit,
                "lname" : lname,    
                "login_username" : username,
                "login_password" : password
            }

    # Don't mess with this line
    time.sleep(random.random() * tfx)

# record records in a tsv
with open(known_records_path, "w", buffering = True) as file :
    for key in known_records.keys() :
        file.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n".format(known_records[key]["user_id"],
                                                          known_records[key]["fname"],
                                                          known_records[key]["minit"],
                                                          known_records[key]["lname"],
                                                          known_records[key]["login_username"],
                                                          known_records[key]["login_password"]))
file.close()
