import sublime, sublime_plugin

import json

from .translator import Translate

class stTranslateCommand(sublime_plugin.TextCommand):
    def run(self, edit, source_language='', target_language=''):
        settings = sublime.load_settings("stTranslate.sublime-settings")
        if not source_language:
            source_language = settings.get("source_language")
        if not source_language:
            source_language = 'auto'

        if not target_language:
            target_language = settings.get("target_language")
        if not target_language:
            print("ERROR: target language parameter is not found")
            self.view.window().run_command("show_panel", {"panel": "console"})
            return

        raw_texts = []
        for region in self.view.sel():
            raw_texts.append(self.view.substr(region))

        # print('selection: {0}'.format(raw_texts))
        translate = Translate(source_language, target_language)
        result = translate.GoogleTranslate("\n\n\n".join(raw_texts), source_language, target_language)

        panel = self.view.window().create_output_panel("translate_my")
        panel.run_command("set_setting", {"setting": "word_wrap", "value": True});
        panel.set_read_only(False)
        panel.run_command("append", {"characters": result})
        panel.set_read_only(True)
        self.view.window().run_command('show_panel', {"panel": "output.translate_my"})

        if not source_language:
            detected = 'Auto'
        else:
            detected = source_language

        sublime.status_message(u'Done! (translate '+detected+' --> '+target_language+')')


    def is_visible(self):
        for region in self.view.sel():
            if not region.empty():
                return True
        return False


class stTranslateToCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        settings = sublime.load_settings("stTranslate.sublime-settings")
        source_language = settings.get("source_language")
        target_language = settings.get("target_language")

        translate = Translate(source_language, target_language)

        langs = translate.langs
        lkey = []
        ltrasl = []

        for (slug, title) in langs.items():
            lkey.append(slug)
            ltrasl.append(title+' ['+slug+']')

        def on_done(index):
            if index >= 0:
                self.view.run_command("st_translate", {"target_language": lkey[index]})

        self.view.window().show_quick_panel(ltrasl, on_done)

    def is_visible(self):
        for region in self.view.sel():
            if not region.empty():
                return True
        return False


class stTranslateInfoCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        settings = sublime.load_settings("stTranslate.sublime-settings")
        source_language = settings.get("source_language")
        target_language = settings.get("target_language")

        translate = Translate(source_language, target_language)
        # print(translate.langs)
        text = (json.dumps(translate.langs, ensure_ascii = False, indent = 2))

        print("{0}".format(text)) 
        notification = '[Google] translate, supported {0} languages.'.format(len(translate.langs))
        sublime.status_message('{0} Check console.'.format(notification))
        sublime.active_window().run_command("show_panel", {"panel": "console"})
