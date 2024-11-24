<h3>Usage:</h3><br>

**READ 'ACKNOWLEDGEMENTS' SESSION FROM README.MD BEFORE RUN THIS TOOL**!<br><br>
The required columns to run this tool is:<br>
*ClientIP,ClientRequestHost,ClientRequestMethod,ClientRequestURI,EdgeStartTimestamp,ZoneName,ClientASN,ClientCountry*,<br>
*ClientDeviceType,ClientSrcPort,ClientRequestBytes,ClientRequestPath,ClientRequestReferer,ClientRequestScheme,ClientRequestUserAgent*<br><br>

To run **network-security-detector tool**, you’ll need to use the Docker basic comands as suggested in the examples bellow:<br>

A initial tests could be done with this sample:<br>
- [Data sample](sample.csv)<br><br>


**1)Add data manually**: Fisrt add a sample of data in .CSV format for machine learning training.<br>

Firs run the container:<br>

`docker run -d --name network-traffic-analyzer:first w1ndx/network-traffic-analyzer:first`<br>

Then, copy the file in your real system to inside the container:<br>

`docker cp /caminho/para/seu/arquivo.csv w1ndx/network-traffic-analyzer:first:/usr/src/network_trf_analyzer/arquivo.csv` #replace the file path and file name to feet your needs

**2)Execute**: To run the tool, execute the following command:<br>

`sudo docker run --rm -p 443:443 w1ndx/network-traffic-analyzer:first bash -c "service apache2 start && python3 /usr/src/network_trf_analyzer/network_trf_analyzer.py"`


`sudo docker run --rm w1ndx/network-traffic-analyzer:first python3 ./network_trf_analyzer.py`

**3)Remove data manually**:<br>

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

An interesting ideia would be setup a daemon to run the network-security-detector tool 24/7
