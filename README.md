# FidoIoTInjest

1. Python Setup: 
Create python env in project directory and install the below libraries or use the requirement.txt which can be found in the project directory. The python version for this project is 3.12.8
pip install fastapi
pip install uvicorn
pip install pydantic
pip install numpy
pip install pytest

2. To setup the database the FIDO_database.db file already exists in the project directory and is set up in the .env file as the SQLITE_DB parameter which is used for connecting to the database. If you have an existing SQLite database you would like to use please use the schema.sql file to import the schema into your database. Then change the SQLITE_DB parameter to the location or url of your database. 

3. To test you can create a launch.json or run fastapi though uvicorn app:app

4. Go to localhost:8000/docs to test the /process-audio endpoint. 
Use the below json test to check successful insert which should return a 201 response

{
  "session_id": "126336376",
  "timestamp": "2025-01-12T19:36:00.935Z",
  "audio_files": [
    {
      "file_name": "random_name",
      "encoded_audio": "MDAwMDAwMTAwMDEwMTAwMDEwMDEwMTAwMDEwMDAwMDAwMDEwMTAwMTAwMTAxMDAxMDAwMDEwMTAwMTAwMDEwMDAxMDAxMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDEwMTEwMTAxMTAwMDAwMDAwMDAwMDEwMTAxMDExMTEwMDAwMDAwMDAwMDAwMDAwMTAxMTExMTExMTAwMDAwMDAwMDAwMDAwMDAwMTAxMTEwMTAxMDExMTExMTExMTEwMTAwMTEwMTAwMTAxMDEwMTAxMDEwMDAxMDAxMDEwMTEwMDAxMTEwMDE="
    }
  ]
}

the below json should be an example of an 422 response where an encoded_audio parameter has not been encoded

{
  "session_id": "126336376",
  "timestamp": "2025-01-12T19:36:00.935Z",
  "audio_files": [
    {
      "file_name": "random_name",
      "encoded_audio": "b'\x52\x49\x46\x46\x12\x00\x00\x00\x57\x41\x56\x45\x66\x6d\x74\x20'"
    }
  ]
}

5. The test file has 3 test functions and can be called using pytest .\integration_tests\app.py

- First is a successful test which creates sample noise data which is then successfully base64 encoded and sent to the endpoint creating a successful 201 response and inserting the data into the database. The numbers such as audio_files_number can also be tweaked here to test sending multiple encoded audio files in one session. It then carries out an assert to ensure the content_list is as expected. 

- The second test is a failure test to ensure that the pydantic model works appropriately at validating types of the payload, there is also 2 custom validators. Encoded_Audio_Validator checks that the encoded_audio parameter is a base64 encoded string. Timestamp_Format_Validate checks that the timestamp is of the correct iso 8601 format. Both of these should raise errors on failing and trigger the standard 422 response. These validators run after pydantic's standard checks.

- Finally, the third test checks that the endpoint returns a 201, on processing 1000 files of 100s durations.




