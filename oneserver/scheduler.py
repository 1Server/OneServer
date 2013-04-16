from datetime import datetime, timedelta
import threading
import time
from heapq import heappush,heappop

##
# The different states that the task can be in. States should
# not be set manually. They should only be set by the scheduler.
class TaskState:
	##
	# Either unscheduled or scheduled and waiting to be run.
	PENDING = 0

	##
	# When the task is running.
	RUNNING = 1

	##
	# The task has finished executing.
	FINISHED = 2

##
# A task is a unit of work that is to be performed on behalf
# of another part of the server or for a plugin. A task is
# scheduled to run at some point in the future and can be
# set to be a recurring event that happens at an interval.
#
# There are two methods to create a task. The first is to
# implement the ITask interface. The benefit to doing that is
# that the task can have more specialized funtionality and
# can be given more data to use for processing.
#
# The second method is to instantiate the interface and just pass
# some settings as well as a function to call when the task
# is run.
class ITask(object):
	##
	# Creates a task with the given time before its called 
	# and performs the requested action when called. The task
	# can also b e set to repeat itself at the same delay
	# interval.
	#
	# @param task the task to perform when called 
	# @param minutes the number of minutes to wait (default 0)
	# @param hours the number of hours to wait (default 0)
	# @param days the number of days to wait (default 0)
	# @param recurring if the task is to repeat itself
	#
	# @return the task object that was created
	@staticmethod
	def createTask(task, minutes = 1, hours = 0, days = 0, recurring = False):
		if task == None or not hasattr(task, '__call__'):
			raise TypeError('A function must be given to create a task.')

		if not issubclass(minutes.__class__, int) or not issubclass(hours.__class__, int) or not issubclass(days.__class__, int):
			raise TypeError('The time given must be in an integer form.')

		ret = ITask(minutes, hours, days, recurring)

		ret.run = task

		return ret

	##
	# Creates a task with the given time before its called.
	# The task can also be set to repeat itself at the same
	# delay interval.
	#
	# @param minutes the number of minutes to wait (default 0)
	# @param hours the number of hours to wait (default 0)
	# @param days the number of days to wait (default 0)
	# @param recurring if the task is to repeat itself
	def __init__(self, minutes = 1, hours = 0, days = 0, recurring = False):
		self.minutes = minutes
		self.hours = hours
		self.days = days
		self.recurring = recurring
		self.state = TaskState.PENDING

		self.timestamp = self.calculateTimestamp()

	##
	# Called when the task is to run. In case the task cares
	# about when it is actually being called it is provided
	# the time that it was executed at. This is given as a
	# datetime object.
	#
	# @param time the time the task was actually selected
	# to run at
	def run(self, time):
		raise NotImplementedError('Task method was not implemented.')

	##
	# Calculates the timestamp of when the task should next run.
	#
	# @return a datetime object for the next run time
	def calculateTimestamp(self):
		return datetime.now() + timedelta(minutes = self.minutes,
						  hours = self.hours,
						  days = self.days)

	##
	# Less than comparison between tasks. Based on the timestamp to next run.
	def __lt__(self, other):
		if not isinstance(other, ITask):
			raise TypeError('Can only compare ITask objects with other ITask objects')

		return self.timestamp < other.timestamp

	##
	# Less than or equal to comparison between tasks. Based on the timestamp to next run.
	def __le__(self, other):
		if not isinstance(other, ITask):
			raise TypeError('Can only compare ITask objects with other ITask objects')

		return self.timestamp <= other.timestamp

	##
	# Equal to comparison between tasks. Based on the timestamp to next run.
	def __eq__(self, other):
		if not isinstance(other, ITask):
			raise TypeError('Can only compare ITask objects with other ITask objects')

		return self.timestamp == other.timestamp

	##
	# Not equal to comparison between tasks. Based on the timestamp to next run.
	def __ne__(self, other):
		if not isinstance(other, ITask):
			raise TypeError('Can only compare ITask objects with other ITask objects')

		return self.timestamp != other.timestamp

	##
	# Greater than or equal to comparison between tasks. Based on the timestamp to next run.
	def __ge__(self, other):
		if not isinstance(other, ITask):
			raise TypeError('Can only compare ITask objects with other ITask objects')

		return self.timestamp >= other.timestamp

	##
	# Greater than comparison between tasks. Based on the timestamp to next run.
	def __gt__(self, other):
		if not isinstance(other, ITask):
			raise TypeError('Can only compare ITask objects with other ITask objects')

		return self.timestamp > other.timestamp

##
# Maximum number of threads to run tasks on
maxThreads = -1

##
# This class provides an method to run task objects given to it at a specific time.
class TaskScheduler():

	##
	# The main thread handle
	mainThread = None

	##
	# Status bool
	running = True

	##
	# Main init
	# @param maxThreads Maximum number of threads
	def __init__(self, maxNumThreads = 10):
		global maxThreads
		maxThreads = maxNumThreads
		self.taskList = []
		self.running = False

	##
	# Starts the scheduler's main thread.  
	# No tasks can be run before this method is called
	def startScheduler(self):
		if self.mainThread is not None:
			if self.mainThread.isAlive():		
				raise RuntimeError("Tried to start an already started Scheduler")
			self.mainThread = None

		self.mainThread = MainSchedulerThread(self)
		self.mainThread.start()
		self.running = True

	##
	# Stops the scheduler's main thread
	# No tasks can be run after this method is called
	def stopScheduler(self):
		if self.mainThread is None:
			raise RuntimeError("Trying to stop a None Thread")
		if not self.mainThread.isAlive():
			raise RuntimeError("Trying to stop a Thread that wasn't started")
		self.mainThread.stopThread()
		self.running = False

	##
	# Adds a task to be executed
	def addTask(self, task):
		if not self.running:
			raise RuntimeError("Tried to add a task to a stopped scheduler")
		if datetime.now() > task.timestamp:
			raise RuntimeError("Tried to schedule a task that should have already been run")
		heappush(self.taskList, task)

	##
	# Returns if the scheduler is still running
	def isAlive(self):
		return self.running

##
# This is the main thread of the TaskScheduler
class MainSchedulerThread(threading.Thread):

	##
	# Main init
	# @param A TaskScheduler to pull Tasks from
	def __init__(self, taskScheduler):
		threading.Thread.__init__(self)
		self.tasks = taskScheduler.taskList
		self.stop = False
		self.daemon = True
		global maxThreads
		self.pool = []
		for a in range(maxThreads):
			t = TaskThread()
			t.start()
			self.pool.append(t)
	
	##
	# Main method, starts checking for new tasks to run
	def run(self):
		while not self.stop:
			while True:
				if len(self.tasks) is 0:
					break

				if datetime.now() < self.tasks[0].timestamp:
					#If it should be run
					#Run it after poping
					task = heappop(self.tasks)
					global maxThreads
					for a in range(maxThreads):
						result = self.pool[a].runTask(task)
						if result:
							break #Task was added
						else:
							pass #Thread already had a task, check next
					#Check if it needs to reoccur
					if task.recurring:
						task.timestamp = task.calculateTimestamp()
						heappush(self.tasks, task)	
				else:
					break
			#After breaking, all tasks that should be run are now running or queued, sleep for 1 min
			time.sleep(60)
	
		#When we are stopping, join worker threads, they are already marked as stopped
		for a in range(maxThreads):
			self.pool[a].join()

	##
	# Stops the exectuion of the scheduler after the next task check, this call will not block
	# Call isAlive() to check for when it is stopped
	def stopThread(self):
		for a in range(maxThreads):
			self.pool[a].stopThread()
		self.stop = True


##
# This a task thread
class TaskThread(threading.Thread):

	##
	# Main init
	def __init__(self):
		threading.Thread.__init__(self)
		self.busy = False
		self.task = None
		self.stop = False
		self.daemon = True

	##
	# Runs the thread in a loop running any given task
	def run(self):
		while not self.stop:
			if self.busy: # Has task
				if self.task is None:
					self.busy = False
				else:
					self.task.state = TaskState.RUNNING
					self.task.run(datetime.now())
					self.task.state = TaskState.FINISHED
					self.task = None
			else:
				time.sleep(1)

	##
	# Runs the given task, returns False if we already have  a task
	# @param task The task to run
	def runTask(self,task):
		if self.busy:
			if self.task is not None:
				return False
		self.task = task
		self.busy = True
		return True

	##
	# Stops the TaskThread, returns a task object if one exists
	def stopThread(self):
		self.stop = True
		return self.task


