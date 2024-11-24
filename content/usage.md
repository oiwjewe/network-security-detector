<h3>Usage:</h3><br>

The required columns to run this tool is:<br>
*ClientIP,ClientRequestHost,ClientRequestMethod,ClientRequestURI,EdgeStartTimestamp,ZoneName,ClientASN,ClientCountry*,<br>
*ClientDeviceType,ClientSrcPort,ClientRequestBytes,ClientRequestPath,ClientRequestReferer,ClientRequestScheme,ClientRequestUserAgent*<br>


However the code has a some flexibility to handle little variations of it. Just don't go too wild.<br><br>

To run this script, you’ll need to use the Docker basic comands as suggested in the examples bellow:<br>



A initial sample could be done with this sample:<br>
https://gist.githubusercontent.com/cloudwalk-tests/3c82d813645f547618b3ea81b6d269b8/raw/e0006a126b85782d95a655977deeabbb2b41d0c7/test-dataset.csv<br>

**1)Add data**: Fisrt add a sample of data in .CSV format for machine learning training.<br>

Firs run the container:<br>

`docker run -d --name network-traffic-analyzer:first w1ndx/network-traffic-analyzer:first`<br>

Then, copy the file in your real system to inside the container:<br>

`docker cp /caminho/para/seu/arquivo.csv w1ndx/network-traffic-analyzer:first:/usr/src/network_trf_analyzer/arquivo.csv` #replace the file path and file name to feet your needs

**2)Execute**: To run the tool, simply execute the following command:<br>

`sudo docker run --rm w1ndx/network-traffic-analyzer:first python3 ./network_trf_analyzer.py`

**3)Remove data**: To remove the data manually:<br>

To remove specific files:<br>

`docker exec w1ndx/network-traffic-analyzer:first rm /usr/src/network_trf_analyzer/arquivo.csv`<br>

To remove all .CSV files in a directory inside the container:<br>

`docker exec w1ndx/network-traffic-analyzer:first rm /usr/src/network_trf_analyzer/*.csv`

To verify if the files were removed sucessfuly:<br>

`docker exec w1ndx/network-traffic-analyzer:first ls /usr/src/network_trf_analyzer/*.csv`

The inclusion and data removal can be done manually but you can automate this process as suggested bellow, in this case provide your customized changes:<br>

# Example of scripts to upload and remove data from the container 
- [Add-data](add-data.sh)<br>
- [Remove-data](remove-data.sh)<br>

An interesting ideia would be setup a daemon to run the network-security-detector 24/7
