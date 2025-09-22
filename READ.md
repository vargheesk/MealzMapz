# MealzMapz

### Reduce Food Waste, Feed Communities

MealzMapz is an interactive web platform designed to connect food donors with people in need, helping to reduce food waste and support communities. The application allows users to share surplus food, discover free or affordable meals in their vicinity, and add community places that provide food assistance.

**Live Preview:** [https://mealmap-8aw4.onrender.com/](https://mealmap-8aw4.onrender.com/)

---

### Key Features

* **User Authentication**: Users can sign up for an account as an "Individual" or an "Organisation" and log in securely. Email verification is required to complete the registration process.
* **Interactive Map View**: Users can explore available food posts and community places on a map, with the option to filter by a specific radius from their current location.
* **Food and Place Listings**: The platform features a dedicated page to browse all listings, which can be filtered by category (Food or Place), cost type (Free, Discounted, or Budget Friendly), and sorted by date, distance, or expiry time.
* **Post Creation**: Authenticated users can add new listings for surplus food or community places by providing details like title, description, location (via a map pin or current location), and other relevant information.
* **Profile Management**: Users have a personal profile page to view their own posts and places, edit their profile details, and manage their listings.
* **Follower Notifications**: When a user adds a new food post, their followers are automatically notified via email.
* **Automated Maintenance**: The application automatically deletes expired listings to ensure all information is up-to-date.

---

### Technologies Used

* **Frontend**: HTML, Tailwind CSS, JavaScript, and Jinja2 for templating.
* **Backend**: Flask (Python).
* **Database**: Supabase (PostgreSQL) for user data, listings, and subscriptions.
* **Mapping**: Leaflet.js and OpenStreetMap for interactive maps.
* **Python Modules**: The core Python modules used in the backend include **Flask**, **Flask-Mail**, **python-dotenv**, and the **supabase** library.
* **Deployment**: The application is configured to be deployed on Render with **gunicorn** as the web server.

---

### Getting Started

1.  **Clone the Repository**:
    ```bash
    git clone [https://github.com/vargheesk/MealzMapz](https://github.com/vargheesk/MealzMapz)
    ```
2.  **Navigate to the Directory**:
    ```bash
    cd MealzMapz
    ```
3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
   
4.  **Environment Variables**: Create a `.env` file in the root directory and add the following variables based on your Supabase and email service configurations:
    ```
    SECRET_KEY=your-secret-key-here
    SUPABASE_URL=your-supabase-url
    SUPABASE_KEY=your-supabase-key
    MAIL_SERVER=your-mail-server
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_USERNAME=your-mail-username
    MAIL_PASSWORD=your-mail-password
    MAIL_DEFAULT_SENDER=your-default-sender
    ```
    (Note: The `.env` file is ignored by Git for security).
5.  **Run the Application**:
    ```bash
    gunicorn app:app
    ```