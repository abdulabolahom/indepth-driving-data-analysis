# Findings (Exploration so far)

## Data coverage
- Events: {len(df_events):,} rows | cols: {df_events.shape[1]}
- 1Hz: {len(df_1hz):,} rows | cols: {df_1hz.shape[1]}
- Date range: {df_1hz['when'].min()} → {df_1hz['when'].max()}
- Journeys: {df_1hz['Journey ID'].nunique()}

## Column health (1Hz)
- No nulls in `when`, `speed`, `limit`.
- {X}% bogus limits (==0).
- GPS coverage: {gps_cov:.1%} rows with Latitude+Longitude.

## Next
- A. Speeding → % per hour and per trip.
- B. Accel/decel → derive acceleration, set harsh thresholds.
- C. Maps → plot worst cases with folium.


Human/Story mode

# Findings — Driving Data Audit

## Dataset shapes
- **Events table (df_events):** 23,405 rows × 14 cols  
- **1Hz table (df_1hz):** 1,247,282 rows × 11 cols  

## Coverage
- **Date range:** 2024-11-28 → 2025-07-28  
- **Journeys:** 1,420 distinct trips  

## Data health
- **Key columns completeness:**  
  - `when` ✅ no nulls  
  - `speed` ✅ no nulls  
  - `limit` ✅ no nulls  
  - `Journey ID` ✅ no nulls  
  - `Latitude/Longitude` ✅ no nulls  

## Observations
- Speed limits mostly in 20/30/40 mph buckets (UK pattern).  
- Some bogus `limit=0` rows (should filter out for analysis).  
- Max speed recorded ≈ 87 mph; limits up to 71 mph.  

## Next
- Build map layers for:
  - All journeys
  - Speeding intensity
  - Harsh accel/decel
  - Most visited roads


## 23/Sep
	•	Data shape: Events ~23,405 rows; 1Hz ~1,247,282 rows; 1,420 journeys.
	•	Date range (events): 2024-11-28 → 2025-07-28.
	•	Overall speeding (raw 1Hz): ~1.9% events; max overspeed ~64.6 (likely map-projection/parking-lot misreads).
	•	Episodes: contiguous overspeed segments now available (duration & max over).
	•	Known data quirks: bogus limits (0/5/10 mph) and motorway flyovers → filter thresholds/persistence before scoring.