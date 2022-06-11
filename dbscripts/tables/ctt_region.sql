-- Table: public.ctt_region

-- DROP TABLE IF EXISTS public.ctt_region;

CREATE TABLE IF NOT EXISTS public.ctt_region
(
    region_id uuid NOT NULL,
    region_name character varying(100) COLLATE pg_catalog."default",
    region_desc character varying(2000) COLLATE pg_catalog."default",
    geolocation character varying(200) COLLATE pg_catalog."default",
    "Status" integer,
    "CreatedDate" date,
    CONSTRAINT ctt_region_pk PRIMARY KEY (region_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.ctt_region
    OWNER to postgres;