import json
import psycopg2

def clean_number(num_str):
    """Convert strings like '308,362' to int 308362."""
    if not num_str:
        return None
    return int(num_str.replace(',', ''))

# Load JSON file (adjust path as needed)
file_path = "./data/metadata/images_metadata.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="unsplash_master_db",
    user="postgres",
    password="135790"
)
cursor = conn.cursor()

# Cache dictionaries to avoid redundant DB lookups
photographer_cache = {}
location_cache = {}
tag_cache = {}

def get_or_create_photographer(name):
    if not name:
        return None
    if name in photographer_cache:
        return photographer_cache[name]
    cursor.execute("SELECT photographer_id FROM photographers WHERE name = %s;", (name,))
    res = cursor.fetchone()
    if res:
        photographer_cache[name] = res[0]
        return res[0]
    cursor.execute("INSERT INTO photographers (name) VALUES (%s) RETURNING photographer_id;", (name,))
    pid = cursor.fetchone()[0]
    conn.commit()
    photographer_cache[name] = pid
    return pid

def get_or_create_location(location_name):
    if not location_name:
        return None
    if location_name in location_cache:
        return location_cache[location_name]
    cursor.execute("SELECT location_id FROM locations WHERE location_name = %s;", (location_name,))
    res = cursor.fetchone()
    if res:
        location_cache[location_name] = res[0]
        return res[0]
    cursor.execute("INSERT INTO locations (location_name) VALUES (%s) RETURNING location_id;", (location_name,))
    lid = cursor.fetchone()[0]
    conn.commit()
    location_cache[location_name] = lid
    return lid

def get_or_create_tag(tag_name):
    if not tag_name:
        return None
    if tag_name in tag_cache:
        return tag_cache[tag_name]
    cursor.execute("SELECT tag_id FROM tags WHERE tag_name = %s;", (tag_name,))
    res = cursor.fetchone()
    if res:
        tag_cache[tag_name] = res[0]
        return res[0]
    cursor.execute("INSERT INTO tags (tag_name) VALUES (%s) RETURNING tag_id;", (tag_name,))
    tid = cursor.fetchone()[0]
    conn.commit()
    tag_cache[tag_name] = tid
    return tid

for item in data:
    # Clean numeric fields
    views = clean_number(item.get("views"))
    downloads = clean_number(item.get("downloads"))
    
    photographer_id = get_or_create_photographer(item.get("photographer_name"))
    location_id = get_or_create_location(item.get("location"))
    
    # Insert into images table
    cursor.execute("""
        INSERT INTO images
        (image_url, description, photographer_id, location_id, views, downloads, published_time, license)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING image_id;
    """, (
        item.get("image_url"),
        item.get("description"),
        photographer_id,
        location_id,
        views,
        downloads,
        item.get("published_time"),
        item.get("license")
    ))
    image_id = cursor.fetchone()[0]
    conn.commit()
    
    # Insert tags and link in image_tags
    tags = item.get("tags", [])
    for tag in tags:
        tag_id = get_or_create_tag(tag)
        if tag_id:
            # Use ON CONFLICT DO NOTHING to avoid duplicates if supported (Postgres)
            cursor.execute("""
                INSERT INTO image_tags (image_id, tag_id) VALUES (%s, %s)
                ON CONFLICT DO NOTHING;
            """, (image_id, tag_id))
    conn.commit()

print("Data loaded successfully!")

cursor.close()
conn.close()
