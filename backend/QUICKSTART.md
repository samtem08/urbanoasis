# Quick Start Guide - Urban Oasis Backend

Get your backend up and running in 5 minutes!

## Prerequisites
- Python 3.8+ installed
- Basic command line knowledge

## Installation (Choose your OS)

### For Mac/Linux:

```bash
# 1. Navigate to backend folder
cd urban_oasis_backend

# 2. Run setup script
./setup.sh

# 3. Create admin user
python manage.py createsuperuser

# 4. Load sample data (optional)
python manage.py loaddata initial_data.json

# 5. Start server
python manage.py runserver
```

### For Windows:

```cmd
# 1. Navigate to backend folder
cd urban_oasis_backend

# 2. Run setup script
setup.bat

# 3. Create admin user
python manage.py createsuperuser

# 4. Load sample data (optional)
python manage.py loaddata initial_data.json

# 5. Start server
python manage.py runserver
```

## Manual Installation (if scripts don't work)

```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate it
# Mac/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 3. Install packages
pip install -r requirements.txt

# 4. Create database
python manage.py makemigrations
python manage.py migrate

# 5. Create admin user
python manage.py createsuperuser

# 6. Start server
python manage.py runserver
```

## Access Your Backend

Once the server is running:

### Admin Panel
- URL: http://127.0.0.1:8000/admin/
- Login with the superuser credentials you created

### API
- Base URL: http://127.0.0.1:8000/api/
- Try: http://127.0.0.1:8000/api/pricing/

## First Steps in Admin Panel

1. **Go to http://127.0.0.1:8000/admin/**

2. **Log in** with your superuser credentials

3. **Add a Pricing Rule:**
   - Click "Pricing Rules" → "Add Pricing Rule"
   - Set name: "Standard Rate"
   - Set base price: 125
   - Set cleaning fee: 75
   - Click "Save"

4. **Upload Gallery Images:**
   - Click "Gallery Images" → "Add Gallery Image"
   - Upload an image
   - Set title and category
   - Click "Save"

5. **Add Amenities:**
   - Click "Amenities" → "Add Amenity"
   - Add items like "Free WiFi", "Parking", etc.
   - Click "Save"

## Test the API

Open your browser and visit:

- **All pricing:** http://127.0.0.1:8000/api/pricing/
- **Gallery images:** http://127.0.0.1:8000/api/gallery/
- **Amenities:** http://127.0.0.1:8000/api/amenities/
- **Reviews:** http://127.0.0.1:8000/api/reviews/
- **Settings:** http://127.0.0.1:8000/api/settings/

## Connect to Your Frontend

In your frontend JavaScript, add:

```javascript
const API_BASE_URL = 'http://127.0.0.1:8000/api';

// Example: Load pricing
async function loadPricing() {
  const response = await fetch(`${API_BASE_URL}/pricing/`);
  const data = await response.json();
  console.log(data.results);
}

loadPricing();
```

## Common Issues

### Port 8000 already in use?
```bash
# Run on different port
python manage.py runserver 8080
```

### Can't see uploaded images?
- Make sure DEBUG=True in settings.py
- Check that media files URL is correct in settings.py
- Images are at: http://127.0.0.1:8000/media/gallery/...

### CORS errors from frontend?
- Check that django-cors-headers is installed
- Verify CORS settings in settings.py

## Next Steps

1. Read the full README.md for detailed documentation
2. Check API_DOCUMENTATION.md for all API endpoints
3. Explore the admin panel features
4. Connect your frontend to the API

## Need Help?

- Check README.md for troubleshooting
- Review API_DOCUMENTATION.md for endpoint details
- Email: hello@urbanoasis.com

---

**You're all set! 🎉**

The backend is now running and ready to manage your Urban Oasis rental property!
