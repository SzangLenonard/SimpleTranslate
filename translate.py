import sublime
import sublime_plugin
import urllib
import json

API_URL = "https://translate.googleapis.com/translate_a/single?client=gtx"

class TranslateCommand(sublime_plugin.TextCommand):
	
	def translate(self,TEXT,SOURCE_LANG,TARGET_LANG):
		TEXT = urllib.parse.quote(TEXT.encode("utf-8"))
		GET_LINK  = "{0}&sl={1}&tl={2}&dt=t&q={3}".format(API_URL,SOURCE_LANG,TARGET_LANG,TEXT)
		x = urllib.request.urlopen(GET_LINK)
		data = x.read()
		obj = json.loads(str(data,'utf-8'))
		result = []
		for x in obj[0]:
			result.append(x[0])
		return "".join(result)

	def loadSetting(self):
		if not hasattr(self,"setting"):
			self.settings = sublime.load_settings("Translate.sublime-settings")
	
	def run(self, edit):
		self.loadSetting() # Load setting file 
		view = self.view
		sel = view.sel()
		selection = sel[0]
		selectionText = view.substr(selection) # Get selection 
		if len(selectionText) >0:
			slang = self.settings.get("source_lang") # source lang config 
			tlang = self.settings.get("target_lang") # target lang 
			inserting = self.translate(selectionText,slang,tlang)
			'''Data after call api'''
			self.view.insert(edit, selection.end() , " {0}".format(inserting)) # insert to current View window
