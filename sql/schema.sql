--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: image_spider; Type: DATABASE; Schema: -; Owner: image_spider
--

CREATE DATABASE image_spider WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'en_US.UTF-8' LC_CTYPE = 'en_US.UTF-8';


ALTER DATABASE image_spider OWNER TO image_spider;

\connect image_spider

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

--
-- Name: add_webpages(text[], integer); Type: FUNCTION; Schema: public; Owner: bkaplan
--

CREATE FUNCTION add_webpages(in_child_urls text[], in_depth integer) RETURNS SETOF void
    LANGUAGE plpgsql
    AS $$

    DECLARE child_url text;
    DECLARE found_depth integer;

    BEGIN

    FOR child_url IN SELECT unnest(in_child_urls)
    LOOP
        BEGIN
            INSERT INTO webpages (url, depth) VALUES (child_url, in_depth);
            EXCEPTION WHEN unique_violation THEN
                SELECT depth INTO found_depth
                    FROM webpages WHERE url = child_url;
                IF in_depth > found_depth THEN
                    UPDATE webpages
                        SET webpages.depth = in_depth,
                        webpages.completion_datetime = NULL
                        WHERE url = child_url;
                END IF;
        END;
    END LOOP;

    END;

$$;


ALTER FUNCTION public.add_webpages(in_child_urls text[], in_depth integer) OWNER TO bkaplan;

--
-- Name: add_webpages(text, text[], integer); Type: FUNCTION; Schema: public; Owner: bkaplan
--

CREATE FUNCTION add_webpages(in_parent_url text, in_child_urls text[], in_depth integer) RETURNS SETOF void
    LANGUAGE plpgsql
    AS $$

    DECLARE child_url text;
    DECLARE parent_id integer;
    DECLARE child_id integer;

    BEGIN

    BEGIN
        INSERT INTO webpages (url) VALUES (in_parent_url);
        EXCEPTION WHEN unique_violation THEN -- do nothing
    END;

    SELECT id INTO parent_id FROM webpages WHERE webpages.url = in_parent_url;

    FOR child_url IN SELECT unnest(in_child_urls)
    LOOP
        BEGIN
            INSERT INTO webpages (url, depth) VALUES (child_url, in_depth);
            EXCEPTION WHEN unique_violation THEN
                UPDATE webpages SET depth = in_depth
                    WHERE webpages.url = child_url
                    AND webpages.depth < in_depth;
        END;
        SELECT id INTO child_id FROM webpages WHERE webpages.url = child_url;
        PERFORM parent FROM webpage_relations
            WHERE webpage_relations.parent = parent_id
            AND webpage_relations.child = child_id;
        IF NOT FOUND THEN
            INSERT INTO webpage_relations (parent, child)
                VALUES (parent_id, child_id);
        END IF;
    END LOOP;

    END;

$$;


ALTER FUNCTION public.add_webpages(in_parent_url text, in_child_urls text[], in_depth integer) OWNER TO bkaplan;

--
-- Name: complete_crawl(text); Type: FUNCTION; Schema: public; Owner: bkaplan
--

CREATE FUNCTION complete_crawl(in_url text) RETURNS SETOF void
    LANGUAGE plpgsql
    AS $$

    BEGIN

    UPDATE webpages SET completion_datetime = now()
        WHERE webpages.url = in_url;

    END;

$$;


ALTER FUNCTION public.complete_crawl(in_url text) OWNER TO bkaplan;

--
-- Name: get_images(integer[]); Type: FUNCTION; Schema: public; Owner: bkaplan
--

CREATE FUNCTION get_images(webpage_ids integer[]) RETURNS TABLE(url text)
    LANGUAGE plpgsql
    AS $$

    BEGIN

    RETURN QUERY SELECT images.url FROM images WHERE id IN (
        SELECT image_relations.image_id FROM image_relations
        WHERE image_relations.webpage_id = ANY (webpage_ids));

    END;

$$;


ALTER FUNCTION public.get_images(webpage_ids integer[]) OWNER TO bkaplan;

--
-- Name: get_tree(integer, integer); Type: FUNCTION; Schema: public; Owner: bkaplan
--

CREATE FUNCTION get_tree(in_parent_id integer, in_limit integer) RETURNS TABLE(parent_id integer, child_id integer)
    LANGUAGE plpgsql STABLE
    AS $$

    BEGIN

    RETURN QUERY WITH RECURSIVE t(parent, child) AS (
        SELECT parent, child
            FROM webpage_relations
            WHERE parent = in_parent_id
        UNION ALL
        SELECT t1.parent, t1.child
            FROM t t0, webpage_relations t1
            WHERE t0.child = t1.parent
    )
    SELECT parent, child FROM t
    LIMIT in_limit;

    END;

$$;


ALTER FUNCTION public.get_tree(in_parent_id integer, in_limit integer) OWNER TO bkaplan;

--
-- Name: get_webpage_info(text); Type: FUNCTION; Schema: public; Owner: bkaplan
--

CREATE FUNCTION get_webpage_info(in_url text, OUT id integer, OUT depth integer, OUT completion_datetime timestamp without time zone) RETURNS record
    LANGUAGE plpgsql
    AS $$

    BEGIN

    SELECT webpages.id, webpages.depth, webpages.completion_datetime
        INTO id, depth, completion_datetime
        FROM webpages WHERE webpages.url = in_url LIMIT 1;

    END;

$$;


ALTER FUNCTION public.get_webpage_info(in_url text, OUT id integer, OUT depth integer, OUT completion_datetime timestamp without time zone) OWNER TO bkaplan;

--
-- Name: relate_image(text, text); Type: FUNCTION; Schema: public; Owner: bkaplan
--

CREATE FUNCTION relate_image(in_webpage_url text, in_image_url text) RETURNS SETOF void
    LANGUAGE plpgsql
    AS $$

    DECLARE image_id integer;
    DECLARE webpage_id integer;

    BEGIN

    BEGIN
        INSERT INTO images (url) VALUES (in_image_url)
            RETURNING id INTO image_id;
        EXCEPTION WHEN unique_violation THEN
            SELECT id INTO image_id FROM images WHERE images.url = in_image_url;
    END;

    SELECT id INTO webpage_id FROM webpages WHERE webpages.url = in_webpage_url;

    INSERT INTO image_relations (image_id, webpage_id)
        VALUES (image_id, webpage_id);

    END;

$$;


ALTER FUNCTION public.relate_image(in_webpage_url text, in_image_url text) OWNER TO bkaplan;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: image_relations; Type: TABLE; Schema: public; Owner: image_spider; Tablespace: 
--

CREATE TABLE image_relations (
    image_id integer,
    webpage_id integer
);


ALTER TABLE public.image_relations OWNER TO image_spider;

--
-- Name: images; Type: TABLE; Schema: public; Owner: image_spider; Tablespace: 
--

CREATE TABLE images (
    id integer NOT NULL,
    url text
);


ALTER TABLE public.images OWNER TO image_spider;

--
-- Name: images_id_seq; Type: SEQUENCE; Schema: public; Owner: image_spider
--

CREATE SEQUENCE images_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.images_id_seq OWNER TO image_spider;

--
-- Name: images_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: image_spider
--

ALTER SEQUENCE images_id_seq OWNED BY images.id;


--
-- Name: webpage_relations; Type: TABLE; Schema: public; Owner: image_spider; Tablespace: 
--

CREATE TABLE webpage_relations (
    parent integer,
    child integer
);


ALTER TABLE public.webpage_relations OWNER TO image_spider;

--
-- Name: webpages; Type: TABLE; Schema: public; Owner: image_spider; Tablespace: 
--

CREATE TABLE webpages (
    id integer NOT NULL,
    url text,
    depth integer DEFAULT 0 NOT NULL,
    completion_datetime timestamp with time zone,
    CONSTRAINT depth_must_be_nonnegative CHECK ((depth >= 0))
);


ALTER TABLE public.webpages OWNER TO image_spider;

--
-- Name: webpages_id_seq; Type: SEQUENCE; Schema: public; Owner: image_spider
--

CREATE SEQUENCE webpages_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.webpages_id_seq OWNER TO image_spider;

--
-- Name: webpages_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: image_spider
--

ALTER SEQUENCE webpages_id_seq OWNED BY webpages.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: image_spider
--

ALTER TABLE ONLY images ALTER COLUMN id SET DEFAULT nextval('images_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: image_spider
--

ALTER TABLE ONLY webpages ALTER COLUMN id SET DEFAULT nextval('webpages_id_seq'::regclass);


--
-- Name: images_id_key; Type: CONSTRAINT; Schema: public; Owner: image_spider; Tablespace: 
--

ALTER TABLE ONLY images
    ADD CONSTRAINT images_id_key UNIQUE (id);


--
-- Name: images_url_key; Type: CONSTRAINT; Schema: public; Owner: image_spider; Tablespace: 
--

ALTER TABLE ONLY images
    ADD CONSTRAINT images_url_key UNIQUE (url);


--
-- Name: webpages_id_key; Type: CONSTRAINT; Schema: public; Owner: image_spider; Tablespace: 
--

ALTER TABLE ONLY webpages
    ADD CONSTRAINT webpages_id_key UNIQUE (id);


--
-- Name: webpages_url_key; Type: CONSTRAINT; Schema: public; Owner: image_spider; Tablespace: 
--

ALTER TABLE ONLY webpages
    ADD CONSTRAINT webpages_url_key UNIQUE (url);


--
-- Name: image_relations_image_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: image_spider
--

ALTER TABLE ONLY image_relations
    ADD CONSTRAINT image_relations_image_id_fkey FOREIGN KEY (image_id) REFERENCES images(id) ON DELETE CASCADE;


--
-- Name: image_relations_webpage_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: image_spider
--

ALTER TABLE ONLY image_relations
    ADD CONSTRAINT image_relations_webpage_id_fkey FOREIGN KEY (webpage_id) REFERENCES webpages(id) ON DELETE CASCADE;


--
-- Name: webpage_relations_child_fkey; Type: FK CONSTRAINT; Schema: public; Owner: image_spider
--

ALTER TABLE ONLY webpage_relations
    ADD CONSTRAINT webpage_relations_child_fkey FOREIGN KEY (child) REFERENCES webpages(id) ON DELETE CASCADE;


--
-- Name: webpage_relations_parent_fkey; Type: FK CONSTRAINT; Schema: public; Owner: image_spider
--

ALTER TABLE ONLY webpage_relations
    ADD CONSTRAINT webpage_relations_parent_fkey FOREIGN KEY (parent) REFERENCES webpages(id) ON DELETE CASCADE;


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

