import sublime
import sublime_plugin
import urllib
import json

API_URL = "https://translate.googleapis.com/translate_a/single?client=gtx"
TARGET_LANG = "en"
SOURCE_LANG = "vi"

class TranslateCommand(sublime_plugin.TextCommand):
	def translate(self,TEXT,SOURCE,TARGET):
		# TEXT="tôi sẽ dạy bạn viết tiếng anh"
		TEXT = urllib.parse.quote(TEXT.encode("utf-8"))
		GET_LINK  = "{0}&sl={1}&tl={2}&dt=t&q={3}".format(API_URL,SOURCE_LANG,TARGET_LANG,TEXT)
		x = urllib.request.urlopen(GET_LINK)
		result = x.read()
		obj = json.loads(str(result,'utf-8'))
		j = []
		for x in obj[0]:
			j.append(x[0])
		return "".join(j)
		

	def run(self, edit):
		view = self.view
		sel = view.sel()
		print("Plugin callHello, World! 123",type(edit))
		selection = sel[0]
		selectionText = view.substr(selection)
		if len(selectionText) >0:
			inserting = self.translate(selectionText)
			self.view.insert(edit, selection.end() , " {0}".format(inserting))
