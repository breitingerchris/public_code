import wx
import os

class MainWin(wx.Frame):

    def __init__(self, parent, title):
        """ Init """
        wx.Frame.__init__(self, parent, title=title, size=(300, 200))
        vbox = wx.BoxSizer(wx.VERTICAL)
        startButton = wx.Button(self, label='Start!')
        vbox.Add(startButton)
        self.SetSizer(vbox)
        self.Show(True)

    def OnOpen(self, e):
        """ Open a file """
        self.dirname = ''
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            f = open(os.path.join(self.dirname, self.filename), 'r')
            self.control.SetValue(f.read())
            f.close()
        dlg.Destroy()


def main():
    app = wx.App(False)
    frame = MainWin(None, "Furz Reddit Suite")
    frame.Show(True)
    app.MainLoop()

if __name__ == '__main__':
    main()