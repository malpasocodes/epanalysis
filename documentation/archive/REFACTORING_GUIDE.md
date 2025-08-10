# Refactoring Recommendations

## Summary of Improvements

I've created several new modules to improve your codebase's architecture, maintainability, and robustness:

### 1. **Type Safety & Data Models** (`lib/models.py`)
- Added `DataConfig` dataclass for centralized configuration
- Created `Institution` model with proper type hints
- Provides structured data access instead of raw DataFrames

### 2. **Enhanced Data Loading** (`lib/data_improved.py`)
- `DataLoader` class with proper error handling
- Validation of data quality with logging
- Robust merge strategies with fallbacks
- Automatic cleanup of merge artifacts (_x/_y columns)

### 3. **Reusable UI Components** (`lib/components.py`)
- `FilterSidebar`: Standardized filter interface
- `MetricsRow`: Consistent metric display
- `RankingsTable`: Enhanced table with search, sort, and summaries
- Separation of presentation logic from data logic

### 4. **Configuration Management** (`config.py`)
- Centralized settings and paths
- Environment variable support
- Path validation utilities
- Consistent formatting definitions

### 5. **Utility Functions** (`lib/utils.py`)
- `DataCleaner`: Column normalization, type coercion, imputation
- `Formatters`: Consistent display formatting
- `Validators`: Data quality checks

## Migration Path

To integrate these improvements:

### Step 1: Update Dependencies
```bash
uv add typing-extensions pydantic
```

### Step 2: Gradually Replace Components
Start with low-risk changes:
1. Replace hardcoded paths with `config.py`
2. Use `DataLoader` instead of current `load_dataset()`
3. Replace UI rendering with modular components

### Step 3: Update Main App
```python
# app.py (refactored version)
import streamlit as st
from config import Config
from lib.data_improved import DataLoader
from lib.components import FilterSidebar, RankingsTable

st.set_page_config(
    page_title=Config.APP_TITLE,
    layout=Config.PAGE_LAYOUT
)

# Load data with new loader
loader = DataLoader()
df = loader.load_all()

# Use components
if page == "Rankings":
    table = RankingsTable(df)
    table.render()
```

## Key Benefits

1. **Better Error Handling**: Graceful failures with informative messages
2. **Type Safety**: Catch errors at development time
3. **Modularity**: Easier to test and maintain individual components
4. **Consistency**: Standardized formatting and UI patterns
5. **Extensibility**: Easy to add new features without breaking existing code

## Additional Recommendations

### Testing
Add unit tests for critical functions:
```python
# tests/test_data.py
def test_roi_parsing():
    loader = DataLoader()
    assert loader._parse_roi_values(pd.Series(["(1.5)"]))[0] == -1.5
```

### Logging
Configure logging for better debugging:
```python
# At app startup
import logging
logging.basicConfig(level=logging.INFO)
```

### Data Validation
Consider using Pydantic for stricter validation:
```python
from pydantic import BaseModel, validator

class InstitutionData(BaseModel):
    unitid: Optional[str]
    name: str
    net_price: float
    
    @validator('net_price')
    def price_must_be_positive(cls, v):
        if v < 0:
            raise ValueError('Net price cannot be negative')
        return v
```

### Performance
- Keep `@st.cache_data` decorators
- Consider adding database backend for larger datasets
- Implement lazy loading for charts

### Documentation
- Add docstrings to all public methods
- Create API documentation with Sphinx
- Add inline comments for complex logic

## Next Steps

1. Review and test the new modules
2. Gradually migrate existing code
3. Add comprehensive error handling
4. Implement logging throughout
5. Add unit tests for critical paths
6. Consider CI/CD pipeline setup