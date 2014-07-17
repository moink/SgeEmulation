import unittest
import random
 
class SgeJob():
 
    def __init__(self,jobname,runtime=100):
        self._jobname=jobname
        self._runtime=runtime
        self._status="queued"
 
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
 
    def add_job(self,jobname,runtime=100):
        self._joblist.append(SgeJob(jobname))
 
    def get_job_names(self):
        jobnames=[]
        for job in self._joblist:
            jobnames.append(job._jobname)
        return jobnames
 
    def get_job_status(self,jobname):
        for job in self._joblist:
            if job._jobname==jobname:
                return job._status
        return "absent"
 
    def tick(ticklength=1):
        pass
 
class TestSgeEmulator(unittest.TestCase):
 
    def setUp(self):
        self.emu=SgeEmulator()
       
    def test_adding_job(self):
        #when you add a job, it should go in the job list, either queued or running
        self.emu.add_job("test job")
        self.assertTrue("test job" in self.emu.get_job_names())
        self.assertTrue(self.emu.get_job_status("test job")
                        in ["queued","running"])
 
    def test_job_runs(self):
        #when you add a job to an emulator with exactly one available slot, the job
        #should start running on the next tick
        emu2=SgeEmulator(1,1)
        emu2.add_job("test",100)
        emu2.tick()
        self.assertTrue(emu2.get_job_status("test")=="running")
      
if __name__ == "__main__":
    unittest.main()
