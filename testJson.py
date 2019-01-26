import sys
import urllib2,json

def main():
	with open("./score.json",'r') as load_f:
		responseJson = json.load(load_f)
	print responseJson.get("kotomo").keys()

if __name__ == "__main__":
	main()