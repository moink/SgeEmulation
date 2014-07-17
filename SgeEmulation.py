import unittest
import random

class SgeError(Exception):
    """Base class for exceptions in this module."""
    pass
 
class SgeJob():
 
    def __init__(self,jobname,runtime=100,initial_status="queued"):
        self.jobname=jobname
        self.runtime=runtime
        self.status=initial_status
        
 
class SgeEmulator():
#This is an emulator for a Sun Grid Engine
#It is from the point of view of a single user, so the number of
#available processors is a random number.
#It doesn't need to implement all aspects of a Sun Grid Engine, just those
#that are necessary to test my queuing strategies.
   
    def __init__(self,min_slots=0,max_slots=10):
        self._joblist=[]
        try:
            self._slots=random.randrange(min_slots,max_slots)
        except ValueError:
            self._slots=min_slots
 
    def add_job(self,jobname,runtime=100,initial_status="queued"):
        if initial_status in ["queued","hold"]:
            self._joblist.append(SgeJob(jobname,runtime,initial_status))
        else:
            raise SgeError("Initial job status can only be 'queued' or 'hold'")
 
    def get_job_names(self):
        jobnames=[]
        for job in self._joblist:
            jobnames.append(job.jobname)
        return jobnames
 
    def get_job_status(self,jobname):
        for job in self._joblist:
            if job.jobname==jobname:
                return job.status
        return "absent"
 
    def tick(self,ticklength=1):
        for job in self._joblist:
            if job.status=="running":
                job.runtime=job.runtime-ticklength
            
 
class TestSgeEmulator(unittest.TestCase):

    def test_adding_job(self):
        #when you add a job, it should go in the job list, either queued or running
        emu=SgeEmulator()
        emu.add_job("test job")
        self.assertTrue("test job" in emu.get_job_names())
        self.assertTrue(emu.get_job_status("test job")
                        in ["queued","running"])

    def test_adding_running_job(self):
        #when you try to add a job that is not queued or on hold, you should get an exception
        emu=SgeEmulator()
        self.assertRaises(SgeError,emu.add_job,"test job",100,"running")
 
    def test_job_runs(self):
        #when you add a job to an emulator with exactly one available slot, the job
        #should start running on the next tick
        emu=SgeEmulator(1,1)
        emu.add_job("test",100)
        emu.tick()
        self.assertTrue(emu.get_job_status("test")=="running")
      
if __name__ == "__main__":
    unittest.main()
