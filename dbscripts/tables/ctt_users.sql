-- Table: public.ctt_users

-- DROP TABLE IF EXISTS public.ctt_users;

CREATE TABLE IF NOT EXISTS public.ctt_users
(
    user_id uuid NOT NULL,
    "EmailAddr" character varying(100) COLLATE pg_catalog."default",
    "Password" character varying(100) COLLATE pg_catalog."default",
    "FirstName" character varying(100) COLLATE pg_catalog."default",
    "LastName" character varying(100) COLLATE pg_catalog."default",
    "HiredDate" date,
    "WorkRole" character varying(100) COLLATE pg_catalog."default",
    "Status" integer,
    " region_id" character varying(30) COLLATE pg_catalog."default",
    CONSTRAINT ctt_users_pkey PRIMARY KEY (user_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.ctt_users
    OWNER to postgres;