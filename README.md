![plot](bhff-logo.png)
# Google Data Transfer
Automating data transfer and processing between Google Forms and Google Sheets, using Google Cloud APIs.
Currently only supports the "Mentoring Reports Default" transfer configuration, used for mentoring report automatization inside BHFF.
## How to install
0. Contact dev at data@bhfuturesfoundation.org for credentials. Place the credentials file in `./secrets/credentials.json`.
1. Create and activate conda environment
```shell
conda create -n google_data_transfer python=3.10
conda activate google_data_transfer
```
2. Install package
```shell
pip install -e .
```
## How to run
#### Mentoring Reports processing
After a "Mentoring Report" Google form is filled out by BHFF scholars, the responses about their mentoring activity (having enough meetings) and the reason behind potential inactivity are transferred to a "Mentoring Scholar Tracking" Google sheet. <br />
The form's and sheet's "edit" URLs must be provided. An "edit" URL contains the `/edit` substring and can be acquired when editing the resources with appropriate permissions. <br />
Run the following command from the repo root:
```shell
python google_data_transfer/cli.py transfer <form-edit-url> <sheet-edit-url> <sheet-name> [--target-col <target-col>]
```  

