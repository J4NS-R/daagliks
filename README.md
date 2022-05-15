# Daagliks

## Usage

### Testing

```sh
export PYTHONPATH=$PWD/test
python3 daagliks_tests.py
```

## Design

* The `daagliks_cron.py` script runs on a user-configurable cron schedule. Something like every 15m during working
  hours.
* On each run the script does the following:
  * Asks the user what they're doing. Stores the result to a DB
  * (todo) sync with sharpie
* The `daagliks_stats.py` script should give some stats about the day.
