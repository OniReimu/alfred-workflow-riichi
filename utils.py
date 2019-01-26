def strSlicedNumber(string):
	fu = ""
	for i in string:
		if i.isdigit():
			fu += i
		else:
			break
	return fu

def strSlicedAlpha(string):
	fu = ""
	for i in string:
		if i.isalpha() or is_Chinese(i):
			fu += i
		else:
			break
	return fu

def is_Chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False