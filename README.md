# 🏠 Smart House Management System

<div align="center">

![House Management](https://img.shields.io/badge/House-Management-blue?style=for-the-badge&logo=home-assistant)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

**A comprehensive web application to manage your household efficiently**

[🚀 Live Demo](#) • [📖 Documentation](#installation) • [🐛 Report Bug](https://github.com/Nisarg1810/House_management_system/issues) • [✨ Request Feature](https://github.com/Nisarg1810/House_management_system/issues)

</div>

---

## 🌟 Features

### 📊 **Dashboard Overview**
- **Real-time Statistics** - Get instant insights into your household management
- **Quick Actions** - Add items, expenses, and events with one click
- **Visual Analytics** - Beautiful charts and graphs for better understanding

### 📦 **Inventory Management**
- ✅ **Stock Tracking** - Keep track of all household items
- 🏷️ **Category Organization** - Organize items by categories (Food, Electronics, etc.)
- 📅 **Expiry Alerts** - Never let food expire again
- 🔍 **Smart Search & Filter** - Find items quickly with advanced filtering
- 📱 **Low Stock Notifications** - Get alerts when items are running low

### 💰 **Expense Tracking**
- 💳 **Multi-Category Expenses** - Track spending across different categories
- 📈 **Monthly Reports** - Analyze your spending patterns
- 🎯 **Budget Management** - Set and monitor monthly budgets
- 📊 **Visual Spending Analysis** - Charts and graphs for expense visualization

### 📅 **Event & Calendar Management**
- 🗓️ **Personal Calendar** - Manage your household events and reminders
- ⏰ **Smart Reminders** - Never miss important dates
- 📝 **Event Details** - Add descriptions and notes to events

### 🛒 **Smart Shopping List**
- 📋 **Auto-Generated Lists** - Automatically create shopping lists from low stock items
- ✅ **Organized by Category** - Shop efficiently with categorized lists
- 🎯 **Priority Items** - Highlight urgent purchases

## 🖼️ Screenshots

<div align="center">

### 🏡 Dashboard
![Screenshot 2025-06-23 154040](https://github.com/user-attachments/assets/157a274f-7b4b-4e59-80b3-eb9d7d204c15)

### 📦 Inventory Management
![image](https://github.com/user-attachments/assets/d295f762-1b7c-4467-85f8-015c73fdc725)

### 💰 Expense Tracking
![image](https://github.com/user-attachments/assets/8de3140c-ac88-4215-a3d6-92bfe4ee7290)


</div>

## 🚀 Quick Start

### Prerequisites

Make sure you have the following installed:
- 🐍 **Python 3.8+**
- 🌐 **pip** (Python package installer)
- 💾 **Git**

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Nisarg1810/House_management_system.git
   cd House_management_system
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv house_management_env
   
   # On Windows
   house_management_env\Scripts\activate
   
   # On macOS/Linux
   source house_management_env/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   
   Open your browser and go to: `http://127.0.0.1:8000/`

## 🛠️ Technology Stack

<div align="center">

| Category | Technologies |
|----------|-------------|
| **Backend** | ![Django](https://img.shields.io/badge/Django-092E20?style=flat&logo=django&logoColor=white) ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) |
| **Frontend** | ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white) ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white) ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black) |
| **Database** | ![SQLite](https://img.shields.io/badge/SQLite-07405E?style=flat&logo=sqlite&logoColor=white) |
| **Styling** | ![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=flat&logo=bootstrap&logoColor=white) ![Font Awesome](https://img.shields.io/badge/Font_Awesome-339AF0?style=flat&logo=fontawesome&logoColor=white) |

</div>

## 📁 Project Structure

```
House_management_system/
├── 📁 house_management/          # Main project directory
│   ├── 📄 settings.py           # Django settings
│   ├── 📄 urls.py               # Main URL configuration
│   └── 📄 wsgi.py               # WSGI configuration
├── 📁 manager_app/              # Main application
│   ├── 📁 migrations/           # Database migrations
│   ├── 📁 static/               # Static files (CSS, JS, Images)
│   ├── 📁 templates/            # HTML templates
│   ├── 📄 models.py             # Database models
│   ├── 📄 views.py              # View functions
│   ├── 📄 urls.py               # App URL configuration
│   └── 📄 admin.py              # Admin configuration
├── 📄 manage.py                 # Django management script
├── 📄 requirements.txt          # Python dependencies
└── 📄 README.md                 # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory and add the following:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration (Optional)
DB_NAME=house_management
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

### Database Setup

The application uses SQLite by default. To use PostgreSQL or MySQL:

1. Install the required database adapter:
   ```bash
   # For PostgreSQL
   pip install psycopg2-binary
   
   # For MySQL
   pip install mysqlclient
   ```

2. Update the `DATABASES` configuration in `settings.py`

## 🎯 Usage

### Adding Inventory Items

1. Navigate to the Dashboard
2. Click the "Add Stock" button in the Inventory card
3. Fill in the item details:
   - Item name
   - Quantity and unit
   - Category
   - Expiry date (optional)
   - Description

### Tracking Expenses

1. Click "Add Expense" in the Expense Tracker card
2. Enter expense details:
   - Title and amount
   - Category
   - Date
   - Description/notes

### Managing Events

1. Use the "Add Event" button in the Calendar card
2. Set event details:
   - Title and date
   - Time (optional)
   - Description

## 📊 API Documentation

The application provides several internal APIs for data management:

### Inventory API Endpoints
- `GET /api/inventory/` - List all inventory items
- `POST /api/inventory/` - Create new inventory item
- `PUT /api/inventory/<id>/` - Update inventory item
- `DELETE /api/inventory/<id>/` - Delete inventory item

### Expense API Endpoints
- `GET /api/expenses/` - List all expenses
- `POST /api/expenses/` - Create new expense
- `GET /api/expenses/monthly/` - Get monthly expense summary

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guidelines for Python code
- Write descriptive commit messages
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

## 🐛 Troubleshooting

### Common Issues

**Database Migration Errors**
```bash
python manage.py makemigrations --empty manager_app
python manage.py migrate
```

**Static Files Not Loading**
```bash
python manage.py collectstatic
```

**Permission Denied Errors**
- Ensure you have proper file permissions
- Check if the virtual environment is activated

### Getting Help

- 📖 Check the [Django Documentation](https://docs.djangoproject.com/)
- 🐛 [Create an Issue](https://github.com/Nisarg1810/House_management_system/issues)
- 💬 Join our community discussions

## 🚀 Deployment

### Heroku Deployment

1. Install Heroku CLI
2. Create a Heroku app:
   ```bash
   heroku create your-app-name
   ```
3. Set environment variables:
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set DEBUG=False
   ```
4. Deploy:
   ```bash
   git push heroku main
   ```

### Docker Deployment

```dockerfile
# Dockerfile included in the repository
docker build -t house-management .
docker run -p 8000:8000 house-management
```

## 📈 Roadmap

- [ ] 📱 **Mobile App** - React Native mobile application
- [ ] 🔔 **Push Notifications** - Real-time notifications for important events
- [ ] 📊 **Advanced Analytics** - More detailed reporting and insights
- [ ] 🌐 **Multi-language Support** - Internationalization
- [ ] 🔗 **API Integration** - Integration with grocery stores and services
- [ ] 👥 **Multi-user Support** - Family member management
- [ ] 🤖 **AI Recommendations** - Smart suggestions based on usage patterns

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Django Community** for the amazing framework
- **Bootstrap** for responsive design components
- **Font Awesome** for beautiful icons
- **Contributors** who have helped improve this project

## 👨‍💻 Author

**Nisarg Patel**
- GitHub: [@Nisarg1810](https://github.com/Nisarg1810)
- Email: [mail](pateln1810@gmail.com)

---

<div align="center">

**⭐ If you found this project helpful, please give it a star! ⭐**

Made with ❤️ by [Nisarg Patel](https://github.com/Nisarg1810)

</div>
