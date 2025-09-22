# 🍽️ MealzMapz

### 🌍 Reduce Food Waste, Feed Communities

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Visit%20Now-brightgreen)](https://mealmap-8aw4.onrender.com/)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/vargheesk/MealzMapz)
[![Python](https://img.shields.io/badge/Python-3.8+-yellow)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-red)](https://flask.palletsprojects.com/)
[![Supabase](https://img.shields.io/badge/Supabase-Database-green)](https://supabase.com/)

MealzMapz is an innovative web platform that bridges the gap between food donors and communities in need. Our mission is to reduce food waste while ensuring that surplus food reaches those who can benefit from it most.

---

## 🚀 Live Application

Experience MealzMapz in action: **[Link](https://mealmap-8aw4.onrender.com/)**

---

## ✨ Key Features

### 🔐 **Secure Authentication System**
- User registration with email verification
- Support for both Individual and Organization accounts
- Role-based access control and profile management

### 🗺️ **Interactive Mapping Experience**
- Real-time map visualization using Leaflet.js and OpenStreetMap
- Location-based filtering with customizable radius
- GPS integration for accurate positioning

### 📱 **Comprehensive Listing Management**
- Browse food posts and community places with advanced filtering
- Category-based sorting (Food/Place, Free/Discounted/Budget Friendly)
- Distance and expiry-based organization

### ✍️ **Content Creation Tools**
- Intuitive forms for adding surplus food listings
- Community place registration with detailed information
- Image upload support and location pinning

### 👤 **Personal Profile Dashboard**
- Centralized view of user's posts and places
- Profile editing and account management
- Listing modification and deletion capabilities

### 📧 **Automated Notification System**
- Email notifications for followers when new food posts are created
- Real-time updates for community engagement

### 🔧 **Smart Maintenance**
- Automatic removal of expired listings
- Database optimization for current information

---

## 🛠️ Technology Stack

### **Frontend Technologies**
- 🎨 **HTML5** - Semantic markup and structure
- 🎨 **Tailwind CSS** - Modern, utility-first styling
- ⚡ **JavaScript** - Dynamic user interactions
- 🔄 **Jinja2** - Server-side templating

### **Backend Infrastructure**
- 🐍 **Flask** - Lightweight Python web framework
- 📧 **Flask-Mail** - Email integration and notifications
- 🗄️ **Supabase** - PostgreSQL database with real-time capabilities
- 🔑 **Supabase Auth** - Authentication and user management

### **Mapping and Location Services**
- 🗺️ **Leaflet.js** - Interactive mapping library
- 🌍 **OpenStreetMap** - Open-source map data
- 📍 **Geolocation API** - Browser-based location services

### **Deployment and Production**
- 🚀 **Render** - Cloud application hosting
- 🦄 **Gunicorn** - Python WSGI HTTP Server
- 🔒 **Environment Variables** - Secure configuration management

---

## 🏗️ Getting Started

### Prerequisites
- Python 3.8 or higher
- Git for version control
- Supabase account for database services
- Email service provider for notifications

### Installation Process

1. **📥 Clone the Repository**
   ```bash
   git clone https://github.com/vargheesk/MealzMapz.git
   cd MealzMapz
   ```

2. **📦 Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **⚙️ Configure Environment Variables**
   
   Create a `.env` file in the root directory:
   ```env
   SECRET_KEY=your-secret-key-here
   SUPABASE_URL=your-supabase-url
   SUPABASE_KEY=your-supabase-key
   MAIL_SERVER=your-mail-server
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=your-mail-username
   MAIL_PASSWORD=your-mail-password
   MAIL_DEFAULT_SENDER=your-default-sender-email
   ```

4. **🚀 Launch the Application**
   ```bash
   python app.py
   ```
   
   For production deployment:
   ```bash
   gunicorn app:app
   ```

---

## 📊 Database Schema

The application utilizes three primary database tables:

- **👥 Users Table** - Stores user profiles, authentication data, and organization information
- **📋 Listings Table** - Contains food posts and community places with location data
- **🔔 Subscriptions Table** - Manages follower relationships and notification preferences

---

## 🤝 Contributing

We welcome contributions from the community to help improve MealzMapz and expand its impact on reducing food waste.

### How to Contribute:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📞 Contact & Support

- **🌐 Website**: [https://mealmap-8aw4.onrender.com/](https://mealmap-8aw4.onrender.com/)
- **💻 Repository**: [https://github.com/vargheesk/MealzMapz](https://github.com/vargheesk/MealzMapz)
- **📧 Developer**: [Your Email Address]

---

## 🌟 Acknowledgments

- OpenStreetMap contributors for providing free mapping data
- Supabase team for the robust backend-as-a-service platform
- The open-source community for the tools and libraries that made this project possible

---

<div align="center">

**🍽️ Together, we can reduce food waste and feed communities! 🌍**

[![Star this repo](https://img.shields.io/github/stars/vargheesk/MealzMapz?style=social)](https://github.com/vargheesk/MealzMapz/stargazers)
[![Fork this repo](https://img.shields.io/github/forks/vargheesk/MealzMapz?style=social)](https://github.com/vargheesk/MealzMapz/network/members)

</div>