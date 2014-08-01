




import os
import glob
import subprocess
 
inpath = '/media/data4/Media/Serien/Two and a Half Men/'
outpath = '/media/data4/temp2/'
for f in glob.glob( os.path.join(inpath, '*.*') ):
    infile = f
    outfile = f[len(inpath):]
    outfile = outpath + outfile[:-3] + 'mp3'
    subprocess.call(["avconv", "-i", infile, "-ac", "1", "-ar", "32000", "-aq", "8", "-ab", "96k", "-vn", outfile])


#subprocess.call(["avconv", "-i", "/media/data4/Media/Serien/The Big Bang Theory/The Big Bang Theory - 1x01 - Pilot.avi", "-ac", "1", "-ar", "32000", "-aq", "8", "-ab", "96k", "-vn", "audio.mp3"])
#avconv -i The\ Big\ Bang\ Theory\ -\ 1x01\ -\ Pilot.avi -ac 1 -ar 32000 -aq 8 -ab 96k -vn audio.mp3


