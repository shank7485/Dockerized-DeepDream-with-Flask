#from deepdream import main
import glob
import os
import Queue
#import thread
import subprocess

waiting_list = Queue.Queue()

def find_newly_added(path):
    newest = max(glob.iglob(path + '*.jpg'), key=os.path.getctime)
    return newest

"""
RUNNING IN THREADS:

def inputs_folder_checker(newest):
        while(True):
            temp = find_newly_added("/opt/deepdream/inputs/")
            if newest != temp:
                newest = temp
                waiting_list.put(newest)
                thread.start_new_thread(main, (waiting_list.get(), ))
"""

"""
RUNNING A SEPARATE PROCESS:
"""

def inputs_folder_checker(newest):
        while(True):
            temp = find_newly_added("/opt/deepdream/inputs/")
            if newest != temp:
                newest = temp
                waiting_list.put(newest)
                subprocess.call(['python', 'deepdream.py', waiting_list.get()])

inputs_folder_checker("/opt/deepdream/inputs/")

"""
def inputs_folder_checker(newest):
        while(True):
            temp = find_newly_added("/opt/deepdream/inputs/")
            if newest != temp:
                newest = temp
                waiting_list.put(newest)
                customer = waiting_list.get()
                print "Started Deep Dream with {}".format(customer)
                main(customer)
                print "Deep Dream Over"

inputs_folder_checker("/opt/deepdream/inputs/")
"""
