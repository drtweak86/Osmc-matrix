import xbmc, xbmcgui, time, os

VIDEO = "/home/osmc/matrix_intro.mp4"   # path to your Matrix clip
MAX_WAIT = 12.0                          # seconds to wait for playback start
PLAY_FOR = 8.0                           # seconds to play before stopping

class BootMatrix(xbmc.Monitor):
    def run(self):
        while not xbmc.getCondVisibility("Window.IsVisible(home)"):
            if self.abortRequested(): return
            time.sleep(0.25)
        time.sleep(0.6)
        if not os.path.exists(VIDEO):
            xbmc.log("[service.boot-matrix] video missing: %s" % VIDEO, xbmc.LOGWARNING)
            return
        xbmc.executebuiltin(f'PlayMedia({VIDEO})')
        p = xbmc.Player()
        t0 = time.time()
        while not p.isPlayingVideo() and (time.time() - t0) < MAX_WAIT:
            if self.abortRequested(): return
            time.sleep(0.1)
        if not p.isPlayingVideo():
            xbmc.log("[service.boot-matrix] failed to start playback", xbmc.LOGWARNING)
            return
        xbmc.executebuiltin('Action(FullScreen)')
        xbmc.executebuiltin('Action(HideOSD)')
        t0 = time.time()
        while (time.time() - t0) < PLAY_FOR:
            if self.abortRequested(): return
            time.sleep(0.1)
        try:
            p.stop()
        except:  # noqa
            pass

if __name__ == "__main__":
    BootMatrix().run()
