DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS seats;
DROP TABLE IF EXISTS events;

CREATE TABLE events(
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    venue TEXT NOT NULL,
    starts_at TIMESTAMPTZ NOT NULL,
    created TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT name_not_blank CHECK (length(trim(name)) > 0)
);

CREATE TABLE seats (
    id BIGSERIAL PRIMARY KEY,
    event_id BIGINT NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    seat_no INT NOT NULL,
    status TEXT NOT NULL DEFAULT 'available',
    CONSTRAINT status_is_known CHECK (status IN ('available', 'booked')),
    CONSTRAINT seat_no_is_positive CHECK (seat_no > 0),
    CONSTRAINT one_seat_no_per_event UNIQUE (event_id, seat_no)
);
CREATE INDEX seats_event_status_idx ON seats (event_id, status);

CREATE TABLE bookings (
    id BIGSERIAL PRIMARY KEY,
    seat_id BIGINT NOT NULL REFERENCES seats(id) ON DELETE CASCADE,
    user_email TEXT NOT NULL,
    created TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT one_booking_per_seat UNIQUE (seat_id)
);