CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  role TEXT DEFAULT 'user', -- agent / admin / seller
  password_hash TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT now()
);
CREATE TABLE locations (
  id SERIAL PRIMARY KEY,
  address TEXT,
  google_maps_link TEXT
);
CREATE TABLE properties (
  id SERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  description TEXT,
  price NUMERIC NOT NULL,
  property_type TEXT, -- house, apartment, land
  bedrooms INT,
  bathrooms INT,
  area_sqm INT,
  photo_location TEXT[],
  status TEXT DEFAULT 'available', -- sold, pending

  owner_id INT REFERENCES users(id),
  location_id INT REFERENCES locations(id),

  created_at TIMESTAMP DEFAULT now()
);
