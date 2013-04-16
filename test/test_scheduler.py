import unittest

from oneserver.scheduler import *

##
# Tests the ITask interface part of the scheduler system.
class TestITask(unittest.TestCase):
	##
	# Basic setup that happens before every test.
	def setUp(self):
		import time
		self.smaller = ITask.createTask(testFunc)
		time.sleep(2)
		self.larger  = ITask.createTask(testFunc)


	##
	# Tests that the factory method creates a task with
	# the given parameters and then can be run properly.
	def test_createTask(self):
		#Try to create a task without a valid function
		with self.assertRaises(TypeError):
			ITask.createTask(None)
		with self.assertRaises(TypeError):
			ITask.createTask(1337)

		#Check the times and recurring are set right
		m = 4
		h = 3
		d = 2
		task = ITask.createTask(testFunc,m,h,d,True)
		self.assertEquals(testFunc,task.run)
		self.assertEquals(m,task.minutes)
		self.assertEquals(h,task.hours)
		self.assertEquals(d,task.days)
		self.assertTrue(task.recurring)
		self.assertEquals(task.state, TaskState.PENDING)

		#Check that invalid times can't be passed it
		with self.assertRaises(TypeError):
			ITask.createTask(testFunc,"as","asd","asdf")


	##
	# Tests that the method for calculating the timestamp works correctly.
	# This means that if invalid parameters are given, it will not give
	# a timestamp that might be usable.
	def test_calculateTimestamp(self):
		from datetime import datetime,timedelta
		#Confirm that the timstamp is calculated correctly
		time = ITask(1,1,1).calculateTimestamp()
		cmpTime = datetime.now() + timedelta(minutes=1,hours=1,days=1)

		self.assertTrue( abs(time - cmpTime).total_seconds() <= 60)

	##
	# Tests the run method, there should always be an Error
	def test_run(self):
		with self.assertRaises(NotImplementedError):
			ITask().run(datetime.now())
	##
	# Tests that the comparison between tasks works as expected. Also checks
	# against non task objects.
	def test_lt(self):
		self.assertTrue (self.smaller < self.larger)
		self.assertFalse(self.smaller < self.smaller)
		self.assertFalse(self.larger  < self.smaller)

		with self.assertRaises(TypeError):
			self.smaller.__lt__("asdf")

	##
	# Tests that the comparison between tasks works as expected. Also checks
	# against non task objects.
	def test_le(self):
				
		self.assertTrue (self.smaller <= self.larger)
		self.assertTrue (self.smaller <= self.smaller)
		self.assertFalse(self.larger  <= self.smaller)

		with self.assertRaises(TypeError):
			self.smaller.__le__("Tasks")

	##
	# Tests that the comparison between tasks works as expected. Also checks
	# against non task objects.
	def test_eq(self):
		
		self.assertTrue (self.smaller == self.smaller)
		self.assertFalse(self.smaller == self.larger)

		with self.assertRaises(TypeError):
			self.smaller.__eq__("LOTS")


	##
	# Tests that the comparison between tasks works as expected. Also checks
	# against non task objects.
	def test_ne(self):
		
		self.assertTrue (self.smaller != self.larger)
		self.assertFalse(self.smaller != self.smaller)

		with self.assertRaises(TypeError):
			self.smaller.__ne__("3 chickens and a cow")

	##
	# Tests that the comparison between tasks works as expected. Also checks
	# against non task objects.
	def test_ge(self):
		
		self.assertTrue (self.larger  >= self.smaller)
		self.assertTrue (self.larger  >= self.larger)
		self.assertFalse(self.smaller >= self.larger)

		with self.assertRaises(TypeError):
			self.larger.__ge__("I'm still alive")

	##
	# Tests that the comparison between tasks works as expected. Also checks
	# against non task objects.
	def test_gt(self):
		
		self.assertTrue (self.larger  > self.smaller)
		self.assertFalse(self.larger  > self.larger)
		self.assertFalse(self.smaller > self.larger)

		with self.assertRaises(TypeError):
			self.larger.__gt__("Oh wait I'm not")

def testFunc():
	pass

class TestTaskScheduler(unittest.TestCase):
	##
	# Tests that the scheduler can be stopped and started without error and that
	# if you do try to start a started scheduler or stop a stopped scheduler an
	# error is raised.
	def test_startStopScheduler(self):
		scheduler = TaskScheduler()

		# Test the normal conditions.
		try:
			scheduler.startScheduler()
		except:
			self.fail('Failed to start scheduler under normal conditions.')

		try:
			scheduler.stopScheduler()
		except:
			self.fail('Failed to stop scheduler under normal conditions.')

		# And now we do the weird stuff...
		scheduler.startScheduler()
		with self.assertRaises(Exception):
			scheduler.startScheduler()

		scheduler.stopScheduler()
		with self.assertRaises(Exception):
			scheduler.stopScheduler()

	##
	# Tests that a task can be added when the scheduler is running and that it is
	# actually performed. It also tests that the scheduler does not accept tasks
	# when it is not running.
	def test_addTask(self):
		scheduler = TaskScheduler()

		# Lets start by just checking things are added. We'll then check that
		# work is performed later.

		# Test the normal conditions.
		scheduler.startScheduler()

		def nop():
			pass

		nopTask = ITask.createTask(nop)

		scheduler.addTask(nopTask)

		scheduler.stopScheduler()

		# Get to the weird stuff!
		with self.assertRaises(Exception):
			scheduler.addTask(nopTask)

		scheduler.startScheduler()
		with self.assertRaises(TypeError):
			scheduler.addTask(None)

		scheduler.stopScheduler()

	##
	# Tests that the scheduler runs events in the correct order and that they are
	# executed about when they should be.
	def test_runTasks(self):
		import datetime
		import time

		scheduler = TaskScheduler()

		scheduler.startScheduler()

		# Now we check that work is actually done.
		class TaskChecker(ITask):
			stack = []

			def __init__(self, minutes = 0, recurring = False):
				super(TaskChecker, self).__init__(minutes = minutes, recurring = recurring)

			def run(self, time):
				TaskChecker.stack.push(time)

		task = TaskChecker(minutes = 1)

		t = datetime.datetime.now() + datetime.timedelta(seconds = 60)
		scheduler.addTask(task)

		time.sleep(120) # Give it some time to run.

		self.assertEquals(len(TaskChecker.stack), 1)
		self.assertAlmostEqual(t, TaskChecker.stack[-1], delta = datetime.timedelta(seconds = 15))

		# Do a quick reset then check that tasks run in the right order.
		TaskChecker.stack = []

		task2 = TaskChecker(minutes = 2)

		t = datetime.datetime.now() + datetime.timedelta(seconds = 60)
		scheduler.addTask(task)
		t2 = datetime.datetime.now() + datetime.timedelta(seconds = 120)
		scheduler.addTask(task)

		time.sleep(300) # Give them some time to run.

		self.assertEquals(len(TaskChecker.stack), 2)
		self.assertAlmostEqual(t, TaskChecker.stack[0], delta = datetime.timedelta(seconds = 15))
		self.assertAlmostEqual(t2, TaskChecker.stack[1], delta = datetime.timedelta(seconds = 30))

		# Make sure that the scheduler actually stops when its told to.
		TaskChecker.stack = []
		scheduler.addTask(task)

		scheduler.stopScheduler()

		time.sleep(75)

		self.assertEquals(len(TaskChecker.stack), 0)

	##
	# Tests that the scheduler reschedules tasks that are set to run more than once.
	def test_runRecurring(self):
		import datetime
		import time

		scheduler = TaskScheduler()

		scheduler.startScheduler()

		class TaskChecker(ITask):
			stack = []

			def __init__(self, minutes = 0, recurring = False):
				super(TaskChecker, self).__init__(minutes = minutes, recurring = recurring)

			def run(self, time):
				TaskChecker.stack.push(time)

		task = TaskChecker(minutes = 1, recurring = True)
		t = datetime.datetime.now() + datetime.timedelta(seconds = 60)
		scheduler.addTask(task)

		for i in range(3):
			time.sleep(75) # Give it some time to work.

			self.assertEquals(len(TaskChecker.stack), i + 1)
			self.assertAlmostEqual(t, TaskChecker.stack[i], datetime.timedelta(15))

			t += datetime.timedelta(seconds = 60)

		scheduler.stopScheduler()

if __name__ is "__main__":
	unittest.main()
