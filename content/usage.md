<h3>Usage:</h3><br>

To run this script, you’ll need to use the Docker basic comands as suggested in the examples bellow:<br>

The required columns to run this tool is:<br>
ClientIP,ClientRequestHost,ClientRequestMethod,ClientRequestURI,EdgeStartTimestamp,<br>
ZoneName,ClientASN,ClientCountry,ClientDeviceType,ClientSrcPort,ClientRequestBytes,<br>
ClientRequestPath,ClientRequestReferer,ClientRequestScheme,ClientRequestUserAgent<br>

However the code has a little flexibility to handle little variations in it, just don't be to wild.

A initial sample could be done with this sample: https://gist.githubusercontent.com/cloudwalk-tests/3c82d813645f547618b3ea81b6d269b8/raw/e0006a126b85782d95a655977deeabbb2b41d0c7/test-dataset.csv<br>

1)Fisrt add a sample of data in .CSV format for machine learning training. This can be done









8)Finally, to run the script, simply execute the following command:<br>

`sudo docker run --rm w1ndx/network-traffic-analyzer:first python3 ./network_trf_analyzer.py`



You can also automate the .csv file upload and remotion in the container.<br>
A simple example of how this could be done is given here:
