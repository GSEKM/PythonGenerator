
# cells = sheet['A1': 'B6']

# for c1, c2 in cells:
#     print("{0:8} {1:8}".format(c1.value, c2.value))

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# import openpyxl
# book = openpyxl.load_workbook('./new/ia.xlsx')
# sheet = book.active

# cells = sheet['A1': 'B6']

# for c1, c2 in cells:
#     print("{0:8} {1:8}".format(c1.value, c2.value))


class ComboBoxWindow(Gtk.Window):



    def __init__(self):
        Gtk.Window.__init__(self, title="IA")

        self.set_border_width(10)


        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        hbox = Gtk.Box(spacing=6)
        self.add(vbox)


        label = Gtk.Label("Entrada do caso problema:")
        vbox.pack_start(label, True, True, 0)
        label = Gtk.Label("Atributos:")
        vbox.pack_start(label, True, True, 0)

        country_store = Gtk.ListStore(str)
        countries = ["Austria", "Brazil", "Belgium", "France", "Germany",
            "Switzerland", "United Kingdom", "United States of America",
            "Uruguay"]
        for country in countries:
            country_store.append([country])

        country_combo = Gtk.ComboBox.new_with_model(country_store)
        country_combo.connect("changed", self.on_country_combo_changed)
        renderer_text = Gtk.CellRendererText()
        country_combo.pack_start(renderer_text, True)
        country_combo.add_attribute(renderer_text, "text", 0)
        vbox.pack_start(country_combo, False, False, True)


        vbox.add(hbox)



        button = Gtk.Button.new_with_mnemonic("_Fechar")
        button.connect("clicked", self.on_close_clicked)
        hbox.pack_start(button, True, True, 0)

        button = Gtk.Button.new_with_label("Continuar")
        button.connect("clicked", self.on_click_me_clicked)
        hbox.pack_start(button, True, True, 0)

    def on_click_me_clicked(self, button):
        print("\"Click me\" button was clicked")

    def on_close_clicked(self, button):
        print("Closing application")
        Gtk.main_quit()

    
    def on_country_combo_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            country = model[tree_iter][0]
            print("Selected: country=%s" % country)



win = ComboBoxWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()