import sys
import TileProblem
import heapq 
import time
import datetime
import math
import psutil
import os

from TileProblem import TileProblem
from queue import PriorityQueue

states_explored = 0

def problemInput(algo,problem_size,heuristic,input_file,output_file):
	tileProblem = TileProblem(start=True,input_file=input_file,problem_size=problem_size)
	if algo == 1:
		a_star_search(tileProblem,heuristic,output_file)
	else:
		recursive_best_first_search_helper(tileProblem,heuristic,output_file)
	return tileProblem

def a_star_search(node,heuristic,output_file):
	global states_explored
	frontier = []
	explored = []
	counter = 0
	node.g = 0
	if heuristic == 1:
		heapq.heappush(frontier,(0,counter,node))
		while not len(frontier)==0:
			current_state,acn,current_node = heapq.heappop(frontier)
			states_explored = states_explored + 1
			if current_node.goal_test():
				print(f"depth: {current_node.g}")
				write_path(return_path(current_node),output_file)
				return True
			if current_node not in explored:
				explored.append(current_node)
				for action in list(TileProblem.actions):
					new = current_node.transition_function(action,current_node)
					if new is None: 
						continue
					counter = counter + 1
					new.g = current_node.g + 1
					new.h = new.manhattan_distance()
					new.f = new.g+new.h
					heapq.heappush(frontier,(new.f,counter,new))
	else:
		heapq.heappush(frontier,(0,counter,node))
		while not len(frontier)==0:
			current_state,acn,current_node = heapq.heappop(frontier)
			states_explored = states_explored + 1
			if current_node.goal_test():
				print(f"depth: {current_node.g}")
				write_path(return_path(current_node),output_file)
				return True
			if current_node not in explored:
				explored.append(current_node)
				for action in list(TileProblem.actions):
					new = current_node.transition_function(action,current_node)
					if new is None: 
						continue
					counter = counter + 1
					new.g = current_node.g + 1
					new.h = new.misplaced_tile()
					new.f = new.g+new.h
					heapq.heappush(frontier,(new.f,counter,new))

def recursive_best_first_search_helper(node,heuristic,output_file):
	node.g=0
	if heuristic == 1:
		node.h = node.manhattan_distance()
		node.f = node.g + node.h
		return recursive_best_first_search1(node,math.inf,output_file)
	else:
		node.h = node.misplaced_tile()
		node.f = node.g + node.h
		return recursive_best_first_search2(node,math.inf,output_file)

def recursive_best_first_search1(node,flimit,output_file):
	global states_explored
	states_explored = states_explored + 1
	if node.goal_test():
		print(f"depth: {node.g}")
		write_path(return_path(node),output_file)
		return True,0
	successors = []
	for action in list(TileProblem.actions):
		child = node.transition_function(action,node)
		if child:
			child.g = node.g + 1
			child.h = child.manhattan_distance()
			child.f = child.g+child.h
			successors.append((child.f,child))
	if len(successors) == 0:
		return False,math.inf
	for i in range(len(successors)):
		si = successors[i][1]
		si.f = max(si.g+si.h,node.f)
		successors[i] = (si.f,si)
	successors = sorted(successors,key=lambda x: x[0])
	while True:
		best = successors[0][1]
		if best.f > flimit:
			return False,best.f
		alt = successors[1][0]
		(result,best.f) = recursive_best_first_search1(best,min(flimit,alt),output_file)
		for i in range(len(successors)):
			if best == successors[i][1]:
				successors[i] = (best.f,best)
		successors = sorted(successors,key=lambda x: x[0])
		if result:
			return (result,best.f)

def recursive_best_first_search2(node,flimit,output_file):
	global states_explored
	states_explored = states_explored + 1
	if node.goal_test():
		print(f"depth: {node.g}")
		write_path(return_path(node),output_file)
		return True,0
	successors = []
	for action in list(TileProblem.actions):
		child = node.transition_function(action,node)
		if child:
			child.g = node.g + 1
			child.h = child.misplaced_tile()
			child.f = child.g+child.h
			successors.append((child.f,child))
	if len(successors) == 0:
		return False,math.inf
	for i in range(len(successors)):
		si = successors[i][1]
		si.f = max(si.g+si.h,node.f)
		successors[i] = (si.f,si)
	successors = sorted(successors,key=lambda x: x[0])
	while True:
		best = successors[0][1]
		if best.f > flimit:
			return False,best.f
		alt = successors[1][0]
		(result,best.f) = recursive_best_first_search2(best,min(flimit,alt),output_file)
		for i in range(len(successors)):
			if best == successors[i][1]:
				successors[i] = (best.f,best)
		successors = sorted(successors,key=lambda x: x[0])
		if result:
			return (result,best.f)

def return_path(node):
	current_node = node
	path = []
	while current_node.parent:
		path = [current_node.parent[1]] + path
		current_node = current_node.parent[0]
	return path

def write_path(path,output_file):
	strpath = ""
	for i in range(len(path)):
		if path[i] == TileProblem.actions.LEFT:
			strpath += "L"
		elif path[i] == TileProblem.actions.RIGHT:
			strpath += "R"
		elif path[i] == TileProblem.actions.UP:
			strpath += "U"
		elif path[i] == TileProblem.actions.DOWN:
			strpath += "D"
		if i + 1 < len(path):
			strpath += ","
	with open(output_file,'w') as fwrite:
		fwrite.write(strpath)

if __name__ == '__main__':
	if len(sys.argv) == 6:
		start = datetime.datetime.now()
		tp = problemInput(int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),sys.argv[4],sys.argv[5])
		stop = datetime.datetime.now()
		print(f"Memory Usage (in bytes): {psutil.Process(os.getpid()).memory_info().rss}")
		print(f"States Explored: {states_explored}")
		print(f"Time (in milliseconds): {(stop-start).total_seconds()*1e3}")
	else:
		tp = problemInput(2,3,2,"puzzle3.txt","puzzle3out.txt")