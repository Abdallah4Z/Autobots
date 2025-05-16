# Data Schema

All files are UTF-8 encoded JSON.  
ID columns are **strings** so facilities (`F1`, `F2`) and neighbourhood numbers (`"3"`) coexist without casting.

---

## `bus_routes.json`

| Field | Type | Units / Domain |
|-------|------|----------------|
| `route_id` | `str` | bus-route ID |
| `stops` | `list[str]` | ordered node IDs |
| `buses_assigned` | `int` | buses |
| `daily_passengers` | `int` | riders / day |

---

## `current_metro_lines.json`

| Field | Type | Units / Domain |
|-------|------|----------------|
| `line_id` | `str` | metro-line ID |
| `name` | `str` | — |
| `stations` | `list[str]` | ordered node IDs |
| `daily_passengers` | `int` | riders / day |

---

## `roads_existing.json`

| Field | Type | Units / Domain |
|-------|------|----------------|
| `from_id` | `str` | node ID |
| `to_id` | `str` | node ID |
| `distance_m` | `float` | metres |
| `capacity_vph` | `int` | vehicles / hour |
| `condition_1_10` | `int` (1–10) | score |

---

## `roads_potential.json`

| Field | Type | Units / Domain |
|-------|------|----------------|
| `from_id` | `str` | node ID |
| `to_id` | `str` | node ID |
| `distance_m` | `float` | metres |
| `capacity_vph` | `int` | vehicles / hour |
| `construction_cost_m_egp` | `int` | million EGP |

---

## `important_facilities.json`

| Field | Type | Units / Domain |
|-------|------|----------------|
| `id` | `str` | facility ID |
| `name` | `str` | — |
| `type` | `str` | category |
| `x` | `float` | longitude (°) |
| `y` | `float` | latitude (°) |

---

## `neighbourhoods.json`

| Field | Type | Units / Domain |
|-------|------|----------------|
| `id` | `int` | neighbourhood ID |
| `name` | `str` | — |
| `population` | `int` | persons |
| `type` | `str` | land-use tag |
| `x` | `float` | longitude (°) |
| `y` | `float` | latitude (°) |

---

## `public_transport_demand.json`

| Field | Type | Units / Domain |
|-------|------|----------------|
| `from_id` | `str` | node ID |
| `to_id` | `str` | node ID |
| `daily_passengers` | `int` | riders / day |

---

## `traffic_flow_patterns.json`

| Field | Type | Units / Domain |
|-------|------|----------------|
| `from_id` | `str` | node ID |
| `to_id` | `str` | node ID |
| `morning_vph` | `int` | vehicles / hour (06-10) |
| `afternoon_vph` | `int` | vehicles / hour (12-16) |
| `evening_vph` | `int` | vehicles / hour (17-20) |
| `night_vph` | `int` | vehicles / hour (22-05) |


