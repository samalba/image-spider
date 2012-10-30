Documentation
=============

Resource: /
-----------

*** Method: GET ***

* Description: View app UI and documentation.
* Returns:
    * Status: `200 OK`
    * Content-type: `text/html`
    * Content: App UI and documentation (README.md) &mdash;
      *You're looking at it.*

*** Method: POST ***

* Description: Initiate crawling at the specified URLs. Specify depth with the
  'depth' querystring. Default depth is 2. Post-data:
  `urls=<URL>\n<URL>\n<URL>\n`&hellip; newline separated, form-urlencoded URLs
  assigned to a `urls` parameter.
* Returns:
    * Status: `202 Accepted` (prior to processing)
    * Content-type: `application/json`
    * Content: `{"job_id":n}`


Resource: /status?job_id=`<JOB_ID>` or ?url=`<URL>`
----------------------------------------------------

*** Method: GET ***

* Description: Get the crawler status for the specified URL.
* Returns:
    * Status: `200` or `404` (depending on URL)
    * Content-type: application/json
    * Content: JSON object having the following properties:
        * url
            * *TODO*
        * job_status
            * `total_depth`: Depth at which a spider was instructed to begin.
            * `current_depth`: Depth at which a spider is currently crawling.
            * `total_pages_completed`: Total pages completed.
            * `depth_percent_complete`: Percent of the current depth complete.
            * `pages_completed_at_depth`: Pages completed at current depth.
            * `pages_completed_at_greater_depth`: Pages done at prior depths.
            * `total_pages_at_depth`: Pages count of current depth.
            * `total_pages_queued`: Count of pages queued so far at any depth.


Resource: /result?job_id=`<JOB_ID>` or ?url=`<URL>`
----------------------------------------------------

*** Method: GET ***

* Description: Get the result set for the specified URL.
* Returns:
    * Status: `200` or `404` (depending on URL)
    * Content-type: application/json
    * Content: [img-url, img-url, img-url, &hellip;]

*** Method: DELETE ***

* Description: Delete the result set for the specified URL.
* Returns:
    * Status: `204` or `404` (depending on URL) -- *Should require HTTP auth.*

Resource: /stop?job_id=`<JOB_ID>` or ?url=`<URL>`
--------------------------------------------------

*** Method: POST ***

* Description: Stop crawling the specified URL.
* Returns:
    * Status: `204` or `404` (depending on URL)

Issues
======

* `pip install dotcloud` fails on Arch Linux because the scripts assume python2
  is the installed version of python.
* pl/python seems unavailable.
* requirements.txt is not installing.
