CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  role TEXT DEFAULT 'user', -- agent / admin / seller
  password_hash TEXT NOT NULL,
  phone_number TEXT,
  is_verified BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT now()
);
CREATE TABLE locations (
  id SERIAL PRIMARY KEY,
  city TEXT NOT NULL,
  province TEXT,
  country TEXT NOT NULL,
  postal_code TEXT,
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
  views_count INT DEFAULT 0,
  status TEXT DEFAULT 'available', -- sold, pending

  owner_id INT REFERENCES users(id),
  location_id INT REFERENCES locations(id),

  created_at TIMESTAMP DEFAULT now()
);
-- Track user favorites/saved properties
CREATE TABLE favorites (
  id SERIAL PRIMARY KEY,
  user_id INT REFERENCES users(id) ON DELETE CASCADE,
  property_id INT REFERENCES properties(id) ON DELETE CASCADE,
  created_at TIMESTAMP DEFAULT now(),
  UNIQUE(user_id, property_id)
);