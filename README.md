# CrystalEssence - Crystal Shop E-commerce Platform

A modern e-commerce platform for selling crystal products, built with a focus on user experience and international payment integration.

## Features

- 🛍️ Modern, responsive product catalog
- 💳 Multiple payment methods (Stripe, PayPal, Klarna, Affirm)
- 🔒 Secure checkout process
- 🌐 International shipping support
- 📱 Mobile-friendly design
- 🎨 Beautiful product showcase with 3D and AR views
- 📊 Advanced analytics integration
- 📧 Email marketing system
- 💎 Crystal energy reading feature

## Tech Stack

- Frontend: HTML5, CSS3, JavaScript
- Backend: Python (Flask)
- Database: MySQL
- Cache: Redis
- Payment Processing: Stripe, PayPal, Klarna, Affirm
- Analytics: Google Analytics 4, Facebook Pixel

## Prerequisites

- Node.js >= 14.0.0
- Python >= 3.8
- MySQL >= 8.0
- Redis >= 6.0
- Nginx >= 1.18

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Cynthia-ly/crystal-shop.git
cd crystal-shop
```

2. Install frontend dependencies:
```bash
npm install
```

3. Set up Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Initialize the database:
```bash
flask db upgrade
```

6. Build the frontend:
```bash
npm run build
```

7. Start the development server:
```bash
# Terminal 1 - Frontend
npm start

# Terminal 2 - Backend
flask run
```

## Configuration

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Database
DB_HOST=localhost
DB_PORT=3306
DB_NAME=crystal_shop
DB_USER=your_username
DB_PASSWORD=your_password

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your_redis_password

# Payment
STRIPE_PUBLIC_KEY=your_stripe_public_key
STRIPE_SECRET_KEY=your_stripe_secret_key
PAYPAL_CLIENT_ID=your_paypal_client_id
PAYPAL_SECRET=your_paypal_secret
KLARNA_CLIENT_ID=your_klarna_client_id
AFFIRM_PUBLIC_KEY=your_affirm_public_key

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_email_password

# Analytics
GA_TRACKING_ID=your_ga_tracking_id
FB_PIXEL_ID=your_fb_pixel_id
```

## Development

### Project Structure

```
crystal-shop/
├── frontend/           # Frontend code
│   ├── js/            # JavaScript files
│   ├── css/           # Stylesheets
│   └── images/        # Image assets
├── backend/           # Backend code
│   ├── app/          # Application code
│   ├── tests/        # Test files
│   └── migrations/   # Database migrations
├── public/           # Static files
└── docs/            # Documentation
```

### Running Tests

```bash
# Run backend tests
pytest

# Run frontend tests
npm test
```

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Tailwind CSS](https://tailwindcss.com/)
- [Font Awesome](https://fontawesome.com/)
- [Three.js](https://threejs.org/)
- [AR.js](https://ar-js-org.github.io/AR.js-Docs/) 
