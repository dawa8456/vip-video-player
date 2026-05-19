from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.utils import platform
from urllib.parse import urlparse
import webbrowser

KV = '''
Screen:
    MDBoxLayout:
        orientation: 'vertical'
        padding: dp(12)
        spacing: dp(10)

        MDToolbar:
            title: "VIP 视频播放器"
            md_bg_color: app.theme_cls.primary_color
            elevation: 6

        MDLabel:
            text: "仅供学习交流使用，注意版权与合法性"
            halign: "center"
            theme_text_color: "Secondary"
            font_style: "Caption"

        MDTextField:
            id: url_field
            hint_text: "输入视频链接（http/https）"
            size_hint_x: 1
            pos_hint: {"center_x": .5}
            multiline: False
            on_text_validate: app.on_play()
            helper_text_mode: "on_focus"

        MDBoxLayout:
            adaptive_height: True
            spacing: dp(8)

            MDDropDownItem:
                id: parser_item
                text: app.parsers[0]
                pos_hint: {"center_y": .5}
                on_release: app.open_parsers_menu(self)

            MDRaisedButton:
                text: "播放"
                on_release: app.on_play()
            MDFlatButton:
                text: "清空"
                on_release:
                    url_field.text = ""
                    app.show_message("已清空")

        MDLabel:
            id: info
            text: ""
            halign: "center"
            theme_text_color: "Primary"
            font_style: "Caption"

        MDBoxLayout:
            adaptive_height: True
            spacing: dp(8)
            padding: dp(6)

            MDIconButton:
                icon: "open-in-new"
                on_release: app.open_raw()
                tooltip_text: "打开原站"

            MDIconButton:
                icon: "cog-outline"
                on_release: app.show_message("解析器在代码或配置中编辑")
                tooltip_text: "设置解析器"
'''

from kivymd.uix.menu import MDDropdownMenu
from kivymd.toast import toast

class VIPApp(MDApp):
    parsers = [
        "https://jx.xmflv.cc/?url=",
        "https://jx.618g.com/?v=",
    ]

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        self.root = Builder.load_string(KV)
        Window.softinput_mode = "below_target"
        self._build_parsers_menu()
        return self.root

    def _build_parsers_menu(self):
        items = []
        for p in self.parsers:
            items.append({
                "viewclass": "OneLineListItem",
                "text": p,
                "on_release": lambda x=p: self.select_parser(x)
            })
        self.parsers_menu = MDDropdownMenu(
            caller=self.root.ids.parser_item,
            items=items,
            width_mult=6
        )

    def open_parsers_menu(self, caller):
        self.parsers_menu.caller = caller
        self.parsers_menu.open()

    def select_parser(self, parser_url):
        self.root.ids.parser_item.set_item(parser_url)
        self.parsers_menu.dismiss()

    def is_valid_url(self, url: str) -> bool:
        if not url:
            return False
        u = url.strip()
        if not urlparse(u).scheme:
            u = "http://" + u
        p = urlparse(u)
        return p.scheme in ("http", "https") and bool(p.netloc)

    def normalized_url(self, url: str) -> str:
        u = url.strip()
        if not urlparse(u).scheme:
            u = "http://" + u
        return u

    def on_play(self):
        url = self.root.ids.url_field.text.strip()
        if not url:
            self.show_message("请输入视频链接")
            return
        if not self.is_valid_url(url):
            self.show_message("无效链接，请检查（http/https）")
            return
        parser = self.root.ids.parser_item.text or self.parsers[0]
        final = parser + self.normalized_url(url)
        try:
            # On Android consider using plyer or intent; webbrowser often works
            webbrowser.open(final)
            self.show_message("已打开解析链接")
        except Exception as e:
            self.show_message(f"打开失败: {e}")

    def open_raw(self):
        url = self.root.ids.url_field.text.strip()
        if not self.is_valid_url(url):
            self.show_message("无效链接")
            return
        try:
            webbrowser.open(self.normalized_url(url))
            self.show_message("已打开原站链接")
        except Exception as e:
            self.show_message(f"打开失败: {e}")

    def show_message(self, text: str):
        # 使用 toast 在移动端体验更好
        if platform == "android" or platform == "ios":
            toast(text)
        else:
            self.root.ids.info.text = text

if __name__ == '__main__':
    VIPApp().run()
