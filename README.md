About
=====

Image-Spider is a web crawler that seeks out images.

Because this was written for a code challenge, I used as few third-party
libraries as reasonable. My directions were to use only "dotcloud services", and
I think I've stuck to that fairly well. In practice this entire piece of code
could have been handled by third-party software, but that wouldn't have been
much of a code challenge.

Design Decisions:

The interface app is basic MVC with a REST interface and a very simple
[web front-end](http://imagespider-bkaplan.dotcloud.com/). The spider app is
a rather small amount of code, so I haven't imposed any conventional
architecture on it.

Under normal circumstances I would probably at least have relied on an router
framework for the MVC. I also would probably have used a scraper such as Scrapy.
Given that this is a relatively simple application, it's acceptable.

Some general notes on the architecture:

* URLs are stored as a tree, thanks to Postgres's WITH RECURSIVE feature. This
  allows results for any given webpage from one job to also be applied to other
  jobs. The current expiry is 15 minutes, but this is arbitrary and adjustable.

* This interface code is separate from the spider code. Multiple spiders can be
  deployed simultaneously to share the workload. The spiders are written so as
  to use dotCloud workers, as requested. Otherwise I would probably have chosen
  to use a python pool of workers, to gain more programmatic control over them.

* REST methods correspond to controller methods.

Shortcomings:

* I chose to use postgresql even though neo4j would have been a more appropriate
  choice for this app. It would have made the app more responsive for deep
  crawls, and its data better structured. But since neo4j support on dotCloud is
  still alpha, and I've had a variety of deployment setbacks already, I decided
  to stick with datastores I know will work.

* DELETE /result should require HTTP auth. The only reason it doesn't is because
  this app is a code demonstration, not intended for production use. HTTP auth
  would be an unnecessary barrier in this case.

* DELETE /result accepts a url parameter, but not job_id. It would be nice to
  offer DELETE for a specified job_id, to remove that job and its results from
  the datastores. Unfortunately the architecture does not permit this because
  URLs are stored only once for any multiple jobs that crawl to them. This means
  that deleting one job could easily delete part of other jobs. If this was
  a required feature, a solution would be (using Postgres):
    * Store an array of job_ids for each webpage URL and each image. This would
      require a lot of redundant information, and would counter the design of
      the current architecture, but would allow us to solve for DELETE.
    * On DELETE of a job_id, begin with the requested webpages at the root of
      the search tree. Apply the following function to each of them.
    * Function:
        * Remove the specified job_id from the webpage's array.
        * Find all images related to that webpage. For each image, remove the
          specified job_id from the image's array.
        * If the image's array is empty then delete that image.
        * For each child of the webpage, recursively apply this function.
        * If the webpage's array is empty then delete that webpage.

Possible Improvements:

* See the following TODO list for starters. I'll add more here as I think of it.

* It would be nice to have a /jobs resource to GET a list of all jobs.

TODO:

* Test coverage is incomplete.
* Aborted jobs are not restarted.

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

* Description: Initiate crawling at the specified URLs.
* QueryString options:
    * `depth`: optional integer, default=2.
* PostData:
    * `urls`: form-urlencoded string of newline separated URLs
  assigned to a `urls` parameter.
* Returns:
    * Status: `202 Accepted` (prior to processing)
    * Content-type: `application/json`
    * Content: `{"job_id":n}`


Resource: /status
-----------------

*** Method: GET ***

* Description: Get the crawler status for the specified URL.
* QueryString options:
    * `job_id`: integer job id, required if url is not specified.
    * `url`: string url, required if job id is not specified.
* Returns:
    * Status: `200` or `404` (depending on URL)
    * Content-type: application/json
    * Content: JSON object having the following properties:
        * `urls`: list of URLs processed for job, excluding any cached results.
        * `job_status`: Either a object or a array of objects; if you request by
                        job_id then it will be a object -- if you request by url
                        then it will be a array of objects (because multiple
                        jobs may have crawled the same URL). In either case, the
                        object(s) will contain the following:
            * `total_depth`: Depth at which a spider was instructed to begin.
            * `current_depth`: Depth at which a spider is currently crawling.
            * `total_pages_completed`: Total pages completed.
            * `depth_percent_complete`: Percent of the current depth complete.
            * `pages_completed_at_depth`: Pages completed at current depth.
            * `pages_completed_at_greater_depth`: Pages done at prior depths.
            * `total_pages_at_depth`: Pages count of current depth.
            * `total_pages_queued`: Count of pages queued so far at any depth.


Resource: /result
-----------------

*** Method: GET ***

* Description: Get the result set for the specified URL.
* QueryString options:
    * `job_id`: integer job id, required if url is not specified.
    * `url`: string url, required if job id is not specified.
* Returns:
    * Status: `200` or `404` (depending on URL)
    * Content-type: application/json
    * Content: [img-url, img-url, img-url, &hellip;]

*** Method: DELETE ***

* Description: Delete the result set for the specified URL, including any
               associated images, any descendant children URLs, and any images
               associated with them. Note: If any jobs are currently crawling
               those URLs, they will be aborted.
* QueryString options:
    * `url`: string url.
* Returns:
    * Status: `204 No Content` or `404 Not Found` (depending on URL)

Resource: /stop
---------------

*** Method: POST ***

* Description: Stop crawling the specified URL.
* QueryString options:
    * `job_id`: integer job id.
* Returns:
    * Status: `202 Accepted` (prior to processing) or `404 Not Found` (depending
      on job_id)
