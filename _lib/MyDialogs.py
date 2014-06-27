from gi.repository import Gtk
import os

class YesCancelDialog(Gtk.Dialog):

    def __init__(self, parent,title,text):
        Gtk.Dialog.__init__(self, title, parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(150, 100)

        label = Gtk.Label(text)

        box = self.get_content_area()
        box.add(label)
        gtksettings = Gtk.Settings.get_default()
        gtksettings.props.gtk_button_images = True
        self.show_all()

class InputBox(Gtk.Dialog):

    def __init__(self, parent,title,text1,text2):
        Gtk.Dialog.__init__(self, title, parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))


        box = self.get_content_area()

        label = Gtk.Label(text1)
        box.add(label)

        self.entry = Gtk.Entry()
        self.entry.set_text(text2)
        box.add(self.entry)
        gtksettings = Gtk.Settings.get_default()
        gtksettings.props.gtk_button_images = True
        self.show_all()

class FileChoose(Gtk.FileChooserDialog):
    def __init__(self, parent,title, wheretostart,choosewhat):
        Gtk.Dialog.__init__(self, title, parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.set_action(choosewhat)
        self.set_filename(wheretostart)
        self.show_all()

class AboutBox(Gtk.AboutDialog):
    def __init__(self,APPNAME,version, window, icon, appdir,comments):
        Gtk.AboutDialog.__init__(self)
        #self.gtk_about_dialog_set_program_name(APPNAME)
        self.set_program_name(APPNAME)
        #self.gtk_about_dialog_set_version(version)
        self.set_version('v.' + version)
        self.set_license_type(Gtk.License.LGPL_3_0)
        self.set_logo(icon)
        self.set_comments(comments)
        aboutauthors = []
        with open(os.path.join(appdir,'_about','AUTHORS'),mode = 'rt') as ftxt:
            for line in ftxt:
                #get rid of the stupid new line
                #(the last one may not have a newline)
                aboutauthors.append(line[:-1] if line.endswith('\n') else line)
        self.set_authors(aboutauthors)
        #same for artists : set_artists 
        #same for documenters: set_documenters 
        ######translators are a special case
        #
        self.show_all()

if __name__ == "__main__":
    print('not usable content, if you understand me...')
