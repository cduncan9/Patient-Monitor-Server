# Final Project
This is the repository for the final project for BME 547. The contributors to this repository are [Aidan Therian](https://github.com/aidan-therien) and [Canyon Duncan](https://github.com/cduncan9), and the professor for BME 547 is [Dr. David Ward](https://github.com/dward2?tab=followers). 
## Using This Software
This software consists of two graphical user interfaces (GUI), one used by a patient (the patient-side client) and one used by someone who is monitoring the patient (the monitoring-station client). These two GUIs are capable of sending and receiving patient data between themselves through the use of a cloud server. 
Both of the client GUIs can only send and receive data when the cloud server is running, so it is important to make sure that the server is running either locally or on a virtual machine (click [here](https://github.com/dward2/BME547/blob/master/Resources/virtual_machines.md) for information on setting up Duke Virtual Machines).

#### Using The Patient-Side Client
To use the patient-side client from the command line, open up a terminal and navigate to the folder containing the python module `patient_gui_client.py`.
Then, on the command line, type in `python python_gui_client.py` and hit `Enter` or `Return`.
You will now see window open up on the screen of your computer that looks like:

ENTER IMAGE HERE OF THE PATIENT SIDE GUIs

Add more here after talking to Aidan

#### Using The Monitoring-Station Client
To use the monitoring-station client, open up a terminal and navigate using the command line to the folder containing the python module `monitoring_station_gui_client.py`.
On the command line type `python mpnitoring_station_gui_client.py` and hit `Enter` or `Return`.
You will now see window open up on the screen of your computer that looks like:

ENTER IMAGE HERE OF THE MONITORING STATION GUI

This monitoring-station graphical user interface enables a user to select a patient medical record number from a drop-down menu and load recent patient data.
Click the down arrow on the drop-down box at the top of the GUI window and select the medical record number of the patient that you are interested in monitoring.
Once you have selected a patient, click the button that says `Load Patient Data`. Once this button has been clicked, the following information will then appear onto the GUI:
* The Patient Id, which is the Medical Record Number of the patient
* The name of the patient
* The most recent heart rate reading, taken from a list of stored heart rate averages for uploaded ECG datasets
* An image of the most recent ECG dataset plotted using `matplotlib`
* The date and time of the most recent ECG dataset upload

All of this data should appear beside its corresponding label on the screen. This data is updated every twenty seconds to ensure that the most recent data is being displayed on the screen.
If you wish to load an image of a past ECG dataset, click on the arrow of the drop-down menu designated `Load Past ECG` and select the timestamp of the ECG which you wish to see.
Press the button beside the drop-down menu that says `Load Data`. After that, you should see the image of the selected ECG dataset appear beside the image of the most recent ECG dataset.
You will also notice another button appear below the new ECG image that says `Save Past ECG Image`. 
If you wish to save a copy of this image onto your computer, press this button. A file dialog box will then pop up onto the screen.
You can use this file dialog box to nevigate to the folder that you wish to save your ECG image, and you can provide a name to save your image file under.

INFORMATION ABOUT USING THE MEDICAL IMAGE DROP DOWN BOX.

If at any time you wish to reset all of data on the scren to it's cleared appearence before any data was loaded, press the `Reset Data` button, and all of the patient data on the screen will disappear.
If at any time you wish to exit the monitoring-station GUI, you can click the `Exit` button, which will close the program.

## About This Software
The patient-side client is used to populate the database that stores patient information. The patient side client is capable of sending the patient's medical record number, name, average heart rate for an ecg sample, the time that any ECG data is sent to the server, an image of a plotted ECG dataset, medical images like Xrays or CT scans, and the filenames of the uploaded medical images.
 
## Access This Server

## Git Status Badge

## Software License 
