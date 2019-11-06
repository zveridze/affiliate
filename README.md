[![Build Status](https://travis-ci.org/zveridze/affiliate.svg?branch=master)](https://travis-ci.org/zveridze/affiliate)
[![Maintainability](https://api.codeclimate.com/v1/badges/e5ab8a137929d09d98a5/maintainability)](https://codeclimate.com/github/zveridze/affiliate/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/e5ab8a137929d09d98a5/test_coverage)](https://codeclimate.com/github/zveridze/affiliate/test_coverage)

## CPA network

### How to start
1. Clone repo
2. pip install -r requirements.txt
3. Make ```Flask run```

### Flake8
You can run flake with ```flake8 .```

### Tests
You can run tests with ```pytest tests/```
See [pytest](http://doc.pytest.org/en/latest/usage.html) documentation for information.

### Instruction:
1. Create user with registration form on /register
2. Create link for current user on /links
3. You can add generated link to your promo campaign
4. After user click and redirect to site system will count a click

### Redis using docker
1. First you need to start Redis Server in Docker container ```run --name %set your name% -p %set your ports% -d redis```
2. Second you need start RQ worker ```rq worker %your Redis Server name%```
3. That`s all. Now you can send tasks to the queue. 
