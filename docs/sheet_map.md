# Sheet map

| Sheet name        | What is it (1 line)                     | Where does the table start? | More than one table? | What does a row represent?     | Keep / Maybe / Drop | Notes |
|-------------------|-----------------------------------------|-----------------------------|----------------------|--------------------------------|---------------------|-------|
| Policy Holder     | Metadata about policy & request          | Row 8                       | Yes                  | Not raw data                   | Drop                | Logo, policy number, request type only |
| Reference         | Definitions of terms used in data        | Row 10, 62, 121, 151        | Yes                  | Term + definition               | Drop (for now)      | Useful for documentation, not analysis |
| Information Exchange | One table with personal info          | Row ? (top)                 | No                   | One row = your details          | Drop                | Not analytical data |
| Journey Event     | Event-level driving data (telemetry)     | Row ~?? (after legend map)  | Yes                  | One row = event (GPS + time)    | Keep                | Main dataset; legend on top, totals at bottom |
| Journey Event 1Hz - Part 1 | High frequency event data        | Row ~??                     | No                   | One row = event (higher freq)   | Keep                | Same as above, but different date ranges |
| Journey Event 1Hz - Part 2 | Same as part 1 (different dates) | Row ~??                     | No                   | One row = event (higher freq)   | Keep                | Dates: 05/11/2024 – 05/08/2025 |
| Journey Event 1Hz - Part 3 | Same as part 1 (different dates) | Row ~??                     | No                   | One row = event (higher freq)   | Keep                | Dates: later period |
| Connection        | Device health check events               | Row ?                       | No                   | One row = health check event    | Maybe               | Structure similar to Journey Event |
| Installation      | Black box installation info              | Row ?                       | No                   | One row = install operation     | Maybe               | Could be useful in another project |
| Missed Appointments | Empty                                  | -                           | -                    | -                              | Drop                | Empty sheet |
| Contact Attempts  | Empty                                   | -                           | -                    | -                              | Drop                | Empty sheet |
| Anomalies         | Empty                                   | -                           | -                    | -                              | Drop                | Empty sheet |