import requests
import threading

from myradar.models import Forecast


def load_forecast(key, lat, lng, time=None, units="auto", lang="en", lazy=False,
                  callback=None):
    """
        This function builds the request url and loads some or all of the
        needed json depending on lazy is True

        inLat:  The latitude of the forecast
        inLong: The longitude of the forecast
        time:   A datetime.datetime object representing the desired time of
               the forecast. If no timezone is present, the API assumes local
               time at the provided latitude and longitude.
        units:  A string of the preferred units of measurement, "auto" id
                default. also us,ca,uk,si is available
        lang:   Return summary properties in the desired language
        lazy:   Defaults to false.  The function will only request the json
                data as it is needed. Results in more requests, but
                probably a faster response time (I haven't checked)
    """

    if time is None:
        url = 'https://api.myradar.dev/forecast/%s/%s,%s' \
              '?units=%s&lang=%s' % (key, lat, lng, units, lang)
    else:
        url_time = time.replace(microsecond=0).isoformat()  # API returns 400 for microseconds
        url = 'https://api.myradar.dev/forecast/%s/%s,%s,%s' \
              '?units=%s&lang=%s' % (key, lat, lng, url_time, units, lang)

    if lazy is True:
        baseURL = "%s&exclude=%s" % (url,
                                     'minutely,currently,hourly,'
                                     'daily,alerts,flags')
    else:
        baseURL = url

    return manual(baseURL, callback=callback)


def manual(requestURL, callback=None):
    """
        This function is used by load_forecast OR by users to manually
        construct the URL for an API call.
    """

    if callback is None:
        return get_forecast(requestURL)
    else:
        thread = threading.Thread(target=load_async,
                                  args=(requestURL, callback))
        thread.start()


def get_forecast(requestURL):
    myradar_reponse = requests.get(requestURL)
    myradar_reponse.raise_for_status()

    json = myradar_reponse.json()
    headers = myradar_reponse.headers

    return Forecast(json, myradar_reponse, headers)


def load_async(url, callback):
    callback(get_forecast(url))
