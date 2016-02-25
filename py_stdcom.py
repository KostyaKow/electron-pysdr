#!/usr/bin/env python

from pycloak.events import Event
from pycloak.threadutils import EzThread
import json, sys, time, threading

def err(msg):
   sys.stderr.write('\npy err: %s\n' % msg)
   sys.stderr.flush()


class ElectronTalker:
   def __init__(self, msg_handler = None):
      self._stop = False
      self.on_msg = Event()
      if msg_handler is not None:
         self.on_msg += msg_handler

      self.t = EzThread(self.reader_thread).thread

   def read_json(self):
      data = None
      try:
         line = sys.stdin.readline()
         if line:
            data = line.strip()
      except:
         pass
      return json.loads(data)

   def reader_thread(self):
      while not self._stop:
         time.sleep(0.05)
         msg = self.read_json()
         self.on_msg(msg)

   def send_json(self, data):
      data['magic'] = 'gentoo_sicp_rms'
      json_data = json.dumps(data)

      if json_data.find('\n') != -1:
         err('we have a newline')

      #err(json_data)
      #sys.stdout.flush()
      sys.stdout.write("%s\n" % json_data)
      sys.stdout.flush()

   def send_cmd(self, action, value):
      cmd = { 'action': action, 'value': value }
      self.send_json(cmd)

   def stop(self):
      self._stop = True

import sys, os
def set_stdout_buff_size(size):
        sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', size)
set_stdout_buff_size(1)

from rtlsdr import RtlSdr
def get_sdr():
	sdr = RtlSdr()

	#configure device
	#sdr.sample_rate = 2.048e6 	#Hz
	#sdr.center_freq = 70e6		#Hz
	#sdr.freq_correction = 60	# PPM
	#sdr.gain = 'auto'
	sdr.sample_rate = 200000
	sdr.center_freq = 907 * 1000 * 1000
	sdr.freq_correction = 60	# PPM
	sdr.gain = 'auto'

	return sdr

sdr = get_sdr()
e = ElectronTalker(lambda msg: err(msg))
i = 0

def check(n):
	if n.real > 1 or n.real < -1:
		err('bad real')
	if n.imag > 1 or n.imag < -1:
		err('bad imag')

while i < 1000:
	sampleComplex = sdr.read_samples() #(512)
	sample = []
	for n in sampleComplex:
		sample.append([n.imag, n.real])
		#check(n)
	e.send_cmd('test', sample)
	time.sleep(0.03)
	i+=1

##############

#def get_version():
#   return 0
#
#def show_section(e, section):
#   e.send_cmd('show_section', section)
#
#def progress(e, progress):
#   #console_log(curr + ' ' + total)
#   percent = curr/total * 100
#   e.send_cmd('progress', percent)
#
#def testProgress():
#   e = ElectronTalker(lambda msg: console_log(msg))
#
#   def update_progress():
#      i = 0
#      while i < 50:
#         time.sleep(0.1)
#         i = i+0.5
#         #e.send_json({ 'action':'progress', 'value': i })
#   ez = EzThread(update_progress)
#   ez.t.join()
#   e.t.join()
#
#if __name__ == '__main__':
#   testProgress()

