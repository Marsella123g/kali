from kivy.uix.checkbox import CheckBox
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineListItem
from plyer import filechooser
from kivy.clock import Clock
import pandas as pd
from matplotlib import pyplot as plt
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
Window.size=(1000,600)
graph_name="Line Chart"
class Image_btn(ButtonBehavior, Image):
    pass
class Setting_Window(MDBoxLayout):
    def graph_switching(self, checkbox, default, graph_name):
        if checkbox.active:
            checkbox.active=False
            default.active=True
            graph_name="Line Chart"
            #print("False")
        else:
            default.active = False
            graph_name=graph_name
            checkbox.active=True
            #print("True")
        print(graph_name)
class Interface(BoxLayout):
    def binder(self,checkbox,value):
        if value:
            print(self.obj_dict[checkbox]," added")
        else:
            print(self.obj_dict[checkbox], " removed")
    def uploader(self, dt):
        self.obj_dict=dict()
        self.column_dict=dict()
        self.files_address=dict()
        self.files = filechooser.open_file(title="Choose csv files", filters=[("*.csv")], multiple=True)
        for file in self.files:
            file_name=file.split("\\")[-1]
            self.files_address[file_name]=file
            box=BoxLayout(size_hint_y=None,height=50,padding=[30,0,0,0])
            checkbox=CheckBox(size_hint_x=.25,background_checkbox_normal="checkbox_nor.png",background_checkbox_down="checkbox_tic.png")
            checkbox.bind(active=self.binder)
            label=Label(text=f"[color=#3f51b5]{file_name}[/color]",markup=True)
            box.add_widget(checkbox)
            box.add_widget(label)
            self.ids.file_placeholder.add_widget(box)
            self.obj_dict[checkbox]=file_name

        columns=pd.read_csv(self.files[0]).columns.values.tolist()
        for column in columns:
            box = BoxLayout(size_hint_y=None, height=50, padding=[30, 0, 0, 0])
            checkbox = CheckBox(size_hint_x=.25, background_checkbox_normal="checkbox_nor.png",
                                background_checkbox_down="checkbox_tic.png")
            label = Label(text=f"[color=#3f51b5]{column}[/color]", markup=True)
            box.add_widget(checkbox)
            box.add_widget(label)
            self.ids.property_placeholder.add_widget(box)
            self.column_dict[checkbox]=column

        self.ids.upload_btn.source = "Drag.png"
    def new_update(self):
        files_checkbox = self.obj_dict.keys()
        properties_checkbox = self.column_dict.keys()
        children = self.ids.graph_placeholder.children
        plt.close('all')
        plt.clf()
        if children:
            self.ids.graph_placeholder.clear_widgets()
        for file in files_checkbox:
            if file.active:
                y_axis = list()
                legend_names = list()
                file_name = self.obj_dict[file]
                file_address = self.files_address[file_name]
                plt.figure(str(file))
                plt.title(file_name)
                plt.grid(True)
                plt.ylabel("Item(s)")
                content = pd.read_csv(file_address)
                for property_checkbox in properties_checkbox:
                    if property_checkbox.active:
                        if self.column_dict[property_checkbox]=="Time" or self.column_dict[property_checkbox]=="dtime" or self.column_dict[property_checkbox]=="time":
                            x_axis=content[self.column_dict[property_checkbox]]
                        else:
                            legend_names.append(self.column_dict[property_checkbox])
                            y_axis.append(content[self.column_dict[property_checkbox]])

                for index,y in enumerate(y_axis):
                    plt.plot(x_axis.to_numpy(),y.to_numpy(), label=legend_names[index])

                box=BoxLayout(size_hint=(1,None),height=500)
                plt.legend()
                plt.gcf().autofmt_xdate()
                box.add_widget(FigureCanvasKivyAgg(plt.gcf()))
                self.ids.graph_placeholder.add_widget(box)

    def upload_menu(self):
        self.ids.upload_btn.source="Drop.png"
        Clock.schedule_once(self.uploader)
    def switching(self):
        self.ids.sm.current="visualizer_window"
    def saving(self):
        dir=filechooser.choose_dir(title="Please Select A Location")
        flag=False
        for i in plt.get_fignums():
            if flag==True:
                plt.savefig(dir[0]+f"\\Figure{i-1}.png")
            flag=True
    def setting_menu(self):
        self.dialog_box=MDDialog(title="Settings", type="custom", content_cls=Setting_Window())
        self.dialog_box.open()

class VisualizerApp(MDApp):
    pass

VisualizerApp().run()
