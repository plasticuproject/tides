[![build](https://github.com/plasticuproject/tides/actions/workflows/tests.yml/badge.svg)](https://github.com/plasticuproject/tides/actions/workflows/tests.yml)
[![Python 3.8](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-380/)
![GitHub](https://img.shields.io/github/license/plasticuproject/tides)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=plasticuproject_tides&metric=alert_status)](https://sonarcloud.io/dashboard?id=plasticuproject_tides)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=plasticuproject_tides&metric=security_rating)](https://sonarcloud.io/dashboard?id=plasticuproject_tides)

Toy Flask API that returns forecasted low tide data during sunlight hours for selected locations.

Requirements:
- python >= 3.8
- python3-pip >= 22.2.2


Install and Run:
```
pip install -r requirements.txt
python -m api
```

Valid Endpoints:
- http://127.0.0.1:5000/api/v1/Half-Moon-Bay-California
- http://127.0.0.1:5000/api/v1/Huntington-Beach
- http://127.0.0.1:5000/api/v1/Providence-Rhode-Island
- http://127.0.0.1:5000/api/v1/Wrightsville-Beach-North-Carolina
