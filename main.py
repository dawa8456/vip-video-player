import re
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.utils import platform

class VIPPlayerApp(App):
    def build(self):
        self.title = "VIP视频播放器"
        
        # 主布局（纵向排列）
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # 标题
        title_label = Label(
            text="[b]VIP视频播放器[/b]", 
            markup=True, 
            font_size='24sp', 
            size_hint_y=None, 
            height=50,
            color=(0.2, 0.2, 0.2, 1)
        )
        main_layout.add_widget(title_label)
        
        # 副标题
        subtitle_label = Label(
            text="支持大部分主流视频网站", 
            font_size='14sp', 
            size_hint_y=None, 
            height=30,
            color=(0.4, 0.4, 0.4, 1)
        )
        main_layout.add_widget(subtitle_label)
        
        # 输入框提示
        tip_label = Label(
            text="请输入或粘贴视频链接:", 
            font_size='16sp', 
            size_hint_y=None, 
            height=30, 
            halign='left', 
            valign='middle',
            color=(0.1, 0.1, 0.1, 1)
        )
        tip_label.bind(size=tip_label.setter('text_size'))
        main_layout.add_widget(tip_label)
        
        # URL 输入框（适配手机触屏多行，高度调大）
        self.url_input = TextInput(
            hint_text="https://...", 
            multiline=False, 
            font_size='16sp', 
            size_hint_y=None, 
            height=50
        )
        main_layout.add_widget(self.url_input)
        
        # 动作按钮布局
        btn_layout = BoxLayout(orientation='horizontal', spacing=15, size_hint_y=None, height=55)
        
        play_btn = Button(text="播放视频", background_color=(0.3, 0.7, 0.3, 1), font_size='16sp')
        play_btn.bind(on_release=self.play_video)
        
        clear_btn = Button(text="清空链接", background_color=(0.9, 0.3, 0.3, 1), font_size='16sp')
        clear_btn.bind(on_release=self.clear_url)
        
        btn_layout.add_widget(play_btn)
        btn_layout.add_widget(clear_btn)
        main_layout.add_widget(btn_layout)
        
        # 快捷导航标题
        nav_label = Label(
            text="快捷导航", 
            font_size='16sp', 
            size_hint_y=None, 
            height=30, 
            halign='left', 
            valign='middle',
            color=(0.1, 0.1, 0.1, 1)
        )
        nav_label.bind(size=nav_label.setter('text_size'))
        main_layout.add_widget(nav_label)
        
        # 视频网站网格布局（手机每行放3个按钮最舒适）
        grid_layout = GridLayout(cols=3, spacing=10, size_hint_y=1)
        
        websites = [
            ("腾讯视频", "https://v.qq.com/"), ("爱奇艺", "https://www.iqiyi.com/"),
            ("优酷", "https://www.youku.com/"), ("B站", "https://www.bilibili.com/"),
            ("搜狐视频", "https://tv.sohu.com/"), ("乐视视频", "https://www.le.com/"),
            ("PPTV", "https://www.pptv.com/"), ("土豆视频", "https://www.tudou.com/"),
            ("暴风影音", "https://www.baofeng.com/"), ("咪咕视频", "https://www.miguvideo.com/"),
            ("西瓜视频", "https://www.ixigua.com/")
        ]
        
        for name, url in websites:
            link_btn = Button(text=name, font_size='14sp', background_color=(0.8, 0.8, 0.8, 1))
            link_btn.bind(on_release=lambda instance, u=url: self.open_browser(u))
            grid_layout.add_widget(link_btn)
            
        main_layout.add_widget(grid_layout)
        return main_layout

    def open_browser(self, url):
        """兼容安卓底层的浏览器调用"""
        if platform == 'android':
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            activity = PythonActivity.mActivity
            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')
            intent = Intent(Intent.ACTION_VIEW, Uri.parse(url))
            activity.startActivity(intent)
        else:
            import webbrowser
            webbrowser.open(url)

    def play_video(self, instance):
        video_url = self.url_input.text.strip()
        # 简单验证
        if not video_url.startswith(('http://', 'https://')):
            self.url_input.text = ""
            self.url_input.hint_text = "请输入有效的http/https链接！"
            return
            
        parser_url = f"https://jx.xmflv.cc/?url={video_url}"
        self.open_browser(parser_url)

    def clear_url(self, instance):
        self.url_input.text = ""

if __name__ == '__main__':
    VIPPlayerApp().run()