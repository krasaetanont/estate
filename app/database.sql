
CREATE TYPE property_status_enum AS ENUM ('available', 'sold', 'pending');
CREATE TYPE user_role_enum AS ENUM ('user', 'admin', 'seller');
CREATE TYPE listing_type_enum AS ENUM ('sale', 'rent');

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  user_role user_role_enum DEFAULT 'user',
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
  google_maps_link TEXT,
  latitude NUMERIC,
  longitude NUMERIC
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
  views_count INT DEFAULT 0,
  property_status property_status_enum DEFAULT 'available',
  listing_type listing_type_enum DEFAULT 'sale', -- sale or rent
  rent_period TEXT, -- e.g., 'month', 'year' (only for rentals)

  owner_id INT REFERENCES users(id),
  location_id INT REFERENCES locations(id),

  created_at TIMESTAMP DEFAULT now(),
  updated_at TIMESTAMP DEFAULT now()
);
-- Track user favorites/saved properties
CREATE TABLE favorites (
  id SERIAL PRIMARY KEY,
  user_id INT REFERENCES users(id) ON DELETE CASCADE,
  property_id INT REFERENCES properties(id) ON DELETE CASCADE,
  created_at TIMESTAMP DEFAULT now(),
  UNIQUE(user_id, property_id)
);


CREATE TABLE property_photos (
  id SERIAL PRIMARY KEY,
  property_id INT REFERENCES properties(id) ON DELETE CASCADE,
  url TEXT NOT NULL,
  is_primary BOOLEAN DEFAULT FALSE,
  sort_order INT DEFAULT 0
);

CREATE INDEX idx_properties_price ON properties(price);
CREATE INDEX idx_properties_location ON properties(location_id);
CREATE INDEX idx_properties_status ON properties(property_status);
CREATE INDEX idx_properties_owner ON properties(owner_id);
CREATE INDEX idx_properties_type ON properties(property_type);
CREATE INDEX idx_favorites_user ON favorites(user_id);
CREATE INDEX idx_property_photos_property ON property_photos(property_id);