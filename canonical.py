def ConverBits(data, fromBits, toBits, pad):

	maxSize = int((len(data) * int(fromBits)) / toBits) + 1
	regrouped = []

	nextByte = 0
	filledBits = 0

	for i in range(len(data)):

		data[i] = data[i] << (8 - fromBits) # 안 쓰는 bit 버리기
		remFromBits = fromBits

		while(remFromBits > 0):
			remToBits = toBits - filledBits

			toExtract = remFromBits
			if(remToBits < toExtract):
				toExtract = remToBits

			nextByte = (nextByte << toExtract) | (data[i] >> (8 - toExtract))

			data[i] = data[i] << toExtract
			remFromBits -= toExtract
			filledBits += toExtract

			if filledBits == toBits:
				regrouped.append(nextByte)
				filledBits = 0
				nextByte = 0

	if pad and filledBits > 0:
		nextByte = nextByte << (toBits - filledBits)
		regrouped.append(nextByte)
		filledBits = 0
		nextByte = 0

	if filledBits > 0 and (filledBits > 4 or nextByte != 0):
		return 0

	return regrouped

if __name__ == "__main__":

	charset = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"
	
	human = "wasm1j5ad7ah3qte6tn9xnvvx6jlfm6uqsvxxqu5rfs"
	check = human.find("1")
	hrp = human[:check]
	value = human[check+1:]
	data = []

	for i in value:
		data.append(charset.find(i))

	checksum = data[len(value)-6:]
	data = data[:len(value)-6]
	
	result = ConverBits(data, 5, 8, False)
	canon = ""

	for i in result:
		if(len(hex(i))==5):
			canon += ''.join('{:02X}'.format(i))[1:]
		else:
			canon += ''.join('{:02X}'.format(i))

	print(canon)
