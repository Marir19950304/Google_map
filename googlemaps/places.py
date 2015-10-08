#
# Copyright 2015 Google Inc. All rights reserved.
#
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
#

"""Performs requests to the Google Maps Places API."""

from googlemaps import convert


def places(client, query, location=None, radius=None, language=None,
           min_price=None, max_price=None, open_now=False, types=None,
           page_token=None):
    """
    Performs text search for places.

    :param query: The text string on which to search, for example: "restaurant".
    :type query: string

    :param location: The latitude/longitude value for which you wish to obtain the
                     closest, human-readable address.
    :type location: string, dict, list, or tuple

    :param radius: Distance in meters within which to bias results.
    :type radius: int

    :param language: The language in which to return results.
    :type langauge: string

    :param min_price: Restricts results to only those places with no less than
                      this price level. Valid values are in the range from 0
                      (most affordable) to 4 (most expensive).
    :type min_price: int

    :param max_price: Restricts results to only those places with no greater
                      than this price level. Valid values are in the range
                      from 0 (most affordable) to 4 (most expensive).
    :type max_price: int

    :param open_now: Return only those places that are open for business at
                     the time the query is sent.
    :type open_now: bool

    :param types: Restricts the results to places matching at least one of the
                  specified types.
    :type types: string or list of strings

    :param page_token: Token from a previous search that when provided will
                       returns the next page of results for the same search.
    :type page_token: string

    :rtype: result dict with the following keys:
            results: list of places
            html_attributions: set of attributions which must be displayed
            next_page_token: token for retrieving the next page of results

    """
    params = {"query": query}

    if location:
        params["location"] = convert.latlng(location)
    if radius:
        params["radius"] = radius
    if language:
        params["language"] = language
    if min_price:
        params["minprice"] = min_price
    if max_price:
        params["maxprice"] = max_price
    if open_now:
        params["opennow"] = "true"
    if page_token:
        params["pagetoken"] = page_token

    return client._get("/maps/api/place/textsearch/json", params)


def place(client, place_id, language=None):
    """
    Comprehensive details for an individual place.

    :param place_id: A textual identifier that uniquely identifies a place,
                     returned from a Places search.
    :type place_id: string

    :param language: The language in which to return results.
    :type langauge: string

    :rtype: result dict with the following keys:
            result: dict containing place details
            html_attributions: set of attributions which must be displayed

    """
    params = {"placeid": place_id}
    if language:
        params["language"] = language
    return client._get("/maps/api/place/details/json", params)


def places_photo(client, photo_reference, max_width=None, max_height=None):
    """
    Downloads a photo from the Places API.

    :param photo_reference: A string identifier that uniquely identifies a
      photo, as provided by either a Places search or Places detail request.
    :type photo_reference: string

    :param max_width: Specifies the maximum desired width, in pixels.
    :type max_width: int

    :param max_height: Specifies the maximum desired height, in pixels.
    :type max_height: int

    :rtype: iterator containing the raw image data, which typically can be
      used to save an image file locally, eg:

    ```
    f = open(local_filename, 'wb')
    for chunk in client.photo(photo_reference, max_width=100):
        if chunk:
            f.write(chunk)
    f.close()
    ```

    """

    if not (max_width or max_height):
        raise ValueError("a max_width or max_height arg is required")

    params = {"photoreference": photo_reference}

    if max_width:
        params["maxwidth"] = max_width
    if max_height:
        params["maxheight"] = max_height

    # "extract_body" and "stream" args here are used to return an iterable
    # response containing the image file data, rather than converting from
    # json.
    response = client._get("/maps/api/place/photo", params,
                           extract_body=lambda response: response,
                           requests_kwargs={"stream": True})
    return response.iter_content()


def places_autocomplete(client, input_text, offset=None, location=None,
                        radius=None, language=None):
    """
    Returns Place predictions given a textual search query, such as
    "pizza near New York", and optional geographic bounds.

    :param input_text: The text query on which to search.
    :type input_text: string

    :param offset: The position, in the input term, of the last character
                   that the service uses to match predictions. For example,
                   if the input is 'Google' and the offset is 3, the
                   service will match on 'Goo'.
    :type offset: int

    :param location: The latitude/longitude value for which you wish to obtain the
                     closest, human-readable address.
    :type location: string, dict, list, or tuple

    :param radius: Distance in meters within which to bias results.
    :type radius: int

    :param language: The language in which to return results.
    :type langauge: string

    :rtype: list of predictions

    """

    params = {"input": input_text}

    if offset:
        params["offset"] = offset
    if location:
        params["location"] = convert.latlng(location)
    if radius:
        params["radius"] = radius
    if language:
        params["language"] = language

    response = client._get("/maps/api/place/queryautocomplete/json", params)
    return response["predictions"]
