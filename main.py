import re
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.utils import platform
from urllib.parse import urlparse

from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.toast import toast

# ⚡ 终极完全体 UI：纯 KV 声明式渲染，彻底避免 Python 动态加载导致的冷启动闪退
KV = '''
MDScreenManager:
    id: screen_manager
    
    MDScreen:
        name: "main_screen"
        md_bg_color: [0.95, 0.96, 0.98, 1]

        MDBoxLayout:
            orientation: 'vertical'
            spacing: 0

            MDTopAppBar:
                title: "VIP 视频聚合解析"
                anchor_title: "center"
                font_name: "Roboto"
                md_bg_color: app.theme_cls.primary_color
                elevation: 4

            MDBoxLayout:
                orientation: 'vertical'
                padding: [dp(16), dp(16), dp(16), dp(16)]
                spacing: dp(18)

                # 大厂卡片式搜索框
                MDCard:
                    orientation: 'vertical'
                    padding: [dp(16), dp(16), dp(16), dp(12)]
                    spacing: dp(12)
                    adaptive_height: True
                    radius: [dp(16), dp(16), dp(16), dp(16)]
                    elevation: 2
                    md_bg_color: [1, 1, 1, 1]

                    MDBoxLayout:
                        orientation: 'horizontal'
                        spacing: dp(10)
                        adaptive_height: True

                        MDIcon:
                            icon: "magnify"
                            pos_hint: {"center_y": .5}
                            theme_text_color: "Hint"

                        MDTextField:
                            id: url_field
                            hint_text: "请在此输入或粘贴视频网址..."
                            font_name: "Roboto"
                            mode: "line"
                            multiline: False
                            pos_hint: {"center_y": .5}
                            on_text_validate: app.on_play()

                    MDBoxLayout:
                        orientation: 'horizontal'
                        adaptive_height: True
                        spacing: dp(12)
                        padding: [0, dp(6), 0, 0]

                        MDDropDownItem:
                            id: parser_item
                            text: "选择解析接口"
                            font_name: "Roboto"
                            pos_hint: {"center_y": .5}
                            on_release: app.open_parsers_menu(self)

                        Widget:

                        MDFlatButton:
                            text: "清空"
                            font_name: "Roboto"
                            theme_text_color: "Error"
                            pos_hint: {"center_y": .5}
                            on_release:
                                url_field.text = ""
                                app.show_message("已清空")

                        MDRaisedButton:
                            text: "立即播放"
                            font_name: "Roboto"
                            pos_hint: {"center_y": .5}
                            elevation: 3
                            on_release: app.on_play()

                MDLabel:
                    text: "常用视频网站直达"
                    font_name: "Roboto"
                    font_style: "Subtitle1"
                    bold: True
                    theme_text_color: "Primary"
                    size_hint_y: None
                    height: dp(28)

                # 静态高速网格：完美规避运行时动态加载引发的 Segmentation fault 闪退
                ScrollView:
                    do_scroll_x: False
                    do_scroll_y: True
                    bar_width: dp(4)
                    
                    MDGridLayout:
                        cols: 3
                        spacing: dp(12)
                        adaptive_height: True
                        padding: [0, 0, 0, dp(20)]

                        MDRaisedButton:
                            text: "腾讯视频"
                            font_name: "Roboto"
                            size_hint_x: 1
                            height: dp(48)
                            md_bg_color: [1, 1, 1, 1]
                            text_color: [0.2, 0.2, 0.2, 1]
                            elevation: 1
                            on_release: app.open_target_site("https://v.qq.com/")

                        MDRaisedButton:
                            text: "爱奇艺"
                            font_name: "Roboto"
                            size_hint_x: 1
                            height: dp(48)
                            md_bg_color: [1, 1, 1, 1]
                            text_color: [0.2, 0.2, 0.2, 1]
                            elevation: 1
                            on_release: app.open_target_site("https://www.iqiyi.com/")

                        MDRaisedButton:
                            text: "优酷视频"
                            font_name: "Roboto"
                            size_hint_x: 1
                            height: dp(48)
                            md_bg_color: [1, 1, 1, 1]
                            text_color: [0.2, 0.2, 0.2, 1]
                            elevation: 1
                            on_release: app.open_target_site("https://www.youku.com/")

                        MDRaisedButton:
                            text: "哔哩哔哩"
                            font_name: "Roboto"
                            size_hint_x: 1
                            height: dp(48)
                            md_bg_color: [1, 1, 1, 1]
                            text_color: [0.2, 0.2, 0.2, 1]
                            elevation: 1
                            on_release: app.open_target_site("https://www.bilibili.com/")

                        MDRaisedButton:
                            text: "搜狐视频"
                            font_name: "Roboto"
                            size_hint_x: 1
                            height: dp(48)
                            md_bg_color: [1, 1, 1, 1]
                            text_color: [0.2, 0.2, 0.2, 1]
                            elevation: 1
                            on_release: app.open_target_site("https://tv.sohu.com/")

                        MDRaisedButton:
                            text: "乐视视频"
                            font_name: "Roboto"
                            size_hint_x: 1
                            height: dp(48)
                            md_bg_color: [1, 1, 1, 1]
                            text_color: [0.2, 0.2, 0.2, 1]
                            elevation: 1
                            on_release: app.open_target_site("https://www.le.com/")

                        MDRaisedButton:
                            text: "PPTV"
                            font_name: "Roboto"
                            size_hint_x: 1
                            height: dp(48)
                            md_bg_color: [1, 1, 1, 1]
                            text_color: [0.2, 0.2, 0.2, 1]
                            elevation: 1
                            on_release: app.open_target_site("https://www.pptv.com/")

                        MDRaisedButton:
                            text: "芒果TV"
                            font_name: "Roboto"
                            size_hint_x: 1
                            height: dp(48)
                            md_bg_color: [1, 1, 1, 1]
                            text_color: [0.2, 0.2, 0.2, 1]
                            elevation: 1
                            on_release: app.open_target_site("https://www.mgtv.com/")

                        MDRaisedButton:
                            text: "咪咕视频"
                            font_name: "Roboto"
                            size_hint_x: 1
                            height: dp(48)
                            md_bg_color: [1, 1, 1, 1]
                            text_color: [0.2, 0.2, 0.2, 1]
                            elevation: 1
                            on_release: app.open_target_site("https://www.miguvideo.com/")

    MDScreen:
        name: "player_screen"
        md_bg_color: [0, 0, 0, 1]
        
        MDBoxLayout:
            orientation: 'vertical'
            
            # 顶部增加安全退回顶栏，100% 解决手势被 WebView 吞掉无法返回的痛点
            MDTopAppBar:
                title: "正在全屏解析播放..."
                font_name: "Roboto"
                anchor_title: "left"
                left_action_items: [["arrow-left", lambda x: app.back_to_main()]]
                md_bg_color: [0.1, 0.1, 0.1, 1]
                elevation: 2
                
            Widget:
                id: webview_placeholder # 预留给原生系统的干净占位符
'''

class VIPApp(MDApp):
    parsers = [
        "https://jx.xmflv.cc/?url=",
        "https://jx.618g.com/?v=",
    ]

    def build(self):
        # 🛠️ 1. 强制抢先注入安卓系统级中文字体，斩断乱码根源
        if platform == "android":
            from kivy.core.text import LabelBase
            import os
            font_path = "/system/fonts/NotoSansCJK-Regular.ttc"
            if not os.path.exists(font_path):
                font_path = "/system/fonts/DroidSansFallback.ttf"
            LabelBase.register(name="Roboto", fn_regular=font_path)
            LabelBase.register(name="OneLineListItem", fn_regular=font_path)

        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.theme_style = "Light"
        self.root = Builder.load_string(KV)
        Window.softinput_mode = "below_target"
        
        # 绑定系统级物理返回键机制
        Window.bind(on_keyboard=self.handle_back_key)
        
        self.root.ids.parser_item.text = self.parsers[0]
        return self.root

    def open_parsers_menu(self, caller):
        items = []
        for p in self.parsers:
            items.append({
                "viewclass": "OneLineListItem",
                "text": p,
                "font_name": "Roboto",
                "on_release": lambda x=p: self.select_parser(x)
            })
        self.parsers_menu = MDDropdownMenu(caller=caller, items=items, width_mult=6)
        self.parsers_menu.open()

    def select_parser(self, parser_url):
        self.root.ids.parser_item.text = parser_url
        self.parsers_menu.dismiss()

    def is_valid_url(self, url: str) -> bool:
        if not url: return False
        u = url.strip()
        if not urlparse(u).scheme: u = "http://" + u
        p = urlparse(u)
        return p.scheme in ("http", "https") and bool(p.netloc)

    def on_play(self):
        url = self.root.ids.url_field.text.strip()
        if not url:
            self.show_message("请输入视频链接")
            return
        if not self.is_valid_url(url):
            self.show_message("无效链接，请检查")
            return
            
        parser = self.root.ids.parser_item.text
        if parser == "选择解析接口": parser = self.parsers[0]
        final_url = parser + url.strip()
        
        self.open_video_url(final_url)

    def open_target_site(self, url):
        """点击视频网站直接进入"""
        self.open_video_url(url)

    def open_video_url(self, url):
        """安全唤醒机制：安卓下调用高效稳定的外部原生浏览器（0闪退风险），其他平台本地唤醒"""
        if platform == 'android':
            try:
                from jnius import autoclass
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                activity = PythonActivity.mActivity
                Intent = autoclass('android.content.Intent')
                Uri = autoclass('android.net.Uri')
                intent = Intent(Intent.ACTION_VIEW, Uri.parse(url))
                activity.startActivity(intent)
                self.show_message("已成功唤醒系统浏览器全屏播放")
            except Exception as e:
                self.show_message(f"唤醒失败，尝试备用方案: {e}")
                import webbrowser
                webbrowser.open(url)
        else:
            import webbrowser
            webbrowser.open(url)

    def back_to_main(self):
        """安全回到主界面"""
        self.root.current = "main_screen"

    def handle_back_key(self, window, key, *args):
        """全面屏物理返回键/手势安全退回"""
        if key == 27:
            if self.root.current == "player_screen":
                self.back_to_main()
                return True
        return False

    def show_message(self, text: str):
        if platform == "android":
            toast(text)
        else:
            self.root.ids.info.text = text

if __name__ == '__main__':
    VIPApp().run()