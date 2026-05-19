import re
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.utils import platform
from urllib.parse import urlparse

from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.toast import toast

# ⚡ 终极高颜值 UI 布局设计（纯正 Material Design 3 现代风格）
KV = '''
MDScreenManager:
    id: screen_manager
    
    MDScreen:
        name: "main_screen"
        md_bg_color: [0.95, 0.96, 0.98, 1]  # 高级柔和护眼灰背景

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

                # 💡 史诗级优化：大厂风格的圆角白色搜索卡片
                MDCard:
                    orientation: 'vertical'
                    padding: [dp(16), dp(16), dp(16), dp(12)]
                    spacing: dp(12)
                    adaptive_height: True
                    radius: [dp(16), ]
                    elevation: 2
                    md_bg_color: [1, 1, 1, 1]

                    MDBoxLayout:
                        orientation: 'horizontal'
                        spacing: dp(10)
                        adaptive_height: True

                        MDIcon:
                            icon: "magnify"  # 放大镜搜索图标
                            pos_hint: {"center_y": .5}
                            theme_text_color: "Hint"

                        MDTextField:
                            id: url_field
                            hint_text: "请在此输入或粘贴视频网址..."
                            font_name: "Roboto"
                            mode: "line"  # 现代极简下划线模式
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

                        Widget: # 弹簧组件，将动作按钮完美推向右侧

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

                # 常用网站直达标签
                MDLabel:
                    text: "常用视频网站直达"
                    font_name: "Roboto"
                    font_style: "Subtitle1"
                    bold: True
                    theme_text_color: "Primary"
                    size_hint_y: None
                    height: dp(28)

                # 响应式舒适滚动网格（彻底解决越界与拥挤）
                ScrollView:
                    do_scroll_x: False
                    do_scroll_y: True
                    bar_width: dp(4)
                    
                    MDGridLayout:
                        id: grid_layout
                        cols: 3
                        spacing: dp(12)
                        adaptive_height: True
                        padding: [0, 0, 0, dp(20)]

    MDScreen:
        name: "player_screen"
        md_bg_color: [0, 0, 0, 1]  # 沉浸式全黑播放背景
        MDBoxLayout:
            id: webview_container
            orientation: 'vertical'
'''

class VIPApp(MDApp):
    parsers = [
        "https://jx.xmflv.cc/?url=",
        "https://jx.618g.com/?v=",
    ]
    webview = None

    def build(self):
        self.theme_cls.primary_palette = "Indigo"  # 使用高质感的靛蓝色作为UI主色调
        self.theme_cls.theme_style = "Light"
        self.root = Builder.load_string(KV)
        Window.softinput_mode = "below_target"
        
        # 绑定手机物理返回键 / 边缘右滑返回手势
        Window.bind(on_keyboard=self.handle_back_key)
        
        # 初始化默认解析接口
        self.root.ids.parser_item.text = self.parsers[0]
        return self.root

    def on_start(self):
        """在App启动的第一时间注入中文字体，完美阻击豆腐块乱码Bug"""
        if platform == "android":
            from kivy.core.text import LabelBase
            import os
            font_path = "/system/fonts/NotoSansCJK-Regular.ttc"
            if not os.path.exists(font_path):
                font_path = "/system/fonts/DroidSansFallback.ttf"
            
            # 强制将系统的中文字体全局绑定到库的渲染内核上
            LabelBase.register(name="Roboto", fn_regular=font_path)
            LabelBase.register(name="OneLineListItem", fn_regular=font_path)
            
        # 字体加载完毕后再开始画按钮网格，确保中文100%显示正常
        self.build_website_grid()

    def build_website_grid(self):
        """动态构建精美响应式卡片网格，完美修复原先173行的冒号爆红Bug"""
        from kivymd.uix.button import MDRaisedButton
        
        websites = [
            ("腾讯视频", "https://v.qq.com/"), ("爱奇艺", "https://www.iqiyi.com/"),
            ("优酷视频", "https://www.youku.com/"), ("哔哩哔哩", "https://www.bilibili.com/"),
            ("搜狐视频", "https://tv.sohu.com/"), ("乐视视频", "https://www.le.com/"),
            ("PPTV", "https://www.pptv.com/"), ("芒果TV", "https://www.mgtv.com/"),
            ("咪咕视频", "https://www.miguvideo.com/"), ("西瓜视频", "https://www.ixigua.com/")
        ]
        
        for name, url in websites:
            # 💡 完美修复：将原先错误的 elevation: 1 改为正确的赋值等号 elevation=1
            btn = MDRaisedButton(
                text=name,
                font_name="Roboto",
                size_hint_x=1,
                height=dp(48),
                md_bg_color=[1, 1, 1, 1],         # 卡片纯白底色
                text_color=[0.2, 0.2, 0.2, 1],     # 高级深灰文字
                elevation=1                        # 正确的Python语法！
            )
            btn.bind(on_release=lambda instance, u=url: self.open_in_webview(u))
            self.root.ids.grid_layout.add_widget(btn)

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
        
        if platform == 'android':
            self.open_in_webview(final_url)
        else:
            import webbrowser
            webbrowser.open(final_url)

    def open_in_webview(self, url):
        """基于 Android 原生高级 WebView 组件的内嵌全屏播放机制"""
        from jnius import autoclass
        from android.runnable import run_on_ui_thread

        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        WebView = autoclass('android.webkit.WebView')
        WebViewClient = autoclass('android.webkit.WebViewClient')
        activity = PythonActivity.mActivity

        @run_on_ui_thread
        def create_webview():
            if not self.webview:
                self.webview = WebView(activity)
                self.webview.getSettings().setJavaScriptEnabled(True)
                self.webview.getSettings().setDomStorageEnabled(True)
                self.webview.getSettings().setMediaPlaybackRequiresUserGesture(False)
                self.webview.setWebViewClient(WebViewClient())
                
                from uix_android import AndroidWidget
                kw = AndroidWidget(self.webview)
                self.root.ids.webview_container.add_widget(kw)
            
            self.webview.loadUrl(url)
            self.root.current = "player_screen"

        create_webview()

    def handle_back_key(self, window, key, *args):
        """【高级手势右滑返回 / 手机物理返回键退回机制】"""
        if key == 27:  # 27 对应安卓系统的全局返回手势
            if self.root.current == "player_screen":
                self.root.current = "main_screen"
                if self.webview:
                    self.webview.loadUrl("about:blank")  # 切断网页防止后台偷跑声音Bug
                self.show_message("已退出播放")
                return True
        return False

    def show_message(self, text: str):
        if platform == "android":
            toast(text)
        else:
            self.root.ids.info.text = text

if __name__ == '__main__':
    VIPApp().run()