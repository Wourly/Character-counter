import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class MyWindow(Gtk.Window):

    cc = 0 #characters count
    wc = 0 #word count
    sc = 0 #sentence count
    rc = 0 #row count
    nc = 0 #number count
    ns = 0 #numbers sum

    ct = 'c' #current type
    lt = 'c' #last type

    wf = 0 #word flag
    nf = 0 #number flag
    sf = 0 #sentence flag
    rf = 0 #row flag

    tn = 0 #temporary number

    bs = 0 #buffer starter

    separator = "#####" #separates files and textarea field

    sl = len(separator) #length of separator
    su = 0 #how many times was separator used (depends on number of files)

    def __init__(self):
        
        Gtk.Window.__init__(self, title="Counter")

        headline = Gtk.Label()
        headline.set_markup("<span font='Tahoma 30' underline='low'>Character counter</span>")

        textview_label = Gtk.Label()
        textview_label.set_markup("<span font='15'><i>Text box</i></span>")
        self.textview = Gtk.TextView()
        textview_scroll = Gtk.ScrolledWindow()
        textview_scroll.add(self.textview)

        filechooser_label = Gtk.Label()
        filechooser_label.set_markup("<span font='15'><i>Choose file(s)</i></span>")
        filechooser_scroll = Gtk.ScrolledWindow()

        self.fbutton1 = Gtk.FileChooserButton()
        self.fbutton2 = Gtk.FileChooserButton()
        self.fbutton3 = Gtk.FileChooserButton()
        self.fbutton4 = Gtk.FileChooserButton()
        self.fbutton5 = Gtk.FileChooserButton()
        self.fbutton6 = Gtk.FileChooserButton()

        filechooser_grid = Gtk.Grid(column_homogeneous=True, row_homogeneous=True)

        filechooser_grid.attach(self.fbutton1,0,0,1,1)
        filechooser_grid.attach(self.fbutton2,0,1,1,1)
        filechooser_grid.attach(self.fbutton3,0,2,1,1)
        filechooser_grid.attach(self.fbutton4,0,3,1,1)
        filechooser_grid.attach(self.fbutton5,0,4,1,1)
        filechooser_grid.attach(self.fbutton6,0,5,1,1)

        filechooser_scroll.add(filechooser_grid)
        
        counter_button = Gtk.Button(label = "COUNT")
        counter_button.connect("clicked", self.counter)

        grid = Gtk.Grid(column_homogeneous=True, row_homogeneous=True)

        grid.attach(headline, 0, 0, 5, 1)
        grid.attach(textview_label, 0, 1, 5, 1)
        grid.attach(textview_scroll, 0, 2, 5, 5)
        grid.attach(filechooser_label, 5, 0, 3, 1)
        grid.attach(filechooser_scroll, 5, 1, 3, 6)
        grid.attach(counter_button, 0, 7, 8, 1)

        self.add(grid)

        self.counts = []

        self.textview.get_buffer()


    def get_buff (self, widget):
        
        buffer = widget.get_buffer()

        return buffer.get_slice(buffer.get_start_iter(), buffer.get_end_iter(), True)

    def get_str_from_buttons (self):

        barray = [self.fbutton1, self.fbutton2, self.fbutton3, self.fbutton4, self.fbutton5, self.fbutton6]

        string_array = []

        for button in barray:

            file_name = button.get_filename()

            if (file_name != None):

                string_array.append(open(file_name, 'r').read())

        #if (len(string_array) > 1):
            #self.cc -= self.sl * (len(string_array) - 1)
            #print(len(string_array))
            #print(self.sl * (len(string_array) - 1))

        self.su += len(string_array) - 1

        #print(sl * self.len(string_array))

        #print(len(string_array))

        #print(self.separator.join(string_array))

        return self.separator.join(string_array)

    def is_punct (self, char):

        for c in "!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~":
            if (c == char):
                return True

    def text_processor (self, text):

        for c in text:
            self.cc += 1

            self.lt = self.ct

            #print(c)

            #type check
            if (c.isdigit() and self.wf == 0): #is number

                self.ct = 'n'

            elif (c == '.' or c == '!' or c == '?'): #might be end of sentence (checks flag later)
            
                self.ct = 'e'
            
            elif (c == '\n'): #might be a row (checks flag later)
            
                self.ct = 'l'
            
            elif (c.isspace() or self.is_punct(c)): #type change is needed to close number reading

                self.ct = 's'

            elif (c == '#'): #file and textarea separator detection
            
                self.ct = 'm'

            #print("cc:\t{}bs:\t{}".format(c, self.bs))

            if (self.ct == 'm'):

                self.bs += 1

            if (self.bs == 5):

                #print("=======================================")
                self.apply_buffer()
                self.bs = 0


            elif (self.ct != 'm'):
                #print("-------")
                self.bs = 0


            #word mark
            if (not c.isalnum() and self.wf == 1): #if word started already (word flag is ON), word continues even with digits...
            
                self.wf = 0
                self.wc += 1
            
            elif (c.isalpha() and self.wf == 0 and self.lt != 'n'): #...but first we check if it has started with alpha character (word flag is OFF), and there was no number before, we also set flags for potential row or sentence
            
                self.ct = 'w'
                self.rf = 1 #enough to be row
                self.wf = 1 #enough to be word
                #print("wf on")
                self.sf = 1 #enough to be sentence
            
            elif (c.isalpha()): #//...but there may also be just an alpha char, that we do not wanna use as number later
            
                self.ct = 'c'

            #number processing           
            if (self.ct == 'n' and self.nf == 0): #first digit of number (number flag is OFF)
            
                self.tn = int(c)
                self.nf = 1 #is a number from now
                self.rf = 1 #is enough to be a row
            
            elif (self.ct == 'n' and self.nf == 1): #there was a digit before (number flag is ON) 
            
                self.tn = self.tn * 10 + int(c)
            
            if (self.ct != 'n' and self.lt == 'n'): #there is an end of a number, we want to add it from buffer to sum
            
                self.nc += 1
                self.ns += self.tn
                self.tn = 0
                self.nf = 0
            

            if (self.ct == 'e' and self.sf == 1): #is this an end of sentence?
            
                self.sf = 0
                self.sc += 1
            

            if (self.ct == 'l' and self.rf == 1): #is this a valid row?
            
                self.rc +=1
                self.rf = 0

            #print("c:\t{}\tbs:\t{}\n".format(c, self.bs))

            #file and textarea separator detection
            
            #print("{}\n".format(c))

    def apply_buffer(self):

        #print("buff_up")

        if (self.wf != 0):
        
            self.wf = 0
            self.wc += 1

        if (self.nf != 0):
        
            self.nf = 0
            self.nc += 1
            self.ns += self.tn        

        if (self.sf != 0):
        
            self.sf = 0
            self.sc +=1       

        if (self.rf != 0):
        
            self.rf = 0
            self.rc += 1
        
    def clear_count(self):

            self.cc = 0
            self.wc = 0
            self.sc = 0
            self.rc = 0
            self.nc = 0
            self.ns = 0

            self.ct = 'c'
            self.lt = 'c'

            self.wf = 0
            self.nf = 0
            self.sf = 0
            self.rf = 0

            self.tn = 0

    def counter (self, widget):

        text_area_text = self.get_buff(self.textview)
        files_text = self.get_str_from_buttons()

        text = text_area_text + self.separator + files_text

        #print(text)

        self.su += 1

        self.cc -= self.su * self.sl

        self.su = 0

        #print(self.su)

        self.text_processor(text)
        self.apply_buffer()

        dialog = self.Dialog(self)
        response = dialog.run()

        dialog.destroy()

        self.clear_count()

    class Dialog(Gtk.Dialog):

        def __init__(self, parent):
            Gtk.Dialog.__init__(self, "Character count", parent, 0)

            label = Gtk.Label()
            label.set_markup("<span font='Tahoma 20' underline='low'>Character count</span>")

            chars = Gtk.Label(label = "characters:")
            nchars = Gtk.Label(label = parent.cc)

            words = Gtk.Label(label = "words:")
            nwords = Gtk.Label(label = parent.wc)

            sentences = Gtk.Label(label = "sentences:")
            nsentences = Gtk.Label(label = parent.sc)

            rows = Gtk.Label(label = "rows:")
            nrows = Gtk.Label(label = parent.rc)

            numbers = Gtk.Label(label = "numbers:")
            nnumbers = Gtk.Label(label = parent.nc)

            num_sum = Gtk.Label(label = "number sum:")
            nnum_sum = Gtk.Label(label = parent.ns)

            grid = Gtk.Grid(column_homogeneous=True, row_homogeneous=True)

            grid.attach(label,0,0,2,1)

            grid.attach(chars,0,1,1,1)
            grid.attach(nchars,1,1,1,1)

            grid.attach(words,0,2,1,1)
            grid.attach(nwords,1,2,1,1)

            grid.attach(sentences,0,3,1,1)
            grid.attach(nsentences,1,3,1,1)

            grid.attach(rows,0,4,1,1)
            grid.attach(nrows,1,4,1,1)

            grid.attach(numbers,0,5,1,1)
            grid.attach(nnumbers,1,5,1,1)

            grid.attach(num_sum,0,6,1,1)
            grid.attach(nnum_sum,1,6,1,1)

            box = self.get_content_area()
            box.add(grid)
            self.show_all()



win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()