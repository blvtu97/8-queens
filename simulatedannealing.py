#Nguyễn Hoàng Thịnh - 17110372

import random
from copy import deepcopy
from math import exp

import time
'''Hàm tạo ngẫu nhiên một trạng thái khi đặt n hậu lên map'''
def createMap(n):
	chessBoard = {}
	temp = [i for i in range(n)] # Tạo danh sách các giá trị hàng sẽ đặt hậu
	random.shuffle(temp) # Tiến hành trộn mảng để cho các giá trị hàng đặt hậu là ngẫu nhiên

	column = 0 # Đặt hậu từ vị trí cột 0

	while len(temp) > 0:
		# Chọn ngẫu nhiên ra một hàng
		row = random.choice(temp)
		chessBoard[column] = row
		temp.remove(row) # Hàng đó đặt hậu thì ta xóa nó đi
		column += 1

	del temp
	return chessBoard

def cost(currentState,numOfQueens):

	# Lấy ra tất cả các key của current state
	list_key = list(currentState)

	threat = 0
	for i in range(numOfQueens):
		for j in range(i+1,numOfQueens):
			# i == j: thì 2 cặp đó cùng hàng
			# currentState[list_key[i]] - currentState[list_key[j]]) == j - i thì 2 cặp đó nằm trên
			# đường chéo
			if i==j or abs(currentState[list_key[i]] - currentState[list_key[j]]) == j - i:
				threat += 1

	return threat

'''Hàm tìm solution để đặt n hậu lên map mà chúng không ăn nhau bằng thuật toán
Simulated Annealing. Trong đó: numOfQueens là số lượng hậu cần đặt trên map numOfQueens x numOfQueens
, temperature là nhiệt độ của thuật toán temperature'''
def simulatedAnnealing(numOfQueens, temperature):

	# Tạo ra current state
	currentState = createMap(numOfQueens)

	# Ta tiến hành đi tính cost cho trạng thái này
	costOfCurrentState = cost(currentState,numOfQueens)

	T = temperature
	omega = 0.99 # Dùng cho hàm schedule(t)
	while T >0:
		T = T*omega # Đây là hàm schedule. Ban đầu T lớn, về sau T sẽ tiến tới 0
		nextState = deepcopy(currentState)

		# Ta tạo ra ngẫu nhiên một trạng thái mới
		# Ngẫu nhiên bằng cách chọn ra 2 cột bất kì, xong hoán đổi vị trí đặt hậu của chúng
		# cho nhau
		# Hàm này tương ứng với next <- a randomly selected successor of current
		while True:
			col1 = random.randrange(0, numOfQueens - 1) # Tạo ngẫu nhiên số 0<=a<= numOfQueens - 1
			col2 = random.randrange(0, numOfQueens - 1)

			if col1 != col2:
				break
		# Đổi 2 cột với nhau
		nextState[col1], nextState[col2] = nextState[col2],\
		nextState[col1]

		# Ta đi tính delta chi phí của trạng thái random này với trạng thái trước

		delta = cost(nextState,numOfQueens) - costOfCurrentState

		# Giá trị current = next tùy thuộc vào giá trị tối ưu của delta, ở đây ta muốn
		# delta âm, vì ta muốn đi tìm chi phí = 0 nên buộc chi phí sau phải nhỏ hơn chi phí trước

		# Trường hợp thứ 2, ta chọn current = next dựa vào xác suất, khi T càng lớn thì
		# delta/T càng nhỏ => exp(-delta/T) càng lớn, thì xác suất càng cao, việc chon current = next
		# sẽ có tỉ lệ hơn, khi T càng về 0 thì exp(-delta/T) thì tỉ lệ current = next sẽ rất thấp

		if delta <  0 or exp(-delta/T) > random.uniform(0,1):
			currentState = deepcopy(nextState)
			costOfCurrentState = cost(currentState,numOfQueens)

		# Kiểm tra xem nếu cost = 0, nghĩa là không có cặp hậu nào ăn nhau => tìm được solution
		if costOfCurrentState == 0:
			return currentState
	return None

'''
Hàm này sẽ trả về solution tìm được và thời gian tìm ra solution đó
'''
def getResults(numOfQueens,temperature):
	startTime = time.time()
	solution = simulatedAnnealing(numOfQueens,temperature)

	return solution, time.time() - startTime



