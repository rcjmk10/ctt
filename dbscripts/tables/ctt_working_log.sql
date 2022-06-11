-- Table: public.ctt_working_log

-- DROP TABLE IF EXISTS public.ctt_working_log;

CREATE TABLE IF NOT EXISTS public.ctt_working_log
(
    log_id uuid[] NOT NULL,
    ticket_id character varying(30) COLLATE pg_catalog."default",
    user_id character varying(30) COLLATE pg_catalog."default",
    "ActionType" character varying(100) COLLATE pg_catalog."default",
    "Notes" character varying(100) COLLATE pg_catalog."default",
    "LogDateTime" timestamp with time zone,
    CONSTRAINT ctt_working_log_pk PRIMARY KEY (log_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.ctt_working_log
    OWNER to postgres;