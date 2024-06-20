
create table
  public.user_types (
    type_name character varying(20) not null,
    constraint user_types_pkey primary key (type_name)
  ) tablespace pg_default;

insert into public.user_types (type_name) values ('admin'),('basic'), ('premium'), ('business');

create table
  public.users (
    user_id uuid not null,
    suspended boolean null default false,
    user_type character varying null,
    disabled boolean not null default false,
    constraint account_pkey primary key (user_id),
    constraint account_user_id_fkey foreign key (user_id) references auth.users (id),
    constraint users_user_type_fkey foreign key (user_type) references user_types (type_name)
  ) tablespace pg_default;
  
create table
  public.billing (
    user_id uuid not null,
    state character varying(255) null,
    city character varying(255) null,
    street character varying(255) null,
    unit character varying(50) null,
    postalcode character varying(20) null,
    credit_card_no bigint null,
    credit_card_cvv smallint null,
    credit_card_expiry date null,
    full_name text null,
    constraint billing_pkey primary key (user_id),
    constraint billing_user_id_fkey1 foreign key (user_id) references users (user_id) on update cascade
  ) tablespace pg_default;
  
create table
  public.suspension (
    suspension_id serial,
    user_id uuid null,
    admin_id uuid null,
    start_date timestamp without time zone null,
    duration interval null,
    end_date timestamp without time zone null generated always as (start_date + duration) stored,
    reason text null,
    constraint suspension_pkey primary key (suspension_id),
    constraint suspension_suspensionid_key unique (suspension_id),
    constraint suspension_admin_id_fkey foreign key (admin_id) references users (user_id),
    constraint suspension_user_id_fkey1 foreign key (user_id) references users (user_id)
  ) tablespace pg_default;
  
create table
  public.reports_on_user (
    report_id serial,
    reporter_id uuid null,
    reportee_id uuid null,
    reason text null,
    constraint reports_on_user_pkey primary key (report_id),
    constraint reports_on_user_reportee_id_fkey1 foreign key (reportee_id) references users (user_id),
    constraint reports_on_user_reporter_id_fkey1 foreign key (reporter_id) references users (user_id)
  ) tablespace pg_default;
  
create table
  public.platforms (
    platform_name character varying(50) not null,
    constraint platforms_pkey primary key (platform_name)
  ) tablespace pg_default;

insert into public.platforms (platform_name) values ('Facebook'),('Instagram'), ('Facebook page');
  
create table
  public.platform_account (
    platform_account_id bigint not null,
    user_id uuid null,
    platform character varying null,
    constraint platform_account_pkey primary key (platform_account_id),
    constraint platform_account_platform_fkey foreign key (platform) references platforms (platform_name),
    constraint platform_account_user_id_fkey foreign key (user_id) references users (user_id)
  ) tablespace pg_default;
  
create table
  public.post_types (
    post_type character varying(20) not null,
    constraint post_types_pkey primary key (post_type)
  ) tablespace pg_default;

-- needs work
CREATE TABLE public.platform_followers_demographic_ (
    
  )

CREATE TABLE public.platform_metrics (
    platform_metrics_id serial PRIMARY KEY, -- auto generated, you do not need to fill this column
    platform_account bigint,
    platform_account_views integer,
    platform_followers integer,
    platform_likes bigint,
    platform_comments integer,
    platform_saves integer,
    platform_shares integer,
    platform_impressions integer,
    platform_reach integer,
    platform_virality_rate numeric GENERATED ALWAYS AS (platform_shares::numeric / NULLIF(platform_impressions, 0)) STORED,
    platform_amplification_rate numeric GENERATED ALWAYS AS (platform_shares::numeric / NULLIF(platform_followers, 0)) STORED,
    platform_engagement_rate numeric GENERATED ALWAYS AS ((platform_likes + platform_shares + platform_comments)::numeric / NULLIF(platform_followers, 0)) STORED,
    platform_sentiment smallint,          -- auto generated, you do not need to fill this column
    date_retrieved timestamp DEFAULT now(),
    CONSTRAINT platform_metrics_platform_account_fkey FOREIGN KEY (platform_account) REFERENCES platform_account (platform_account_id)
) TABLESPACE pg_default;

CREATE TABLE public.post_metrics (
    post_metric_id SERIAL PRIMARY KEY,  -- auto generated, you do not need to fill this column
    post_id bigint,
    platform_account bigint,
    post_type character varying(20),
    post_likes integer,
    post_shares integer,
    post_saved integer,
    post_comments integer,
    post_impressions integer,
    post_reach integer,
    post_profile_views integer,
    post_virality_rate numeric GENERATED ALWAYS AS (post_shares::numeric / NULLIF(post_impressions, 0)) STORED,
    post_amplification_rate numeric,    -- auto generated, you do not need to fill this column
    post_engagement_rate numeric GENERATED ALWAYS AS ((post_likes + post_shares + post_comments)::numeric / NULLIF(post_reach, 0)) STORED,
    post_sentiment smallint,
    date_retrieved timestamp DEFAULT now(),
    CONSTRAINT post_metrics_platform_account_fkey FOREIGN KEY (platform_account) REFERENCES platform_account (platform_account_id)
) TABLESPACE pg_default;

-- team table
-- drafts table



-- function to update the post_amplification_rate column in the post_metrics table
CREATE OR REPLACE FUNCTION update_post_amplification_rate()
RETURNS TRIGGER AS $$
DECLARE
    follower_count INTEGER;
BEGIN
    -- Retrieve the latest follower count for the platform account from the platform_metrics table
    SELECT platform_followers
    INTO follower_count
    FROM platform_metrics
    WHERE platform_account = NEW.platform_account
    ORDER BY date_retrieved DESC
    LIMIT 1;

    -- Calculate and update the post_amplification_rate
    UPDATE post_metrics
    SET post_amplification_rate = CASE 
                                    WHEN follower_count = 0 THEN NULL 
                                    ELSE NEW.post_shares::numeric / follower_count 
                                  END
    WHERE post_id = NEW.post_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- fcuntion to update the platform_sentiment column in the platform_metrics table
CREATE TRIGGER trg_update_post_amplification_rate
AFTER INSERT OR UPDATE ON post_metrics
FOR EACH ROW
EXECUTE FUNCTION update_post_amplification_rate();

CREATE OR REPLACE FUNCTION update_platform_sentiment()
RETURNS TRIGGER AS $$
DECLARE
    avg_sentiment NUMERIC;
BEGIN
    -- Calculate the average sentiment for the platform account
    SELECT AVG(post_sentiment)
    INTO avg_sentiment
    FROM post_metrics
    WHERE platform_account = NEW.platform_account;

    -- Update the platform_sentiment in the platform_metrics table
    UPDATE platform_metrics
    SET platform_sentiment = avg_sentiment
    WHERE platform_account = NEW.platform_account;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_platform_sentiment
AFTER INSERT OR UPDATE OR DELETE ON post_metrics
FOR EACH ROW
EXECUTE FUNCTION update_platform_sentiment();
