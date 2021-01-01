# Datastore
A file-based key-value data store which support the basic Create, Read and Delete operations.

## Features

* A new key-value pair can be added to the Data-store using Create operation
* 1GB file storing size
* Can store values upto 16KB and using string key capped at 32 chars
* Accessing a key-value pair can be performed using Read operation
* Removing a key-value pair can be performed using Delete operation
* Once the Time-To-Live for a key has expired, the key will no longer accessable
* Can access data using multiple-threads by same client

## Getting Started

* Clone the repository and cd into `Datastore`
```
bash
git clone https://github.com/sandeep159/Datastore.git
cd Datastore
```
       
* Include header file
```
python
from datastore import DataStore
```

* Initialise an object for datastore
```
python
data_store = DataStore(file_location = `File_Path`)
```
   **NOTE :- it can be initialized using an operational filepath if not provided it will reliably create itself**
   
* ### CREATE
```
python
data_store.create(key_name,value,time_to_live)
```
A new key-value pair can be added to data store `create()` function, it has 2 neccessary arguments key which should be a `string` capped at 32 chars and value wich should be a `JSON` object capped at `16KB` and a time_to_live property it is optional by default it will take 60, but if provided it will be evaluated as `seconds`, once the time_to_live for a key expired the key will be unavailable for other operations

   
* ### READ
```
python
data_store.read(key)
```

A `read()` function takes one argument key, if key not found or expired an appropreate error message is displayed else the value will be returned


* ### DELETE
```
python
data_store.delete(key)
```

A `delete()` function takes one argument key, if key not found or expired an appropreate error message is displayed else the corresponding data will be deleted from data store



## Running the tests

the `python` file `test_cases.py` has the test cases which cover all the basic operations of the `datastore.py` in expected an unexpected ways including multiple treads

execute the following file to run test on `datastore`

`test_cases.py`
