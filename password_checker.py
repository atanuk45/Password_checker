import requests
import hashlib
import sys


def request_api_data(query_char):
	url = 'https://api.pwnedpasswords.com/range/'+query_char
	res = requests.get(url)
	#print(res.text)
	if res.status_code !=200:
		raise RuntimeError(f'Error fetching: {res.status_code}, check the api and try again')
	return res

def get_password_leaks_count(hashes, hashes_to_check):
	hashes = (line.split(':') for line in hashes.text.splitlines())
	for h, count in hashes:
		if h==hashes_to_check:
			return count
	return 0

def pwned_api_check(password):
	#print(hashlib.sha1(password.encode('utf-8')).hexdigest().upper())
	sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
	first5_char,tail=sha1password[:5],sha1password[5:]
	response = request_api_data(first5_char)
	#print(first5_char, tail)
	return get_password_leaks_count(response, tail)

def main(args):
	for password in args:
		count = pwned_api_check(password)
		if count!=0:
			print(f'your password {password} is leaked {count} times......try another password')
		else:
			print(f'your password {password} is never leaked till now !!!!well done keep going!!')
	return 'done!!'	

if __name__=='__main__':
	sys.exit(main(sys.argv[1:]))