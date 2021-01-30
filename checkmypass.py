import requests
import hashlib
import sys

def request_api_data(query_character):
	url = 'https://api.pwnedpasswords.com/range/'+ query_character
	res = requests.get(url)
	if res.status_code != 200 :
		raise RuntimeError(f'error fetching:{res.status_code},check the api and try again!')
	return res

def get_password_leak_count(hashes,hash_to_check):
	hashes = (line.split(':') for line in hashes.text.splitlines())
	for h,count in hashes:
		#print(h,count)
		if h == hash_to_check:
			return count

	

def pwned_check_api(password):
	sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
	first_5,tail = sha1password[:5],sha1password[5:]
	response = request_api_data(first_5)
	return get_password_leak_count(response,tail)
	

def main(args):
	for password in args:
		count = pwned_check_api(password)
		if count:
			print(f'{password} was found {count} times,you should change your password!')
		else:
			print(f'{password} was NOT found, carry on!')
	return 'done!'

if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]))
	
