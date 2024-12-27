from gi.repository import GObject, Gtk, Gedit

class CharacterCountPlugin(GObject.Object, Gedit.ViewActivatable):
    __gtype_name__ = "SelectionCharacterCountPlugin"
    view = GObject.Property(type=Gedit.View)

    def __init__(self):
        GObject.Object.__init__(self)
        self._status_label = None

    def do_activate(self):
        self._insert_status_label()
        self.view.connect("notify::selection-bound", self._update_character_count)
        self.view.get_buffer().connect("notify::cursor-position", self._update_character_count)

    def do_deactivate(self):
        if self._status_label:
            status_bar = self.view.get_toplevel().get_statusbar()
            status_bar.remove(self._status_label)
            self._status_label = None

    def do_update_state(self):
        self._update_character_count()

    def _insert_status_label(self):
        status_bar = self.view.get_toplevel().get_statusbar()
        if not self._status_label:
            self._status_label = Gtk.Label(label="Selection Character Count")
            self._status_label.set_margin_start(20)  # 20px left margin
            self._status_label.set_margin_end(20)    # 20px right margin
            status_bar.pack_end(self._status_label, expand=False, fill=False, padding=0)
            status_bar.show_all()

    def _update_character_count(self, *args):
        buffer = self.view.get_buffer()
        if buffer:
            if buffer.get_has_selection():
                start, end = buffer.get_selection_bounds()
                selected_text = buffer.get_text(start, end, True)
                char_count = len(selected_text)
            else:
                char_count = 0
            self._status_label.set_text(f"SCC: {char_count}")
