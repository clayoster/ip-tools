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


Deployment Examples
==
## Docker Compose
```yaml
services:
  ip-tools:
    container_name: ip-tools
    image: ghcr.io/clayoster/ip-tools:latest
    restart: always
    environment:
      # Enable to allow headers.* and proxy-headers.* to work. Disabled by default
      # to avoid exposing internal infrastructure bread crumbs by accident.
      ENABLE_HEADERS: false
    ports:
      - "8090:8080"
```

## Kubernetes
```yaml
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ip-tools
  namespace: ip-tools
  labels:
    app: ip-tools
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ip-tools
  template:
    metadata:
      labels:
        app: ip-tools
    spec:
      containers:
        - name: ip-tools
          image: ghcr.io/clayoster/ip-tools:latest
          # Enable to allow headers.* and proxy-headers.* to work. Disabled by default
          # to avoid exposing internal infrastructure bread crumbs by accident.
          env:
            - name: ENABLE_HEADERS
              value: "false"
          ports:
            - containerPort: 8080
              name: 8080tcp
              protocol: TCP
          resources: {}
---
apiVersion: v1
kind: Service
metadata:
  name: ip-tools
  namespace: ip-tools
spec:
  selector:
    app: ip-tools
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: ClusterIP
---
apiVersion: traefik.io/v1alpha1
kind: IngressRoute
metadata:
  name: ip-tools
  namespace: ip-tools
spec:
  entryPoints:
    - websecure
  routes:
    - match: Host(`ip.example.com`) || Host(`epoch.example.com`) || Host(`headers.example.com`) || Host(`proxy-headers.example.com`)|| Host(`ptr.example.com`)
      kind: Rule
      services:
        - name: ip-tools
          port: 80
```
