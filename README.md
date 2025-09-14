ip-tools
=======

This web app will respond with different information based on the subdomain of the request that is received. Assuming that your domain is example.com and you have configured the following subodmians:

* ip.example.com
  * Responds with the IP of the requester
* epoch.example.com
  * Provides the current epoch time
* headers.example.com
  * Outputs the headers that were received with the request
  * Must be enabled by setting an environment variable of ENABLE_HEADERS=true
    * If the application is facing the internet, this can expose sensitive information
* proxy-headers.example.com
  * Outputs the proxy headers that were received with the request
  * Must be enabled by setting an environment variable of ENABLE_HEADERS=true
    * If the application is facing the internet, this can expose sensitive information
* ptr.example.com
  * Outputs the PTR record for the IP address of the requester

This project is based on the original work here: https://github.com/major/icanhaz
