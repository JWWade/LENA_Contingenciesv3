"""
The MIT License (MIT)
Copyright (c) 2018 Paul Yoder, Joshua Wade, Kenneth Bailey, Mena Sargios, Joseph Hull, Loraina Lampley, John Peden, Bishoy Boktor, Kate Lovett, Joel Norris, Joseph London, Jesse Offei-nkansah

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import xml.etree.ElementTree as ET
from copy import deepcopy
import os
import csv
import pandas as pd
import threading
import Queue
from Helpers import *
import math

# Event Item
class EItem:
	def __init__(self, attr):
		self.spkr = attr["spkr"]
		self.onset = attr["startTime"]
		self.offset = attr["endTime"]
		#print self.spkr

	def GetFloatTime(self,arg='onset'):
		t = self.onset[2:-1] if arg=='onset' else self.offset[2:-1]
		return float(t)

class EItemCSV:
	def __init__(self, data):
		self.spkr = data[2]
		self.onset = data[0]
		self.offset = data[1]
		#print self.spkr

	def GetFloatTimeCSV(self, arg='onset'):
		t = self.onset[2:-1] if arg=='onset' else self.offset[2:-1]
		return float(t)

# Event Item List
class EItemList:
	def __init__(self, _varMap={}, pid=0, its_filename=''):
		self.list = []
		self.list_ = []
		self._varMap = _varMap
		self.seqType = self._varMap["seqType"]
		self.pid = pid
		self.its_filename = its_filename
		self.relevantSpkrs = self._varMap["A"]+','+self._varMap["B"]+','+self._varMap["C"]+',Pause'
		self.pauseDur = float(self._varMap["PauseDur"])
		self.eventCnt = {"A":0,"B":0,"C":0,"P":0}
		self.evTypes = ["A","B","C","P"]
		self.contingencies = {"a":0, "b":0, "c":0, "d":0}
		self.round = True if "True" in self._varMap["roundingEnabled"] else False

	def AddEItem(self, seg, flag=None):
		# Specify CHN events as either CHNSP or CHNNSP events
		if 'CHN' in seg.attrib["spkr"]:
			seg.attrib["spkr"] = self.Modify_CHN_Events(seg)

		# Handle first and last events in .its file if they aren't relevant speakers
		if (flag is 'Initial' or flag is 'Terminal') and seg.attrib["spkr"] not in self.relevantSpkrs:
			seg.attrib["spkr"]="Pause"
		if seg.attrib["spkr"] in self.relevantSpkrs:
			self.list.append( EItem(seg.attrib) )

	def AddEItemCSV(self, data_array, flag=None):
		#print 'This is csv stuff'

		if(flag is 'Initial' or flag is 'Terminal') and data_array[2] not in self.relevantSpkrs:
			data_array[2] = "Pause"
		if data_array[2] in self.relevantSpkrs:
			self.list.append( EItemCSV(data_array) )

	def Modify_CHN_Events(self, seg):
		CHN_mod = ''
		if 'startUtt1' in seg.attrib:
			CHN_mod = 'CHNSP'
		else:
			CHN_mod = 'CHNNSP'
		return CHN_mod

	def Size(self):
		return len(self.list)

	def GetItem(self, index):
		return self.list[index]

	def InsertPauses(self):
		self.list_.append(deepcopy(self.list[0]))
		for i in range(1,self.Size()):
			#determine whether to add pause before copying event
			curEvT = self.list[i].GetFloatTime('onset')
			preEvT = self.list[i-1].GetFloatTime('offset')
			eT = curEvT - preEvT
			P = self.pauseDur
			if eT >= P:
				# calculate number of pauses to insert
				numP = 0
				if self.round is True:
					try:
						numP = int( (eT / P) + .5 )
					except ZeroDivisionError:
						numP = int( (0) + .5)
				else:
					try:
						numP = int( (float(eT) / float(P)) )
					except ZeroDivisionError:
						numP = int((0) + .5)

				for j in range(0,numP):
					# insert pause
					startTime = preEvT+(j*P)
					endTime = min(curEvT,startTime+P)
					pAttr = {"spkr":"Pause","startTime":str(startTime),"endTime":str(endTime)}
					self.list_.append( EItem(pAttr) )
			#add current event
			self.list_.append( deepcopy(self.list[i]) )

		#free memory used by interim list
		self.list = deepcopy(self.list_)
		self.list_ = None

	def InsertPausesCSV(self):
		self.list_.append(deepcopy(self.list[0]))
		#print(self.Size())
		#print(self.list[0].startTime)
		for i in range(1,self.Size()):
			print 'Before GetFloatTime'
			#determine whether to add pause before copying event
			curEvT = self.list[i].GetFloatTimeCSV('onset')
			preEvT = self.list[i-1].GetFloatTimeCSV('offset')

			print 'After GetFloatTime'
			eT = curEvT - preEvT
			P = self.pauseDur
			if eT >= P:
				# calculate number of pauses to insert
				numP = 0
				if self.round is True:
					try:
						numP = int( (eT / P) + .5 )
					except ZeroDivisionError:
						numP = int( (0) + .5)
				else:
					try:
						numP = int( (float(eT) / float(P)) )
					except ZeroDivisionError:
						numP = int((0) + .5)

				for j in range(0,numP):
					# insert pause
					startTime = preEvT+(j*P)
					endTime = min(curEvT,startTime+P)
					pAttr = []
					pAttr.append(startTime)
					pAttr.append(endTime)
					pAttr.append("Pause")
					#pAttr = {"spkr":"Pause","startTime":str(startTime),"endTime":str(endTime)}
					print 'Do we make it here successfully?'
					self.list_.append( EItemCSV(pAttr) )
			#add current event
			self.list_.append( deepcopy(self.list[i]) )
		print 'What about here yo?'
		#free memory used by interim list
		self.list = deepcopy(self.list_)
		self.list_ = None

	def TallyItems(self):
		for i in range(0, self.Size()): # iterate over Event Items
			for e in self.evTypes:			
				if self.list[i].spkr in self._varMap[e]:
					self.eventCnt[e] += 1

	def SeqAn(self):
		numItems = self.Size()
		# A-->B
		if self._varMap['seqType'] == 'A_B':
			print 'A-->B Analysis in progress...'
			# iterate over event items
			for i in range(0, numItems-1):
				curr = self.list[i]
				next = self.list[i+1]
				if curr.spkr in self._varMap["A"] and next.spkr in self._varMap["B"]:
					self.contingencies["a"] += 1
				elif curr.spkr in self._varMap["A"] and next.spkr not in self._varMap["B"]:
					self.contingencies["b"] += 1
				elif curr.spkr not in self._varMap["A"] and next.spkr in self._varMap["B"]:
					self.contingencies["c"] += 1
				elif curr.spkr not in self._varMap["A"] and next.spkr not in self._varMap["B"]:
					self.contingencies["d"] += 1
		# (A-->B)-->C
		elif self._varMap['seqType'] == 'AB_C':
			print '(A-->B)-->C Analysis in progress...'
			# iterate over event items
			for i in range(0, numItems-2):
				curr = self.list[i]
				nextB = self.list[i+1]
				nextC = self.list[i+2]
				if curr.spkr in self._varMap["A"] and nextB.spkr in self._varMap["B"] and nextC.spkr in self._varMap["C"]:
					self.contingencies["a"] += 1
				elif curr.spkr in self._varMap["A"] and nextB.spkr in self._varMap["B"] and nextC.spkr not in self._varMap["C"]:
					self.contingencies["b"] += 1
				elif not(curr.spkr in self._varMap["A"] and nextB.spkr in self._varMap["B"]) and nextC.spkr in self._varMap["C"]:
					self.contingencies["c"] += 1
				elif not(curr.spkr in self._varMap["A"] and nextB.spkr in self._varMap["B"]) and nextC.spkr not in self._varMap["C"]:
					self.contingencies["d"] += 1

	def Header(self):
		# Subject ID
		h = 'PID,its_filename,'
		
		# Event Counts
		for e in self.evTypes:
			h += self._varMap[e].replace(",","+") + ','

		# Contingencies
		h += 'a,b,c,d,OCV'
		return h

	def ResultsTuple(self):
		# Subject ID
		rt = self.pid + ',' + self.its_filename.split('/')[-1] + ','

		# Event Counts
		for e in self.evTypes:
			rt += str(self.eventCnt[e]) + ','

		# Contingencies
		# tokens used for OCV computation
		tok_a = float(self.contingencies["a"])
		tok_b = float(self.contingencies["b"])
		tok_c = float(self.contingencies["c"])
		tok_d = float(self.contingencies["d"])

		# OCV operant contingency value
		OCV = (tok_a / (tok_a + tok_b)) - (tok_c / (tok_c + tok_d))

		rt += str(self.contingencies["a"]) + ',' + str(self.contingencies["b"]) + ',' + str(self.contingencies["c"]) + ',' + str(self.contingencies["d"]) + ',' + str(OCV)
		return rt
	
class SeqAnalysis:
	def __init__(self, seqData, out_results, stopper):

		# extract items from seqData object
		self.varMap = seqData.seq_config

		# prime for writing output
		batch_single = None
		if len(seqData.its_dict) > 1:
			batch_single = "Batch"
		else:
			batch_single = "Single"

		# setup vars
		self.results = []
		self.out_results = out_results
		self.error_results = []
		self.stopper = stopper
		self.tLock = threading.Lock()

		# kick off threads in batch
		while len(seqData.its_dict) > 0:
			# prep for run
			tempItem = {}
			tempDict = {}
			threads = []
			for i in range(seqData.num_threads):
				try:
					tempItem = seqData.its_dict.popitem()
					tempDict.update({tempItem[0]:tempItem[1]})
				except KeyError:
					pass # dict is empty
			
			# perform run
			for k,v in tempDict.iteritems():
				t = threading.Thread(target=self.Perform, args=(k,v,))
				t.daemon = True
				threads.append(t)
				t.start()

			# wait for threads
			for thread in threads:
				thread.join()

		if not stopper.is_set():
			# write output
			output_data = OutData(batch_single, seqData.seq_config,self.results)
			if '.xlsx' in seqData.output_format:
				output_xlsx(output_data)
			if '.csv' in seqData.output_format:
				output_csv(output_data)
			if '.txt' in seqData.output_format:
				ouput_txt(output_data)

			# report analysis result
			if len(self.error_results) > 0:
				self.out_results.append("Failed Sequence Analysis!")
			else:
				self.out_results.append("Successfully Sequence Analysis!")


	def Perform(self, pID, path):
		# retrieve work items from queue
		if not self.stopper.is_set():
			try:
				# Announce
				print 'Analysis in progress on pID=' + str(pID) + ', file=' + path

				# Define necessary objects
				eiList = None
				tree = None

				# INITIALIZE ESSENTIAL OBJECTS
				#Init event item list
				eiList = EItemList(_varMap=self.varMap, pid=pID, its_filename=path)
				
				if os.path.splitext(path)[1] == '.csv':
					#csv_data = list(csv.reader(open(path)))
					df = pd.read_csv(path)
					csv_data = df.values.tolist()
					
					print pd.DataFrame(csv_data)

					csv_arr = []
					csv_arr.append(str(csv_data[0][0]))
					csv_arr.append(str(csv_data[0][1]))
					csv_arr.append(str(csv_data[0][2]))
					#print(csv_arr)
					#print(csv_data[0][1])

					#print(csv_arr[0])
					#print(csv_arr[1])
					#print(csv_arr[2])
					eiList.AddEItemCSV(csv_arr, flag='Initial')
					for i in range(2, len(csv_data) - 1):
						csv_arr[0] = str(csv_data[i][0])
						csv_arr[1] = str(csv_data[i][1])
						csv_arr[2] = str(csv_data[i][2])
						eiList.AddEItemCSV(csv_arr)
					csv_arr[0] = str(csv_data[-1][0])
					csv_arr[1] = str(csv_data[-1][1])
					csv_arr[2] = str(csv_data[-1][2])
					eiList.AddEItemCSV(csv_arr, flag='Terminal')

					eiList.InsertPausesCSV()
				else:
					#Load xml tree
					tree = ET.parse(path)

					#Get access to only the conversational segments in the .its file
					recNode = tree.find("ProcessingUnit")
					segs = list(recNode.iter("Segment"))

					# iterate over segments and copy
					eiList.AddEItem( segs[0], flag='Initial' )
					for i in range(1, len(segs)-1):
						eiList.AddEItem( segs[i] )
					eiList.AddEItem( segs[-1], flag='Terminal' )

					# free memory used by xml tree
					tree = None
					eiList.InsertPauses()
				
				#Insert contiguous pauses
				

				print 'Made it past InsertPauses()'
				#Tally each item in the EItemList
				eiList.TallyItems()

				print 'Made it past TallyItems()'
				#Perform primary analysis
				eiList.SeqAn()

				#write data and break from loop
				elh = eiList.Header()
				outputContent = ""
				with self.tLock:
					if len(self.results) == 0:
						self.results.append(elh)

				outputContent += eiList.ResultsTuple()

				# write data with Lock on results
				with self.tLock:
					self.results.append(outputContent)

			# Log All Errors
			except Exception as e:
				with self.tLock:
					self.error_results.append(str(e))