-- copy and paste to the supabase sql editor
create extension if not exists "uuid-ossp";

create table public.users (
    id uuid references auth.users(id) on delete cascade primary key,
    name varchar(255) not null,
    email varchar(255) unique not null,
    role varchar(50) not null check (role in ('individual', 'organisation')),
    organisation_type varchar(100),
    organisation_description text,
    created_at timestamp with time zone default now(),
    updated_at timestamp with time zone default now()
);

create table public.listings (
    id serial primary key,
    user_id uuid references public.users(id) on delete cascade,
    category varchar(50) not null check (category in ('Food', 'Place')),
    cost_type varchar(50) not null check (cost_type in ('free', 'discounted', 'budget_friendly')),
    title varchar(255) not null,
    description text not null,
    lat decimal(10, 8) not null,
    lon decimal(11, 8) not null,
    image_url text,
    expiry_time timestamp with time zone,
    timings varchar(255),
    created_at timestamp with time zone default now(),
    updated_at timestamp with time zone default now()
);

create table public.subscriptions (
    id serial primary key,
    subscriber_id uuid references public.users(id) on delete cascade,
    followed_user_id uuid references public.users(id) on delete cascade,
    created_at timestamp with time zone default now(),
    unique(subscriber_id, followed_user_id)
);
