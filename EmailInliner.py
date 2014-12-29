import sublime, sublime_plugin, urllib, json


class EmailInlineCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		region = sublime.Region(0, self.view.size())
		content = self.view.substr(region)

		api_url = 'http://premailer.dialect.ca/api/0.1/documents'
		values = { 	'html' : content,
					'adapter' : view.settings().get('ei_premailer_adapter'),
					'base_url' : view.settings().get('ei_premailer_base_url'),
					'link_query_string' : view.settings().get('ei_premailer_link_query_string'),
					'preserve_styles' : view.settings().get('ei_premailer_preserve_styles'),
					'remove_ids' : view.settings().get('ei_premailer_remove_ids'),
					'remove_clases' : view.settings().get('ei_premailer_remove_classes'),
					'remove_comments' : view.settings().get('ei_premailer_remove_comments') }

		data = urllib.parse.urlencode(values)
		data = data.encode('utf-8')
		req = urllib.request.urlopen(api_url, data)
		api_response = req.read().decode('utf-8')

		obj = json.loads(api_response)
		html_url = obj['documents']['html']

		content_req = urllib.request.urlopen(html_url)
		inlined_content = content_req.read().decode('utf-8')


		self.view.replace(edit, region, inlined_content)