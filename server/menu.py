from telebot import types

bot = None

back_str = ''
wrong_msg = None


def clean(chat_id):
	bot.pre_message_subscribers_next_step[chat_id] = []


class Instance:
	def __init__(self, name, callback=None, back=True):
		super().__init__()
		self.name = name
		self.children = []
		self.column = []
		self.back_button = back
		if type(callback) is str:
			self.message = callback
			self.list_handler = None
		else:
			self.list_handler = callback
			self.message = None
		if back:
			b = Instance("Back", "UP", back=False)
			self.children.append(b)
		self.parent = None

	def make_keyboard(self):
		markup = types.ReplyKeyboardMarkup()
		for child in self.children:
			r = [child.name]
			for col in child.column:
				r.append(col.name)
			markup.row(*r)
		return markup

	def append_column(self, name, callback=None, back_button=True):
		col = Instance(name, callback=callback, back=back_button)
		self.column.append(col)
		col.parent = self.parent
		return col

	def get_column(self, name=None):
		columns = [self]
		columns.extend(self.column)
		if name is not None:
			for c in columns:
				if name == c.name:
					return c
		return columns

	def get_row(self, name):
		strings = name.split(">")
		cur = self
		for s in strings:
			cur = self.__find(cur, s)
			if cur is None:
				return
		return cur

	def __find(self, cur, name):
		for child in cur.children:
			if child.name == name:
				return child

	def add_row(self, name, callback=None, back_button=True):
		child = Instance(name, callback=callback, back=back_button)
		if self.back_button:
			temp = self.children.pop()
		self.children.append(child)
		if self.back_button:
			self.children.append(temp)
		child.parent = self
		return child

	def get_node(self, text):
		for child in self.children:
			if child.name == text:
				return child
			for col in child.column:
				if col.name == text:
					return col

	@staticmethod
	def check(msg):
		return msg.text is None

	def handler(self, message):
		if message.text == '/start':
			return
		next_menu = self.get_node(message.text)
		clean(message.chat.id)
		if (message.text == "Back") & (self.parent is not None):
			print(str(message.chat.id) + "    Go Back from \"" + self.name + "\" to \"" + self.parent.name + "\"")
			bot.register_next_step_handler(message, self.parent.handler)
			bot.send_message(message.chat.id, back_str, reply_markup=self.parent.make_keyboard())
			return
		if (next_menu is None) | (self.check(message)):
			print(str(message.chat.id) + "    Wrong message : " + self.name + "    message=\"" + str(message.text) + "\"")
			if wrong_msg is not None:
				bot.send_message(message.chat.id, wrong_msg, reply_markup=self.make_keyboard())
			bot.register_next_step_handler(message, self.handler)
			return
		if next_menu.list_handler is not None:
			s = next_menu.list_handler(message)
			if s is not None:
				if type(s) == str:
					next_menu.message = s
				else:
					return
			print(str(message.chat.id) + "    Callback was fired : \"" + next_menu.name + "\"")
		if True if (len(next_menu.children) == 0) else (next_menu.children[0].name == "Back"):
			if next_menu.list_handler is None:
				print(str(message.chat.id) + "    Need a list_callback : \"" + next_menu.name + "\"")
			bot.send_message(message.chat.id, next_menu.message, reply_markup=self.make_keyboard())
			bot.register_next_step_handler(message, self.handler)
			return
		print(str(message.chat.id) + "    Go next from \"" + self.name + "\" to \"" + next_menu.name + "\"")
		if (next_menu.message is not None) & (message.text == 'Back'):
			next_menu.message = 'Up'
		bot.send_message(message.chat.id, next_menu.message, reply_markup=next_menu.make_keyboard())
		bot.register_next_step_handler(message, next_menu.handler)


class Menu:
	def __init__(self, name, message, b):
		super().__init__()
		self.root = Instance(name, callback=message, back=False)
		global bot
		bot = b

	def set_back(self, str):
		global back_str
		back_str = str

	def set_wrong(self, str):
		global wrong_msg
		wrong_msg = str

	def get_root(self):
		return self.root
