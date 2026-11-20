# TikTok Shop Analytics Dashboard

A comprehensive analytics tool for TikTok e-commerce operations, featuring SKU-level analysis, customer segmentation, LTV/CAC analysis, and marketing insights for the US market.

## 中文简介

TikTok Shop 数据分析看板:面向美国市场的跨境电商运营分析工具。支持 Excel/CSV 导入,围绕 SKU 动销、客户 RFM 分层、LTV/CAC、直播表现和营销渠道做分析,并一键生成带图表的 Excel 报告。前端 React + TypeScript + ECharts,后端 FastAPI + Pandas/scikit-learn,PostgreSQL/Redis 由 Docker Compose 编排。

> 仓库不含真实店铺数据和 `.env` 配置。运行前复制 `.env.example`,再导入自己的数据。

## Features

- **Multi-Source Data Import**: Excel/CSV files, TikTok API, Database
- **SKU-Level Analysis**: Pattern-based product analysis, inventory management
- **Customer Analysis**: RFM segmentation, behavioral clustering, LTV/CAC tracking
- **Marketing Insights**: Channel value assessment, US market-specific recommendations
- **Live Stream Analytics**: Traffic, conversion, and product performance
- **Advanced Analytics**: Correlation analysis, clustering, trend prediction
- **Excel Report Generation**: Automated report creation with charts and insights
- **Interactive Dashboard**: Real-time data visualization with ECharts

## Tech Stack

### Frontend
- React 18 + TypeScript
- Vite
- Ant Design 5.x
- Apache ECharts 5.x
- Zustand + React Query

### Backend
- FastAPI (Python 3.11+)
- Pandas + NumPy
- Scikit-learn + Statsmodels
- OpenPyXL + XlsxWriter
- Celery + Redis

### Database
- PostgreSQL 15+
- Redis 7+

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### Using Docker Compose (Recommended)

1. Clone the repository
```bash
git clone <repository-url>
cd tiktok-analytics
```

2. Configure environment variables
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Start all services
```bash
docker-compose up -d
```

4. Access the application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Local Development

#### Backend Development
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements/dev.txt

# Set up database
alembic upgrade head

# Run development server
uvicorn app.main:app --reload
```

#### Frontend Development
```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

## Project Structure

```
tiktok-analytics/
├── frontend/           # React frontend application
├── backend/            # FastAPI backend application
├── data/              # Data directory (imports/exports)
├── docs/              # Documentation
├── docker-compose.yml  # Docker orchestration
└── README.md
```

## API Documentation

Once the backend is running, visit http://localhost:8000/docs for interactive API documentation.

## Database Schema

The application uses PostgreSQL with the following main tables:
- `orders` - Order data
- `order_items` - Order items with SKU information
- `products` - Product information
- `product_skus` - SKU-level data with pattern information
- `customers` - Customer data
- `customer_ltv_cac` - LTV/CAC metrics
- `customer_segments` - Customer segmentation results
- `live_sessions` - Live stream sessions
- `traffic` - Traffic data
- `campaigns` - Marketing campaigns

## US Market Features

The tool includes specialized features for the US market:
- Regional preferences (West Coast, East Coast, Midwest, South)
- Generational preferences (Gen Z, Millennials, Gen X, Boomers)
- Cultural theme support (Halloween, Thanksgiving, Christmas, Independence Day)
- Pop culture integration
- DEI (Diversity, Equity, Inclusion) considerations
- Time zone analysis (EST/PST)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Your License Here]

## Contact

[Your Contact Information]
