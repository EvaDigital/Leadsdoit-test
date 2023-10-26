# Leadsdoit-test

## Initial Setup
1. **Clone the project**
```sh
  git clone https://github.com/EvaDigital/Leadsdoit-test.git
```
2. **Go to project derictory**
```sh
  cd Leadsdoit-test/
```
4. **Create .env file (use env-exemple)**
```sh
  nano .env
```
4. **Start the App**
```sh
  docker-compoe up --build -d
```

### API

### Base URL

All API requests should be made to:

```
http://localhost:8080/
```

### `/get-weather/` (GET)

Getting the weather on a specific date

#### Request

- Method: GET
- URL: `/get-weather/`
- Params: `day:2023-10-26 `

```json
[
    {
        "city": "Krakow",
        "temperature": 15,
        "description": "Clouds",
        "time": "13:53"
    },
   ...
]
```

### TESTS
```sh
  docker exec -it leadsdoit-test-web-1 pytest
```
