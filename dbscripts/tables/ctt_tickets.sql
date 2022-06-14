-- Table: public.ctt_tickets

-- DROP TABLE IF EXISTS public.ctt_tickets;

CREATE TABLE IF NOT EXISTS public.ctt_tickets
(
    ticket_id uuid NOT NULL,
    "TowerID" character varying(100) COLLATE pg_catalog."default",
    "TowerStreet" character varying(100) COLLATE pg_catalog."default",
    "ModuleID" character varying(100) COLLATE pg_catalog."default",
    "ErrorCode" character varying(100) COLLATE pg_catalog."default",
    "ErrorDetails" character varying(2000) COLLATE pg_catalog."default",
    "ErrorDateTime" character varying(100) COLLATE pg_catalog."default",
    "AssignedUser_ID" character varying(30) COLLATE pg_catalog."default",
    "AssignedDateTime" character varying(100) COLLATE pg_catalog."default",
    "Ticket_Status" character varying(30) COLLATE pg_catalog."default",
    "CompletedDateTime" character varying(100) COLLATE pg_catalog."default",
    "Longitude" character varying(100) COLLATE pg_catalog."default",
    "Latitude" character varying(100) COLLATE pg_catalog."default",
    geom geometry,
    CONSTRAINT ctt_tickets_pkey PRIMARY KEY (ticket_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.ctt_tickets
    OWNER to postgres;