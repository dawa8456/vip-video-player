from kivy.uix.widget import Widget
from kivy.private import build_from_cli

if not build_from_cli:
    from jnius import autoclass
    LinearLayout = autoclass('android.widget.LinearLayout')
    LayoutParams = autoclass('android.widget.LinearLayout$LayoutParams')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')

class AndroidWidget(Widget):
    def __init__(self, native_widget, **kwargs):
        super(AndroidWidget, self).__init__(**kwargs)
        self.native_widget = native_widget
        self.layout = LinearLayout(PythonActivity.mActivity)
        self.layout.addView(self.native_widget, LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT))
        PythonActivity.mActivity.addContentView(self.layout, LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT))
        self.bind(pos=self.update_size, size=self.update_size)

    def update_size(self, *args):
        pass

    def on_parent(self, widget, parent):
        if not parent and hasattr(self, 'layout'):
            window = PythonActivity.mActivity.getWindow()
            window.getDecorView().findViewById(android.R.id.content).removeView(self.layout)