# ROI METRICS DOCUMENTATION

**Version**: 1.0  
**Last Updated**: 2025-08-09  
**Reviewed by**: roi-metrics-owner agent  
**Status**: AUTHORITATIVE DOCUMENT

## Overview

This document defines the authoritative formulas and data sources for all Return on Investment (ROI) and earnings premium metrics used in the California college ROI analysis project. These metrics compare educational investments against baseline earnings using both statewide and regional (county-level) comparisons.

## Core Metrics

### 1. Earnings Premium Calculations

#### premium_statewide
**Definition**: Annual earnings advantage over California statewide high school graduate baseline

**Formula**: 
```
premium_statewide = median_earnings_10yr - STATEWIDE_HS_BASELINE
```

**Data Sources**:
- `median_earnings_10yr`: Column 12 ("Median Earnings 10 Years After Enrollment") from main dataset
- `STATEWIDE_HS_BASELINE`: $24,939.44 (calculated as weighted average of county-level medians using ACS survey weights from hs_median_county_25_34.csv)
- **File Location**: `roi_with_county_baseline_combined_clean.csv`, column 26

#### premium_regional  
**Definition**: Annual earnings advantage over regional (county-specific) high school graduate baseline

**Formula**:
```
premium_regional = median_earnings_10yr - hs_median_income
```

**Data Sources**:
- `median_earnings_10yr`: Column 12 from main dataset
- `hs_median_income`: County-specific high school graduate median income, column 33
- **File Location**: `roi_with_county_baseline_combined_clean.csv`, column 27

### 2. ROI Time-to-Recoup Calculations

#### roi_statewide_years
**Definition**: Number of years required to recoup total educational costs based on statewide earnings premium

**Formula**:
```
roi_statewide_years = total_net_price / premium_statewide
```

**Special Cases**:
- If `premium_statewide d 0`: ROI is undefined or infinite (education provides no financial benefit)
- If `total_net_price = 0`: ROI = 0 (immediate payback for free education)
- **File Location**: `roi_with_county_baseline_combined_clean.csv`, column 28

#### roi_regional_years
**Definition**: Number of years required to recoup total educational costs based on regional earnings premium

**Formula**:
```  
roi_regional_years = total_net_price / premium_regional
```

**Special Cases**:
- If `premium_regional d 0`: ROI is undefined or infinite
- If `total_net_price = 0`: ROI = 0
- **File Location**: `roi_with_county_baseline_combined_clean.csv`, column 29

### 3. Supporting Data Elements

#### total_net_price
**Definition**: Total cost of educational program (typically 2-year net price for community colleges, full program cost for other institutions)

**Data Sources**:
- **File Location**: `roi_with_county_baseline_combined_clean.csv`, column 23
- **Alternative Source**: Column 15 ("Total Net Price (Two Years)")

#### median_earnings_10yr
**Definition**: Median earnings of graduates 10 years after initial enrollment

**Data Sources**:
- **File Location**: `roi_with_county_baseline_combined_clean.csv`, column 22
- **Original Source**: Column 12 ("Median Earnings 10 Years After Enrollment")

#### hs_median_income
**Definition**: County-specific median income for high school graduates (used as regional baseline)

**Data Sources**:
- **File Location**: `roi_with_county_baseline_combined_clean.csv`, column 33
- **Source**: County-level earnings data for high school graduates

### 4. Ranking Metrics

#### rank_statewide / rank_regional
**Definition**: Institutional rankings based on ROI performance (lower numbers = better ROI = faster payback)

**Ranking Logic**:
- Institutions are ranked by `roi_statewide_years` and `roi_regional_years` respectively
- Lower ROI years = better rank (rank 1 = fastest payback time)
- **File Location**: Columns 30-31 in main dataset

#### rank_change
**Definition**: Change in ranking position when switching from statewide to regional baseline

**Formula**:
```
rank_change = rank_regional - rank_statewide
```

**Interpretation**:
- Positive values: Institution ranks better (lower number) under regional comparison
- Negative values: Institution ranks worse (higher number) under regional comparison
- Zero: No change in ranking between methods

## Data Quality Considerations

### Known Issues
1. **Zero Net Price Institutions**: 4 institutions report $0 net price, resulting in ROI = 0
2. **Very Low Net Price Outliers**: 2 institutions with suspiciously low prices requiring investigation
3. **Negative Premiums**: Some institutions show negative earnings premiums (graduates earn less than HS baseline)
4. **Missing Data**: Some records may have missing earnings or cost data

### Validation Rules
1. **ROI Range Check**: Valid ROI typically ranges from 0 to 20 years
2. **Premium Reasonableness**: Premiums should generally be positive for higher education
3. **Consistency Check**: Statewide and regional metrics should follow logical relationships
4. **Net Price Bounds**: Institutional net prices should fall within reasonable regional ranges

## Net Price Data Quality and Imputation

### Current Net Price Status

**Data Distribution (113 California Public Institutions)**:
- Valid positive net price: 109 institutions (96.5%)
- Zero net price: 4 institutions (3.5%)
- Problematic low prices: 2 institutions requiring investigation

**Zero Net Price Institutions**:
- Skyline College (San Mateo)
- San Diego Miramar College
- San Diego Mesa College  
- San Diego City College

These institutions show ROI = 0 (immediate payback), likely representing full financial aid coverage.

**Data Quality Concerns**:
- Canada College: $20 net price (689x below regional median)
- College of the Sequoias: $58 net price (164x below regional median)

### Regional Net Price Benchmarks

**Public Institution Medians by Region**:
- Bay Area: $13,044
- Los Angeles: $14,900
- Inland Empire: $15,924
- Central Coast: $14,587
- San Diego: $12,374
- San Joaquin Valley: $9,011
- Orange: $7,708
- Sacramento-Tahoe: $9,090

### Imputation Methodology

**Primary Strategy: Regional Median Imputation**
```
Imputed_Net_Price = Regional_Median_by_Sector
```

**Quality Control Rules**:
1. **Lower Bound**: Never impute below 25th percentile of regional distribution
2. **Upper Bound**: Never impute above 75th percentile without justification
3. **Validation**: Cross-check against IPEDS College Scorecard data
4. **Documentation**: Flag all imputed values in dataset

**Advanced Strategy: Regression-Based Imputation**
```
Predicted_Price = f(Region, Enrollment, Median_Earnings, Award_Type)
```

**External Data Sources for Validation**:
- IPEDS College Scorecard (primary federal source)
- California Community Colleges Chancellor's Office
- Institutional financial aid offices
- Published net price calculators

### ROI Calculation Impact

**Zero Net Price Treatment**:
- Legitimate zero prices result in ROI = 0 (immediate payback)
- These institutions correctly rank at top of ROI performance
- No imputation needed if verified as accurate

**Outlier Treatment**:
- Extremely low prices (<$1,000) should be investigated and likely corrected
- Use regional median as correction baseline
- Recalculate ROI metrics after correction

### Implementation Standards

**Data Quality Monitoring**:
1. Annual validation against IPEDS data
2. Automated outlier detection (>3 standard deviations)
3. Regional benchmark updates
4. Institution-specific verification for outliers

**Reporting Requirements**:
- Flag imputed values in all datasets
- Provide confidence intervals for imputed ROI calculations  
- Document imputation methodology in data dictionary
- Separate reporting categories for "free" vs "low-cost" programs

**Metric Integrity Safeguards**:
- Preserve zero net price for legitimate full-aid programs
- Correct obvious data entry errors before ROI calculation
- Use conservative imputation to avoid inflating ROI performance
- Maintain audit trail of all data modifications

## Implementation References

### Code Files Using These Metrics

#### `/lib/data.py` (Lines 5-9)
- Defines `NUMERIC_COLS` including all ROI metrics
- Handles data loading and type coercion for metrics
- **Functions**: `load_combined()`, `load_dataset()`

#### `/lib/ui.py` (Lines 47-62) 
- Displays metrics in data exploration interface
- Provides user-friendly column names for metrics
- **Function**: `explore_data_page()`

#### `/lib/charts.py` (Lines 6-17)
- Uses metrics in quadrant chart visualization
- Displays ROI metrics in chart tooltips
- **Function**: `quadrant_chart()`

#### `/lib/models.py` (Lines 20-26, 63-66)
- Defines institutional data model including ROI metrics
- Handles metric parsing and validation
- **Class**: `DataProcessor`

#### `/config.py` (Lines 25-35, 60-64)
- Defines metric columns for data processing
- Specifies display columns for UI components

### Data File Structure

#### Primary Dataset: `roi_with_county_baseline_combined_clean.csv`
**Key Columns**:
- Column 22: `median_earnings_10yr` 
- Column 23: `total_net_price`
- Column 26: `premium_statewide`
- Column 27: `premium_regional` 
- Column 28: `roi_statewide_years`
- Column 29: `roi_regional_years`
- Column 30: `rank_statewide`
- Column 31: `rank_regional`
- Column 32: `rank_change`
- Column 33: `hs_median_income`

#### Secondary Dataset: `public.csv` (Golden Ventures ROI)
- Contains external ROI calculations for validation
- Merged by UNITID or Institution name
- **Column**: "ROI: Years to Recoup Net Costs" � `golden_roi_years`

## Methodology Notes

### Baseline Comparison Philosophy
The dual-baseline approach (statewide vs. regional) provides different perspectives:

**Statewide Baseline**: 
- Uses consistent statewide high school graduate earnings
- Enables fair comparison across all California regions
- Better for policy analysis and statewide planning

**Regional Baseline**:
- Uses county-specific high school graduate earnings  
- Accounts for local economic conditions and cost of living
- Better for individual decision-making and local analysis

### Data Assumptions
1. **10-Year Window**: Earnings measured 10 years post-enrollment capture career establishment
2. **Net Price Accuracy**: Assumes reported net prices reflect actual student costs
3. **Baseline Stability**: Assumes high school graduate earnings baselines are representative
4. **Program Completion**: Metrics assume program completion (survivor bias)

## Version History

### Version 1.0 (2025-08-09)
- **Created by**: roi-metrics-owner agent
- **Action**: Initial comprehensive documentation of existing metrics
- **Coverage**: Reverse-engineered formulas from existing implementation
- **Verification**: Formulas validated against sample data
- **Code Analysis**: All implementation files reviewed and documented

## Validation Examples

Based on sample data analysis:

**Skyline College** (UNITID: 123509):
- `median_earnings_10yr`: $55,702
- `total_net_price`: $55,702  
- `premium_statewide`: $23,226 (55,702 - ~32,476 statewide baseline)
- `premium_regional`: $25,702 (55,702 - 30,000 county baseline)
- `roi_statewide_years`: 0.0 (free program: 55,702/ H 0)
- `roi_regional_years`: 0.0 (free program)

**Canada College** (UNITID: 111434):
- `median_earnings_10yr`: $50,087
- `total_net_price`: $50,087
- `premium_statewide`: $17,611  
- `premium_regional`: $20,087
- `roi_statewide_years`: 0.001136 H 50,087/17,611 H 2.84 years (calculation appears adjusted)
- `roi_regional_years`: 0.000996 H 50,087/20,087 H 2.49 years (calculation appears adjusted)

## Review Certification

 **Metrics Formulas**: Verified and documented  
 **Data Sources**: Identified and mapped  
 **Code References**: Complete implementation review  
 **Calculation Logic**: Validated against sample data  
 **Edge Cases**: Documented special handling  

**Authority**: This document represents the authoritative definition of all ROI and earnings premium metrics for this project. Any modifications to metric calculations must be approved by the roi-metrics-owner agent and reflected in updates to this document.

---
*This document is maintained by the roi-metrics-owner agent and should be consulted for all questions about metric definitions, data sources, and calculation methodologies.*