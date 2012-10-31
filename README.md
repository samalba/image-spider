About
=====

Image-Spider is a web crawler that seeks out images.

Because this was written for a code challenge, I used as few third-party
libraries as reasonable. My directions were to use only "dotcloud services", and
I think I've stuck to that fairly well.

Design Decisions:

The interface app is basic MVC with a REST interface and a very simple
[web front-end](http://imagespider-bkaplan.dotcloud.com/). The spider app is
a rather small amount of code, so I haven't imposed any conventional
architecture on it.

Under normal circumstances I would probably at least have relied on an router
framework for the MVC. But given that this is a relatively simple application,
it's acceptable.

Some general notes on the architecture:

* URLs are stored as a tree, thanks to Postgres's WITH RECURSIVE feature. This
  allows results for any given webpage from one job to also be applied to other
  jobs. The current expiry is 15 minutes, but this is arbitrary and adjustable.

* This interface code is separate from the spider code. Multiple spiders can be
  deployed simultaneously to share the workload.

* REST methods correspond to controller methods.

Shortcomings:

* I chose to use postgresql even though neo4j would have been a more appropriate
  choice for this app. It would have made the app more responsive, and its data
  better structured. But since neo4j support on dotCloud is still alpha, and
  I've had a variety of deployment setbacks already, I decided to stick with
  datastores I know will work. Switching to Neo4j would avoid the need to
  paginate results.

Possible Improvements:

* See the following TODO list for starters. I'll add more here as I think of it.
* A /jobs resource for listing all active jobs. It would be useful if the web
  interface provided a "stop" link for each of them.

TODO:

* The crawler (worker) works for me locally, but not yet on dotCloud.
* /result GET currently returns only images from the first 5000 pages found, and
  does not include pagination yet. This is because images are associated with
  URLs, not job ids. Using neo4j instead of postgres to store the tree would
  elimintate the need for pagination, although it might still be useful.
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
