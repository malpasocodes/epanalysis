# DATASETS.md

## Dataset Inventory

### Source Datasets
1. **gr-private.csv** - Private institutional data from Golden Record system
2. **gr-public.csv** - Public institutional data from Golden Record system

### Consolidated Datasets  
1. **gr-institutions.csv** - Consolidated institutional dataset with 13 standardized fields
2. **roi-metrics.csv** - ROI metrics calculated for all 327 institutions

### Analytics Datasets
1. **hs_median_county_25_34.csv** - High school graduate median earnings by county baseline

## Field Definitions

### gr-institutions.csv (Consolidated Dataset)
This dataset contains 327 California higher education institutions (206 private, 121 public) with the following standardized fields:

#### Raw Fields (directly from source systems)
1. **OPEID6** (Integer)
   - Description: Office of Postsecondary Education Identifier (6-digit format)
   - Source: Federal Department of Education OPEID system
   - Usage: Primary institutional identifier for federal data matching
   - Data Quality: 262 unique values across 327 records (some institutions share OPEID6)

2. **Institution** (String)
   - Description: Official institution name
   - Source: Institutional registration records
   - Usage: Primary display name for institutions

3. **City** (String)
   - Description: Primary city location of institution
   - Source: Institutional address records

4. **County** (String)
   - Description: California county where institution is located
   - Source: Geographic lookup from institutional addresses

5. **Region** (String)
   - Description: California economic region classification
   - Source: Regional economic development boundaries
   - Values: Bay Area, Los Angeles, Central Coast, San Joaquin Valley, Inland Empire, etc.

6. **Predominant Award** (String)
   - Description: Most commonly awarded credential type
   - Source: IPEDS completion data analysis
   - Values: Certificate, Associate's, Bachelor's, Master's, Doctoral

7. **Sector** (String)
   - Description: Institution control and level classification
   - Source: IPEDS institutional characteristics
   - Values: Public, Private for-profit, Private nonprofit

8. **Undergraduate Degree-seeking students** (Integer)
   - Description: Fall enrollment count of degree/certificate-seeking undergraduates
   - Source: IPEDS Fall Enrollment survey
   - Data Quality: Numeric values cleaned of comma formatting

9. **ZIP** (String)
   - Description: Postal ZIP code for institution's primary address
   - Source: Institutional address records
   - Format: 5-digit ZIP or ZIP+4 format

10. **Latitude** (Float)
    - Description: Geographic latitude coordinate
    - Source: Geocoded from institutional addresses
    - Precision: 6 decimal places
    - Data Quality: 1 missing value

11. **Longitude** (Float)
    - Description: Geographic longitude coordinate  
    - Source: Geocoded from institutional addresses
    - Precision: 6 decimal places
    - Data Quality: 1 missing value

#### Derived Fields (calculated/transformed)
12. **Median Earnings 10 Years After Enrollment** (Integer)
    - Description: Median earnings of students 10 years after initial enrollment
    - Source: Federal Student Aid data matched to tax records
    - Transformation: Currency formatting removed, converted to integer
    - Units: US dollars (annual)
    - Coverage: Students who received federal financial aid

13. **Annual Net Price** (Integer) - **NEW FIELD ADDED**
    - Description: Average annual net price after financial aid for title IV students
    - Source: IPEDS Net Price data
    - Transformation: Currency formatting and parentheses removed, negative values preserved  
    - Units: US dollars (annual)
    - Range: $10 - $56,381
    - Statistics:
      - Mean: $17,589
      - Median: $17,550
      - 25th percentile: $7,613
      - 75th percentile: $25,676

## Data Lineage

### Source Systems
- **Golden Record System**: Comprehensive institutional database maintained for California higher education analysis
- **IPEDS (Integrated Postsecondary Education Data System)**: Federal institutional data collection
- **Federal Student Aid**: Student-level earnings data from tax record matching
- **Department of Education OPEID**: Official institutional identifier system
- **American Community Survey (ACS)**: County-level high school graduate earnings data

### Collection Methodology
1. **Source Data**: Downloaded from Golden Record system containing California higher education institutions
2. **Date Range**: Data represents most recent complete academic year
3. **Population**: All degree-granting institutions in California reporting to IPEDS

### Transformation History
1. **Data Loading** (2025-08-10):
   - Loaded gr-private.csv (206 institutions)
   - Loaded gr-public.csv (121 institutions)
   - Combined total: 327 institutions

2. **Data Cleaning**:
   - Removed BOM (Byte Order Mark) characters from all text fields
   - Cleaned monetary fields by removing currency symbols, commas, parentheses
   - Converted negative values in parentheses format to proper negative numbers
   - Coerced numeric fields with error handling for invalid values
   - Removed comma formatting from enrollment counts

3. **Field Selection**:
   - Selected 13 standardized fields from larger source datasets
   - Ensured consistent field naming across private and public datasets

4. **Data Concatenation**:
   - Combined private and public datasets maintaining field consistency
   - Sorted by OPEID6 for consistent ordering

## Data Quality Notes

### Known Issues
1. **OPEID6 Duplicates**: 262 unique OPEID6 values across 327 records
   - Cause: Some institutions share federal identifiers (branch campuses)
   - Impact: Cannot use OPEID6 as unique key without additional qualifiers

2. **Missing Coordinates**: 1 institution missing longitude value
   - Impact: Affects geographic analysis and mapping capabilities
   - Recommendation: Geocode missing address manually

3. **Annual Net Price Range**: Wide range from $10 to $56,381
   - Very low values may indicate data quality issues or special programs
   - Recommendation: Investigate institutions with net price < $500

### Data Validation Results
- **Completeness**: 99.7% complete (only 1 missing longitude value)
- **Consistency**: All required fields present in both source datasets
- **Format Standardization**: All monetary and numeric fields properly formatted
- **Geographic Coverage**: All major California regions represented

### Limitations
1. **Federal Aid Recipients Only**: Earnings data limited to students who received federal financial aid
2. **Timing**: Net price and earnings data may be from different academic years
3. **Sample Size**: Earnings calculations may be based on small cohorts for some institutions
4. **Private Institution Coverage**: May not include all small private institutions

### ROI Metrics Data Quality

#### Known Issues
1. **Negative Earnings Premiums**: 44 institutions show negative premiums (earnings below HS baseline)
   - Cause: Short-term programs or data quality issues in earnings reporting
   - Impact: ROI calculations marked as invalid (999 years)
   - Sectors Affected: Primarily private for-profit certificate programs

2. **Missing County Baselines**: 12 institutions have counties without baseline earnings data
   - Affected Counties: Include smaller/rural counties not in ACS sample
   - Resolution: Uses statewide baseline ($24,939.44) as fallback
   - Impact: May underestimate regional premium for rural institutions

3. **Very Low Net Prices**: Some institutions have net prices under $100
   - May indicate data errors, special programs, or calculation methodology issues
   - Produces very favorable ROI calculations that may not reflect reality

#### Data Validation Results
- **Coverage**: 327 institutions (100% of target population)
- **Valid Statewide ROI**: 283 institutions (86.5%)
- **Valid Regional ROI**: 286 institutions (87.5%) 
- **Complete Premium Calculations**: 327 institutions (100%)
- **County Baseline Coverage**: 315 institutions (96.3%)

#### Statistics Summary
- **Statewide ROI Years**: Mean 3.36, Median 1.04 (valid values only)
- **Regional ROI Years**: Mean 4.31, Median 1.02 (valid values only)
- **Premium Range**: $-1,363 to $47,051 (statewide), $-2,381 to $47,051 (regional)
- **Net Price Range**: $10 to $56,381

#### Methodology Validation
- Consistent calculation methodology across all 327 institutions
- Same baseline values and formulas used for public and private sectors  
- Rankings use standardized minimum-rank method for tie handling
- Invalid ROI values properly identified and excluded from rankings

## Change Log

### 2025-08-10: Initial Consolidation
- **Action**: Created consolidated gr-institutions.csv dataset
- **Source Files**: 
  - gr-private.csv (206 institutions)
  - gr-public.csv (121 institutions)
- **Fields Added**: 13 standardized fields including new Annual Net Price field
- **Transformations Applied**:
  - BOM character removal
  - Monetary field cleaning
  - Numeric field standardization
  - Data concatenation and sorting
- **Output**: gr-institutions.csv (327 institutions)
- **Quality Checks**: Field availability verified, data types standardized
- **Documentation Created**: Complete field definitions and lineage documentation

### Field Evolution
- **Annual Net Price**: Added as 13th field in consolidation process
  - Previously considered but not included in initial 12-field plan
  - Successfully found in both source datasets
  - Provides critical cost information for institutional comparison
  - Complements earnings data for ROI calculations

### roi-metrics.csv (ROI Analytics Dataset)
This dataset contains calculated ROI metrics for all 327 California higher education institutions (206 private, 121 public) using consistent methodology across all sectors.

#### Raw Fields (from source data)
1. **OPEID6** (Integer)
   - Description: Office of Postsecondary Education Identifier
   - Source: gr-institutions.csv
   - Usage: Primary institutional identifier

2. **Institution** (String)
   - Description: Official institution name
   - Source: gr-institutions.csv
   - Usage: Institution display name

3. **County** (String)
   - Description: California county where institution is located
   - Source: gr-institutions.csv
   - Usage: Regional baseline mapping

4. **Sector** (String)
   - Description: Institution control and level classification
   - Source: gr-institutions.csv
   - Values: Public, Private for-profit, Private non-profit

5. **median_earnings_10yr** (Integer)
   - Description: Median earnings of students 10 years after enrollment
   - Source: gr-institutions.csv (from Federal Student Aid data)
   - Units: US dollars (annual)
   - Coverage: Students who received federal financial aid

6. **total_net_price** (Integer)
   - Description: Average annual net price after financial aid
   - Source: gr-institutions.csv (from IPEDS Net Price data)
   - Units: US dollars (annual)

#### Derived Fields (calculated for ROI analysis)
7. **premium_statewide** (Float)
   - Description: Earnings premium above statewide high school baseline
   - Calculation: median_earnings_10yr - $24,939.44
   - Baseline Source: Weighted average statewide HS earnings
   - Units: US dollars (annual)

8. **premium_regional** (Float)
   - Description: Earnings premium above county-specific high school baseline
   - Calculation: median_earnings_10yr - hs_median_income (by county)
   - Baseline Source: hs_median_county_25_34.csv
   - Fallback: Uses statewide baseline for counties without data
   - Units: US dollars (annual)

9. **roi_statewide_years** (Float)
   - Description: Years to recoup educational costs using statewide baseline
   - Calculation: total_net_price / premium_statewide
   - Special Values: 0.0 for free/negative cost, 999 for no/negative premium
   - Units: Years

10. **roi_regional_years** (Float)
    - Description: Years to recoup educational costs using regional baseline
    - Calculation: total_net_price / premium_regional
    - Special Values: 0.0 for free/negative cost, 999 for no/negative premium
    - Units: Years

11. **rank_statewide** (Integer)
    - Description: ROI ranking using statewide baseline (lower = better)
    - Calculation: Rank of roi_statewide_years (ascending)
    - Method: Minimum ranking for ties
    - Coverage: Only institutions with valid ROI (< 999 years)

12. **rank_regional** (Integer)
    - Description: ROI ranking using regional baseline (lower = better)
    - Calculation: Rank of roi_regional_years (ascending)
    - Method: Minimum ranking for ties
    - Coverage: Only institutions with valid ROI (< 999 years)

13. **rank_change** (Float)
    - Description: Change in ranking from statewide to regional baseline
    - Calculation: rank_regional - rank_statewide
    - Interpretation: Negative = improved rank with regional baseline

14. **hs_median_income** (Float)
    - Description: County-specific high school graduate median earnings
    - Source: hs_median_county_25_34.csv
    - Coverage: 25-34 year old demographic
    - Missing: 12 institutions have counties without baseline data

## Change Log

### 2025-08-10: Initial Consolidation
- **Action**: Created consolidated gr-institutions.csv dataset
- **Source Files**: 
  - gr-private.csv (206 institutions)
  - gr-public.csv (121 institutions)
- **Fields Added**: 13 standardized fields including new Annual Net Price field
- **Transformations Applied**:
  - BOM character removal
  - Monetary field cleaning
  - Numeric field standardization
  - Data concatenation and sorting
- **Output**: gr-institutions.csv (327 institutions)
- **Quality Checks**: Field availability verified, data types standardized
- **Documentation Created**: Complete field definitions and lineage documentation

### 2025-08-10: ROI Metrics Dataset Creation
- **Action**: Created roi-metrics.csv with comprehensive ROI calculations for all institutions
- **Source Files**:
  - gr-institutions.csv (327 institutions with earnings and net price data)
  - hs_median_county_25_34.csv (34 county baselines)
- **Fields Added**: 14 fields (6 raw + 8 derived ROI metrics)
- **Methodology**:
  - Statewide baseline: $24,939.44 (weighted average HS earnings)
  - County-specific baselines mapped via FIPS codes
  - Consistent ROI calculation: net_price / earnings_premium
  - Rankings with minimum-rank method for ties
- **Coverage**: 100% institution coverage, 96.3% county baseline coverage
- **Data Quality**: 86.5% valid statewide ROI, 87.5% valid regional ROI
- **Edge Case Handling**:
  - Negative premiums marked as 999 years (invalid)
  - Missing county baselines use statewide fallback
  - Zero/negative net prices handled as 0.0 ROI years
- **Output**: roi-metrics.csv (327 institutions, 14 fields)
- **Validation**: Statistical analysis confirms reasonable ROI distributions