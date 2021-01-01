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
   **NOTE :- recomending a JSON object for argument value, but any thing is acceptable, the time_to_live is an optional argument if not provided it will take 60**
