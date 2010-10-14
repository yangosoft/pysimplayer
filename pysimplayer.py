# -*- coding: utf-8 -*-
# pysimplayer is an example of use of pyffmpeg, pygame and alsaaudio to
# play videos with Python.

# pyffmpeg: http://code.google.com/p/pyffmpeg/
# pygame: http://www.pygame.org/
# alsaaudio: http://pyalsaaudio.sourceforge.net/


###############################################################################
#  Copyright (C) 2002-2007  Yango http://usuarios.multimania.es/sisar
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
################################################################################




from pyffmpeg import *
      
import pygame
import alsaaudio

TS_VIDEO_RGB24={ 'video1':(0, -1, {'pixel_format':PixelFormats.RGB24,'dest_width':1360, 'dest_height':768}), 'audio1':(1,-1,{})}


class AlsaSoundLazyPlayer:
    def __init__(self,rate=44100,channels=2,fps=25):
        self._rate=rate
        self._channels=channels
        self._d = alsaaudio.PCM()
        self._d.setchannels(channels)
        self._d.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        self._d.setperiodsize(int((rate*channels)//fps))
        self._d.setrate(rate)
    def push_nowait(self,stamped_buffer):
        self._d.write(stamped_buffer[0].data)




def display(p):
  pygame.surfarray.use_arraytype("numpy")
  p=p.swapaxes(0,1)
  
  pygame.surfarray.blit_array(screen,p)
  
  
  pygame.display.flip()



## create the reader object
mp=FFMpegReader()




pygame.init()

#window size
image_width=1360
image_height=768

tmpSurface=pygame.Surface((image_height,image_width))


size=(image_width,image_height) 




## open an audio-video file
mp.open("video.avi",TS_VIDEO_RGB24 )
tracks=mp.get_tracks()
screen = pygame.display.set_mode(size,pygame.DOUBLEBUF)


print "Audio sample %d Channels %d , fps %d , %s" % (tracks[1].get_samplerate(),tracks[1].get_channels(),tracks[0].get_fps(),tracks[0].get_size())

ap=AlsaSoundLazyPlayer(tracks[1].get_samplerate(),tracks[1].get_channels(),tracks[0].get_fps())
tracks[1].set_observer(ap.push_nowait)




## define a function to be called back each time a frame is read...
def obs(f):
  display(f) 

tracks[0].set_observer(obs)

mp.run()