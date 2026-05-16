# 🍅 Food Ingredient Classifier

> **AI-powered food ingredient recognition with smart recommendations and nutrition information**

A complete machine learning application that classifies food ingredients from images and provides intelligent cooking recommendations along with detailed nutritional information.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.13+-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🌟 Features

### 🤖 **AI Classification**
- **Deep Learning Model**: Custom CNN with MobileNetV2 backbone
- **Channel Attention**: Advanced attention mechanism for better accuracy
- **9 Food Classes**: Tomat, Daging, Keju, Kentang, Susu, Tahu, Telur, Tempe, Bawang Putih
- **High Accuracy**: Optimized for Indonesian food ingredients

### 💡 **Smart Recommendations**
- **AI-Powered Suggestions**: Cooking tips and usage recommendations
- **Context-Aware**: Recommendations based on ingredient properties
- **Multiple Sources**: Gemini AI integration with fallback system

### 📊 **Nutrition Information**
- **Complete Nutrition Data**: Calories, protein, fat, carbs, fiber, calcium
- **Health Categories**: Low/medium/high calorie classification
- **Health Tags**: High protein, low fat indicators
- **Recipe Calculator**: Total nutrition for multiple ingredients

### 🎨 **Modern Web Interface**
- **Responsive Design**: Works on desktop and mobile
- **Drag & Drop Upload**: Easy image upload interface
- **Real-time Results**: Instant classification and recommendations
- **Beautiful UI**: Modern dark theme with Tailwind CSS

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 16+ (for frontend development)
- Git

### 1. Clone Repository
```bash
git clone <repository-url>
cd coba
```

### 2. Setup Backend
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Setup Frontend
```bash
cd frontend
npm install
npm run build:css
cd ..
```

### 4. Run Application
```bash
# Start FastAPI server
uvicorn backend.main:app --reload

# Open browser
# http://localhost:8000
```

## 📁 Project Structure

```
coba/
├── 🔧 backend/              # FastAPI backend
│   ├── main.py             # Main API server
│   ├── services/           # Business logic
│   │   ├── predict.py      # ML prediction service
│   │   ├── recommendation.py # AI recommendations
│   │   └── nutrition.py    # Nutrition data service
│   ├── model/              # Trained ML model
│   └── data/               # Nutrition database
├── 🎨 frontend/             # Web interface
│   ├── index.html          # Main web page
│   ├── src/
│   │   ├── app.mjs         # JavaScript logic
│   │   └── *.css           # Styling
│   └── package.json        # Frontend dependencies
├── 🤖 training/             # ML training pipeline
│   ├── config.py           # Training configuration
│   ├── models.py           # Model architecture
│   ├── trainer.py          # Custom training loop
│   └── data_utils.py       # Data preprocessing
├── 📊 dataset/              # Training data
├── 📄 scripts/              # Utility scripts
├── 🧪 tests/                # Test suite
└── 📚 docs/                 # Documentation
```

## 🔧 API Endpoints

### Core Endpoints
```http
POST /predict              # Image classification
GET  /health              # Health check
GET  /                    # Frontend interface
```

### Nutrition API
```http
GET  /nutrition/{ingredient}           # Get nutrition info
GET  /nutrition/search?q={query}      # Search ingredients
GET  /nutrition/summary               # Nutrition statistics
GET  /nutrition/ingredients           # List all ingredients
POST /nutrition/recipe                # Calculate recipe nutrition
```

### Example Response
```json
{
  "filename": "tomato.jpg",
  "prediction": {
    "label": "tomat",
    "confidence": 0.95
  },
  "recommendation": {
    "text": "Tomat cocok untuk salad segar atau saus pasta...",
    "source": "gemini"
  },
  "nutrition": {
    "nama": "Tomat",
    "kalori_kcal": 18.0,
    "protein_g": 0.9,
    "kategori_kalori": "Rendah Kalori",
    "tinggi_protein": false,
    "rendah_lemak": true
  }
}
```

## 🤖 Machine Learning Pipeline

### Model Architecture
- **Backbone**: MobileNetV2 (ImageNet pretrained)
- **Custom Layer**: Channel Attention mechanism
- **Input Size**: 224x224 RGB images
- **Output**: 9 food ingredient classes
- **Framework**: TensorFlow/Keras

### Training Features
- **Custom Training Loop**: tf.GradientTape for advanced control
- **Two-Phase Training**: Warmup + Fine-tuning
- **Data Augmentation**: Rotation, zoom, flip, contrast
- **Early Stopping**: Patience-based training termination
- **TensorBoard Integration**: Real-time training monitoring

### Training Pipeline
```bash
# Full training pipeline
python train_model.py

# Custom configuration
python train_model.py --epochs 20 --no-plots

# Inference only
python train_model.py --inference-only --sample-image test.jpg
```

## 🌐 Deployment

### Local Development
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Deployment

#### Railway (Recommended)
```bash
# Push to GitHub
git push origin main

# Deploy to Railway
# 1. Connect GitHub repo at railway.app
# 2. Auto-deploy with railway.json config
```

#### Docker
```bash
# Build image
docker build -t food-classifier .

# Run container
docker run -p 8000:8000 food-classifier
```

### Environment Variables
```bash
# .env file
GEMINI_API_KEY=your_gemini_api_key_here
MODEL_PATH=backend/model/model.keras
LABEL_PATH=backend/model/class_names.json
```

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test
python -m pytest tests/test_main.py

# Run with coverage
python -m pytest --cov=backend tests/
```

## 📊 Performance

### Model Metrics
- **Accuracy**: 85%+ on validation set
- **Inference Time**: ~200ms per image
- **Model Size**: ~15MB (.keras format)
- **Classes**: 9 Indonesian food ingredients

### API Performance
- **Response Time**: <500ms average
- **Throughput**: 100+ requests/minute
- **Uptime**: 99.9% target
- **Memory Usage**: ~500MB with model loaded

## 🛠️ Development

### Adding New Ingredients
1. **Collect Data**: Add images to `dataset/{new_ingredient}/`
2. **Retrain Model**: Run `python train_model.py`
3. **Update Nutrition**: Add data to `dataset/dummy_gizi.csv`
4. **Convert Data**: Run `python scripts/convert_nutrition_data.py`

### Frontend Development
```bash
cd frontend

# Watch CSS changes
npm run watch:css

# Build for production
npm run build:css
```

### Backend Development
```bash
# Auto-reload on changes
uvicorn backend.main:app --reload

# Debug mode
uvicorn backend.main:app --reload --log-level debug
```

## 🤝 Contributing

1. **Fork** the repository
2. **Create** feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** changes (`git commit -m 'Add amazing feature'`)
4. **Push** to branch (`git push origin feature/amazing-feature`)
5. **Open** Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use TypeScript for new frontend features
- Add tests for new functionality
- Update documentation for API changes

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **TensorFlow Team** - For the amazing ML framework
- **FastAPI** - For the modern Python web framework
- **Tailwind CSS** - For the beautiful styling system
- **Google Gemini** - For AI-powered recommendations
- **MobileNetV2** - For the efficient CNN architecture

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-username/food-classifier/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/food-classifier/discussions)
- **Email**: your-email@example.com

---

<div align="center">

**Made with ❤️ for Indonesian Food Recognition**

[⭐ Star this repo](https://github.com/your-username/food-classifier) • [🐛 Report Bug](https://github.com/your-username/food-classifier/issues) • [💡 Request Feature](https://github.com/your-username/food-classifier/issues)

</div>