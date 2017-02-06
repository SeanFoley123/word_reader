class Node(object):
	"""This will ONLY work for words that all start with the same letter. It starts checking at the children level, not the grandparent.
You also need to specify if the first letter begins a word.
Also credit goes to http://cbio.ufs.ac.za/live_docs/nbn_tut/trees.html
"""
	def __init__(self, value, children=None):
		self.value = value
		self.children = children
		if self.children == None:
			self.children = []

	def check(self, string_in, index=0):								#checks if the next index of the given string is the value of any of self's children. I think this one works.
		i = 0															#index of which child you are at
		letter_is_word = string_in[0] in ['a', 'i', 'o']
		if len(string_in)==1 and letter_is_word:						#Depends on the letter: a is a word, e is not.
		 	return True
		while True:														#as long as you don't have a result, keep checking through the children
			if i == len(self.children):									#if we've exhausted all the children without returning a true
				return False
			child = self.children[i]
			if child.value == string_in[index+1]:						#if the child has the value of the next index of the string: so, if 
				if index+1 == len(string_in)-1:
					return child.is_leaf()
				else:													#not the end of the string, so go another layer deep
					return child.check(string_in, index+1)
			i += 1

	def display(self, level = 0):
		ret = "\t"*level+repr(self.value)+"\n"
		for child in self.children:
			ret += child.display(level+1)
		return ret

	def is_leaf(self):
		for child in self.children:										#is it a standalone word? ex: cartoon is a word. Every word must end in ''
			if child.value == '':
				return True
		return False

	def return_children_values(self):
		result = []
		for child in self.children:
			result.append(child.value)
		return result

def create_node(word_list, start_letter):
	whole_node = Node(start_letter)
	added_node = False
	for word in word_list:
		current_node = whole_node
		for i in range(1, len(word)):
			for child in current_node.children:
				if word[i] == child.value:
					current_node = child
					added_node = True
					break
			if not added_node:
				new_node = Node(word[i], [])
				current_node.children.append(new_node)
				current_node = new_node
			added_node = False
		current_node.children.append(Node(''))
	return whole_node

def list_words(word_in):
	all_words_file = open('words.txt')									#makes a list of words out of the file
	all_words = []
	for word in all_words_file:
		all_words.append(word.strip())
	all_words.sort()

	end_index = 0														#makes a dictionary of lists of words starting with each letter
	list_dict = {}
	for letter in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']:
		temp = []
		for i in range(end_index, len(all_words)):
			if all_words[i][0] != letter:
				end_index = i 
				break
			temp.append(all_words[i])
		list_dict[letter] = temp

	node_dict = {}
	for key in list_dict:												#turns the dictionary of lists into a dictionary of trees
		node_dict[key] = create_node(list_dict[key], key)
	
	words_result = []
	for i in range(len(word_in)):
		for k in range(i+1, len(word_in)):
			if word_in[i:k+1] not in words_result:
				result = node_dict[word_in[i]].check(word_in[i:k+1])
				if result:
					words_result.append(word_in[i:k+1])
	for i  in range(len(words_result)):
		words_result[i] = words_result[i].title()

	words_result.sort()													#make the list sorted a. by length and b. alphabetically
	words_result.sort(key=len, reverse=True)

	print
	print words_result													#prints results and restarts
	print
	word_input(False)

def word_input(first):
	if first:
		user_word = raw_input('Enter a word: ')
	else:
		user_word = raw_input('Enter another word! This is fun!: ')
	user_word = user_word.lower()
	adjusted_input = []
	for letter in user_word:
		if letter in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']:
			adjusted_input.append(letter)
	adjusted_input = ''.join(adjusted_input)
	list_words(adjusted_input)
if __name__ == '__main__':
	word_input(True)