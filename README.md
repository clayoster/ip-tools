ip-tools
=======

This web app will respond with different information based on the subdomain of the request that is received. Assuming that your domain is example.com and you have configured the following subodmians:

* ip.example.com
  * Responds with the IP of the requestor
* epoch.example.com
  * Provides the current epoch time
* headers.example.com
  * Outputs the headers that were received with the request
* proxy-headers.example.com
  * Outputs the proxy headers that were received with the request
* ptr.example.com
  * Outputs the PTR record for the IP address of the requestor

This project is based on the original work here: https://github.com/major/icanhaz
