import os,json, sys, threading
from datetime import datetime,timedelta

File_Path= "storage/datas.json"

class DataStore:

    def __init__(self, file_location = File_Path):
        self.file_location = file_location
        self.lock = threading.Lock()

        # initialising using an operational file path.
        self.datas = self.load_datas()


    # initializing using an operational file path, if not provided it will create itself one
    def load_datas(self):

        # initialising an temporary JSON object
        json_obj = {}

        # creating an operational file path and and file storage 
        if not os.path.exists(self.file_location):
            os.makedirs(os.path.dirname(self.file_location))
            self.add_to_json(json_obj)
            print("CREATED AN NEW DATA STORE IN FILE PATH ",os.path.abspath(self.file_location))

        # Accessing the existing file path
        else:
            json_obj = self.load_from_json(json_obj)
            print("ACCESSING EXISTING DATA STORE FROM FILE PATH", os.path.abspath(self.file_location))

            # checking if data expired or not
            json_obj = self.is_expired(json_obj)

        # returning the JSON object
        return json_obj


    # adding obJects to DATASTORE
    def add_to_json(self, json_obj):
        with open(self.file_location, 'w') as new_file:
            json.dump(json_obj, new_file)
    
    # loading objects from JSON
    def load_from_json(self, json_obj):
        with open(self.file_location) as existing_file:
            json_obj = json.load(existing_file)
        return json_obj
    
    # removing expired data from DATASTORE
    def is_expired(self,json_obj):
        for key in list(json_obj.keys()):
            if datetime.strptime(json_obj[key]['expire'], '%Y-%m-%dT%H:%M:%SZ') < datetime.now():
                print("DATA FOR KEY ",key," IS EXPIRED VALUES WILL NO LONGER BE AVAILABLE")
                del json_obj[key]
        # updating DATASTORE with modified datas
        with open(self.file_location, 'w') as new_file:
            json.dump(json_obj, new_file)
        return json_obj


    # A new key-value pair can be added to the data store using the create operation.
    def create(self,key,value,expiry=60):
        self.lock.acquire()
        try:
            # to keep track if any error occured
            flag = True 
            self.datas = self.is_expired(self.datas)

            # if create is invoked for an existing key, this will execute
            if key in self.datas: 
                print("THE KEY YOU ENTERED",key, "ALREADY EXISTS, PLEASE TRY ANOTHER")
                flag=False

            # the key should be a string capped at 32 chars, else this will execute
            if type(key) != str or len(key) > 32:
                print("YOUR KEY ",key," SHOULD BE MAX 32 CHARACTERS AND MUST BE A STRING")
                flag=False
            
            #The size of the file storing data must never exceed 1GB which is (1024  * 1024 * 1024) [1GB = 1024^3]
            if (os.path.getsize(self.file_location) + sys.getsizeof(value)) >= (1024  * 1024 * 1024) :
                print("MEMORY SIZE REACHED MAXIMUM SIZE OF 1GB")
                flag=False

            # The value is always a JSON object - capped at 16KB which is (16*1024) [1KB = 1024]
            if sys.getsizeof(value) > (16 * 1024):
                print("VALUE SIZE REACHED MAXIMUM SIZE OF 16 KB")
                flag=False
            
            # creates new JSON key-value pair if no error occured
            if flag == True:
                expiry_date = datetime.now()+timedelta(seconds=expiry)
                self.datas[key] = {
                    'value': json.dumps(value),
                    'created_date' : datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
                    'expire' : expiry_date.strftime('%Y-%m-%dT%H:%M:%SZ')
                }

                self.add_to_json(self.datas)
                print("NEW DATA ADDED TO THE RECORD KEY = ",key," VALUE = ", value)

        except Exception as e:
            print(str(e))
        self.lock.release()
        return flag



    
    # A read operation to access the data from DATASTORE by providing key
    def read(self,key):

        try:
            # it returns an json object
            datas = {}
            datas = self.load_from_json(datas)
            datas = self.is_expired(datas)
            result = None
            
            # if key not found in DATASTORE
            if key not in datas.keys():
                print("CAN'T READ THE KEY YOU ENTERED ",key, "DOES NOT EXIST OR MAY EXPIRED TRY ANOTHER KEY")
                result = False 
            
            # if the key found
            if key in datas.keys():
                result = True
                print("THE VALUES FOR THE KEY ",key," IS ",datas[key]['value'])

        except Exception as e:
            print(str(e))  

        return result   



    # delete operation to remove objects from DATASTORE using key provided
    def delete(self,key):
        self.lock.acquire()
        try:

            datas = {}
            datas = self.load_from_json(datas)
            datas = self.is_expired(datas)
            result = None  
            
            # if key is not found in datastore
            if key not in datas.keys():
                print(" CAN'T DELETE THE KEY YOU ENTERED ",key, " DOES NOT EXIST OR MAY EXPIRED")
                result = False


            # if key found 
            if key in datas.keys():
                print("THE VALUE ",datas[key]['value']," FOR KEY ",key," IS DELETED FROM DATA STORE")
                del datas[key]
                result = True

                self.add_to_json(datas)
        except Exception as e:
            print(str(e))
        self.lock.release()
        return result




