import requests
from flask import render_template
import hashlib

def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching :{res.status_code},TRY AGAIN!!')
    return res


def pwned_api_check(password):
   
    sha1pass = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    head,tail = sha1pass[:5] , sha1pass[5:]
    response = request_api_data(head)
  
    return get_pass_leaks_count(response,tail)





def get_pass_leaks_count(hashes,hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h , count in hashes:
       if h == hash_to_check:
           return(count)
    return 0

def main(user_pass):
    count = pwned_api_check(user_pass)
    if count:
        return render_template('got_pwned.html',user_pass=user_pass,count=count)
       
    else:
        return render_template('not_pwned.html',user_pass=user_pass,count=count)

      

