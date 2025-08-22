# Data Dictionary

## Journey_Event_Sample — minimal keep set

| Column name              | Data type | Meaning                                           | Keep/Maybe/Drop | Notes |
|--------------------------|-----------|---------------------------------------------------|-----------------|-------|
| Event Time Stamp         | datetime  | Device-recorded event time                        | Keep            | Day-first parsing; compare with GPS time if needed |
| GPS Date Time            | datetime  | GPS-derived timestamp                             | Keep            | Prefer for ordering when present |
| RTC Date Time            | datetime  | Device real-time clock timestamp                  | Keep            | Secondary reference time |
| Latitude                 | float     | GPS latitude (WGS84)                              | Keep            | May contain NaN |
| Longitude                | float     | GPS longitude (WGS84)                             | Keep            | May contain NaN |
| Horizontal Speed         | float     | Instantaneous speed at event                      | Keep            | Units TBD (mph or km/h) |
| Road Speed Limit         | float     | Posted speed limit at location                     | Keep            | Units TBD; cross-check with country |
| Journey ID               | string    | Journey/session identifier                         | Keep            | Likely primary join key within workbook |
| Policy Number            | string    | Insurance policy identifier                        | Maybe           | Often constant in this dataset |
| Voucher ID               | string    | Device/account identifier                          | Maybe           | Often constant; keep if varies |
| Accumulated Trip Distance| int       | Cumulative distance within trip                    | Keep            | Units TBD (m or km) |
| Accumulated Trip Idle Time | int     | Cumulative idle time                               | Keep            | Units TBD (sec?) |
| Accumulated Trip Run Time  | int     | Cumulative engine/run time                         | Keep            | Units TBD (sec?) |
| Time Elapsed             | float     | Elapsed time since trip start (bucketed?)          | Maybe           | Mostly 60s → likely minute ticks |
| VIN                      | string    | Vehicle identification number                      | Drop            | 100% null in sample |


| Column name            | Data type | Meaning                                                | Keep/Maybe/Drop | Notes |
|------------------------|-----------|--------------------------------------------------------|-----------------|-------|
| Event Type             | string    | Label describing the event at this timestamp           | Keep            | Use for grouping/filtering (e.g., ignition, trip tick) |
| Delta Trip Distance    | float/int | Distance added since previous event                    | Keep            | Units TBD (m or km); 0 for idle ticks |
| Direction              | float     | Bearing at event (degrees from North)                  | Maybe           | Expected 0–359; may be noisy when stationary |
| Altitude               | float/int | Elevation above sea level                              | Maybe           | Units TBD (meters?); may be missing |
| GPS Accuracy           | float     | Reported GPS accuracy error                            | Maybe           | Lower is better; scale/units TBD |