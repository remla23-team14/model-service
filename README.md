# model-service
This service provides an API endpoint so that one can check 
if reviews are positive or negative.

## How to run

### Service start-up
The best way to start the service is through the released docker images.
To run the latest version:
```sh
docker run --rm -it -p8080:8080 ghcr.io/remla23-team14/model-service:latest
```

If you wish to run modify some enviroment variables see the docker compose and README
in [our operation repo](https://github.com/remla23-team14/operation).

#### Start-up locally
One can also start of the service locally by following these steps:
1. Download python dependencies: `pip install -r requirements.txt`
2. Rename the file `development.env` to `.env`.
3. Run it by calling `python src/app.py`

### Service querying 
You can then query the service **after starting it** to see if a review is positive or negative by either:
* Going to [http://localhost:8080/apidocs](http://localhost:8080/apidocs) and interacting with the swagger api.
* Using curl: `curl -X POST "http://127.0.0.1:8080/predict" -H  "accept: application/json" -H  
  "Content-Type: application/json" -d "{  \"review\": \"We are glad we found this place.\"}"`
* Or performing POST on "http://localhost:8080/" with json body containing the msg.

### Build the docker image
You can also build the docker image yourself.

Go to the root of this directory in terminal:
```shell
cd <path_to_model-service_root>
```

Build the docker image:
```shell
docker build . -t ghcr.io/remla23-team14/model-service:latest

#Or if you want to give it your own name:
docker build . -t <your_name>:<your_tag>
```

Then it can be run with:

```sh
docker run --rm -it -p8080:8080 ghcr.io/remla23-team14/model-service:latest

#Or if you built it using your own name:
docker run --rm -it -p8080:8080 <your_name>:<your_tag>
```
