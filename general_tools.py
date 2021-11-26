'''
Created on 14 Jan 2013

simple functions for things like progress bars and saving data to pickle files

@author: Kieran Finn
'''
import pickle

def pload(fname):
    f=open(fname,'rb')
    try:
        out=pickle.load(f)
    except:
        f.close()
        f=open(fname,'r')
        out=pickle.load(f)
    f.close()
    return out

def pdump(obj,fname):
    f=open(fname,'wb')
    pickle.dump(obj,f)
    f.close()
  
def read_file(fname):
    f=open(fname,'r')
    out=f.read()
    f.close()
    return out

def list_to_extension(int_list):
    out=''
    for i in int_list:
        out+='_%d' %i
    return out

def check_in_sorted(item, sorted_list):
    hi=len(sorted_list)-1
    lo=0
    while lo<=hi:
        mid=int((hi+lo)/2)
        if sorted_list[mid]==item:
            return True
        if item<sorted_list[mid]:
            hi=mid-1
        else:
            lo=mid+1
    return False