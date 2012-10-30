About
=====

Image-Spider is a web crawler that seeks out images.

TODO:

* The crawler (worker) works for me locally, but not yet on dotCloud.
* /result GET currently returns only images from the first 5000 pages found, and
  does not (yet) include pagination. This is because images are associated with
  URLs, not job ids. They should be associated with both, in order to reteive
  all of them, although in this case pagination may still be desirable. Another,
  more appropriate, solution for eliminating the need for pagination would be to
  use neo4j instead of postgres to store the tree. This is what I wanted to do
  at first, but dotCloud only offers alpha support for it, and getting it up and
  running seemed like it might take too much time.
* /result DELETE is unimplemented. It should require HTTP auth.
* /status GET should support url parameter.
* /stop POST is unimplemented.
* Test coverage is incomplete.

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
    * Status: `204` or `404` (depending on URL)

Resource: /stop?job_id=`<JOB_ID>` or ?url=`<URL>`
--------------------------------------------------

*** Method: POST ***

* Description: Stop crawling the specified URL.
* Returns:
    * Status: `204` or `404` (depending on URL)
