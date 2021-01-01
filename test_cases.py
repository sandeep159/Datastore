# DATA STORE EXPOSING AS A LIBRARY
from datastore import DataStore
import threading, os, unittest, time, json, sys

class test_cases_for_datastore(unittest.TestCase):

    def setUp(self):
        self.data_store = DataStore()
    
    def test_initialize_with_operational_file_path(self):
        self.assertTrue(os.path.exists(self.data_store.file_location))
    
    # CREATING DATAS USING CREATE
    def test_create_data(self):
        d1 = self.data_store.create("person1",
        {
            'name' : 'john',
            'dob' : '06-07-2000'
        },5)
        self.assertTrue(d1)
        d2 = self.data_store.create("person2",
        {
            'name' : 'mark',
            'dob' : '06-07-2000'
        },10)
        self.assertTrue(d2)
        d3 = self.data_store.create("person3",
        {
            'name' : 'stark',
            'dob' : '08-05-1998'
        },10)
        self.assertTrue(d3)

    # TRYING CREATE DATA FOR EXISTING KEY
    def test_create_data_for_existing_key(self):
        d1 = self.data_store.create("person1",
        {
            'name' : 'stark',
            'dob' : '08-05-1998'
        },30)
        self.assertFalse(d1)

    # TRYING TO CREATE DATA USING INVALID KEYS
    def test_create_data_for_InvalidKey(self):

        # KEY CAPPED MORE THAN 32 CHARS
        d1 = self.data_store.create("person123456789011121314151617181920212223242526272829",
        {
            'name' : 'tony',
            'dob' : '03-02-1978'
        },30)
        self.assertFalse(d1)

        # USING NON-STRING AS KEY
        d2 = self.data_store.create(12345,
        {
            'name' : 'mark',
            'dob' : '07-08-1999'
        },60)
        self.assertFalse(d2)
    
    # TRYING TO CREATE DATA USING INVALID VALUE SIZE MORE THAN 16KB
    def test_create_data_for_InvalidValues(self):
        self.fileloc = "test_datas/sixteen_KB.json"
        value={}
        with open(self.fileloc) as f:
            value = json.load(f)
        d1 = self.data_store.create("SixteenKB",value,60)   
        self.assertFalse(d1)
    
    # ACCESSING DATA USING READ BY PROVIDING PROPER KEY
    def test_read_data(self):
        d1 = self.data_store.read("person3")
        self.assertTrue(d1)
    
    # TRYING TO ACCESS DATA USING NON-EXISTING KEY
    def test_read_data_for_NonExisting_Key(self):
        d1 = self.data_store.read("SixteenKB")
        self.assertFalse(d1)
    
    # REMOVING DATA USING DELETE
    def test_delete_data(self):
        d1 = self.data_store.delete("person2")
        self.assertTrue(d1)
    
    # TRYING TO DELETE AN NON-EXISTING DATA
    def test_delete_NonExisting_data(self):
        time.sleep(5)
        d1 = self.data_store.delete("person1")
        self.assertFalse(d1)

    # A CLIENT PROCESS IS ALLOWED TO ACCESS THE DATA STORE USING MULTIPLE THREAD
    def test_create_data_using_multiplethreads(self):
        t1 = threading.Thread(target=self.data_store.create,args=("thread1",
        {
            'name':'king',
            'dob' : '02-03-1991'
        },5))
        t2= threading.Thread(target=self.data_store.read, args=("person3", ))
        t3 = threading.Thread(target=self.data_store.delete, args=("person1", ))

        t1.start()
        t2.start()
        t3.start()
    
        t1.join()
        t2.join()
        t3.join()

        self.assertTrue(t1)
        self.assertTrue(t2)
        self.assertTrue(t3)



if __name__ == "__main__":
    unittest.main()

   
