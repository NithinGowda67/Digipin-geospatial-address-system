# JavaScript Library Guide

Official JavaScript/TypeScript implementation of DIGIPIN for web and Node.js applications.

## Installation

### Node.js / NPM

```bash
npm install digipin-js
```

```javascript
const digipin = require('digipin-js');
```

### ES6 / TypeScript

```typescript
import * as digipin from 'digipin-js';
// Or
import { encode, decode, getNeighbors } from 'digipin-js';
```

### Browser (CDN)

```html
<script src="https://cdn.jsdelivr.net/npm/digipin-js/digipin.js"></script>
<script>
  const code = digipin.encode(28.622788, 77.213033);
  console.log(code); // '39J49LL8T4'
</script>
```

### Local File

```html
<script src="path/to/digipin.js"></script>
<script>
  // Functions available on window.digipin
  const code = digipin.encode(28.6, 77.2);
</script>
```

## Quick Start

### Basic Usage

```javascript
const digipin = require('digipin-js');

// Encode coordinates to DIGIPIN
const code = digipin.encode(28.622788, 77.213033);
console.log(code); // '39J49LL8T4'

// Decode back to coordinates
const coord = digipin.decode('39J49LL8T4');
console.log(coord); // { lat: 28.622788, lon: 77.213033 }

// Validate code
console.log(digipin.isValid('39J49LL8T4')); // true
```

### TypeScript Example

```typescript
import { encode, decode, Coordinate, isValid } from 'digipin-js';

const dakBhawan: Coordinate = { lat: 28.622788, lon: 77.213033 };
const code: string = encode(dakBhawan.lat, dakBhawan.lon);

if (isValid(code)) {
  const location: Coordinate = decode(code);
  console.log(`Location: ${location.lat}, ${location.lon}`);
}
```

## API Reference

### Core Functions

#### `encode(lat, lon, precision?)`

Encodes coordinates to DIGIPIN code.

**Parameters:**
- `lat` (number): Latitude (2.5 to 38.5)
- `lon` (number): Longitude (63.5 to 99.5)
- `precision` (number, optional): Code length (1-10), default 10

**Returns:** `string` - DIGIPIN code

**Throws:** `Error` if coordinates are invalid

**Examples:**
```javascript
// Full precision (10 characters, ~4m)
const code = encode(28.6, 77.2); // '39J49LL8T4'

// City level (5 characters, ~4km)
const cityCode = encode(28.6, 77.2, 5); // '39J49'

// Region level (3 characters, ~63km)
const regionCode = encode(28.6, 77.2, 3); // '39J'
```

#### `decode(code)`

Decodes DIGIPIN code to coordinates (centroid).

**Parameters:**
- `code` (string): DIGIPIN code (1-10 characters)

**Returns:** `{ lat: number, lon: number }` - Coordinate object

**Throws:** `Error` if code is invalid

**Example:**
```javascript
const coord = decode('39J49LL8T4');
console.log(coord.lat, coord.lon); // 28.622788 77.213033
```

#### `isValid(code, strict?)`

Validates DIGIPIN code format.

**Parameters:**
- `code` (string): Code to validate
- `strict` (boolean, optional): If true, requires exactly 10 characters

**Returns:** `boolean`

**Examples:**
```javascript
isValid('39J49LL8T4');      // true
isValid('39J49');            // true
isValid('INVALID');          // false
isValid('39J49', true);      // false (strict mode)
isValid('39J49LL8T4', true); // true
```

#### `isValidCoordinate(lat, lon)`

Validates coordinates are within India's bounding box.

**Parameters:**
- `lat` (number): Latitude
- `lon` (number): Longitude

**Returns:** `boolean`

**Examples:**
```javascript
isValidCoordinate(28.6, 77.2);  // true (Delhi)
isValidCoordinate(51.5, -0.1);  // false (London)
```

#### `getBounds(code)`

Gets the bounding box for a DIGIPIN code.

**Parameters:**
- `code` (string): DIGIPIN code

**Returns:** `{ minLat, maxLat, minLon, maxLon }`

**Throws:** `Error` if code is invalid

**Example:**
```javascript
const bounds = getBounds('39J49LL8T4');
console.log(bounds);
// {
//   minLat: 28.6227...,
//   maxLat: 28.6228...,
//   minLon: 77.2129...,
//   maxLon: 77.2131...
// }
```

#### `getParent(code, level)`

Gets parent code at specified hierarchical level.

**Parameters:**
- `code` (string): DIGIPIN code
- `level` (number): Target precision (1-10)

**Returns:** `string` - Parent code

**Throws:** `Error` if code or level is invalid

**Example:**
```javascript
const fullCode = '39J49LL8T4';
const cityCode = getParent(fullCode, 5);  // '39J49'
const stateCode = getParent(fullCode, 2); // '39'
```

### Neighbor Discovery

#### `getNeighbors(code, direction?)`

Gets immediate neighboring cells.

**Parameters:**
- `code` (string): Center DIGIPIN code
- `direction` (string, optional): Direction filter
  - `'all'` (default): All 8 neighbors
  - `'cardinal'`: Only N, S, E, W (4 neighbors)
  - Specific: `'north'`, `'south'`, `'east'`, `'west'`, `'northeast'`, `'northwest'`, `'southeast'`, `'southwest'`

**Returns:** `string[]` - Array of neighbor codes

**Throws:** `Error` if code or direction is invalid

**Examples:**
```javascript
// All 8 neighbors
const neighbors = getNeighbors('39J49LL8T4');

// Cardinal directions only
const cardinal = getNeighbors('39J49LL8T4', 'cardinal');

// Specific direction
const north = getNeighbors('39J49LL8T4', 'north');
```

#### `getDisk(code, radius?)`

Gets all cells within a radius (filled disk).

**Parameters:**
- `code` (string): Center DIGIPIN code
- `radius` (number, optional): Cell layers (default 1)
  - `0`: Just center
  - `1`: 3×3 grid (9 cells)
  - `2`: 5×5 grid (25 cells)

**Returns:** `string[]` - Array of codes

**Throws:** `Error` if code or radius is invalid

**Examples:**
```javascript
// 3×3 grid (center + 8 neighbors)
const area = getDisk('39J49LL8T4', 1);
console.log(area.length); // 9

// 5×5 grid
const larger = getDisk('39J49LL8T4', 2);
console.log(larger.length); // 25
```

### Batch Operations

#### `batchEncode(coordinates, precision?)`

Batch encode multiple coordinates.

**Parameters:**
- `coordinates` (Array<{lat, lon}>): Array of coordinate objects
- `precision` (number, optional): Code length (default 10)

**Returns:** `string[]` - Array of DIGIPIN codes

**Example:**
```javascript
const locations = [
  { lat: 28.6, lon: 77.2 },
  { lat: 19.0, lon: 72.8 },
  { lat: 13.0, lon: 77.6 }
];

const codes = batchEncode(locations, 5);
// ['39J49', '25C3...', '27F6...']
```

#### `batchDecode(codes)`

Batch decode multiple codes.

**Parameters:**
- `codes` (string[]): Array of DIGIPIN codes

**Returns:** `Array<{lat, lon}>` - Array of coordinate objects

**Example:**
```javascript
const codes = ['39J49LL8T4', '25C3PP9KL6'];
const coords = batchDecode(codes);
// [{ lat: 28.6..., lon: 77.2... }, { lat: 19.0..., lon: 72.8... }]
```

## Real-World Examples

### 1. Store Locator (React)

```jsx
import React, { useState } from 'react';
import { encode, getDisk } from 'digipin-js';

function StoreLocator() {
  const [stores, setStores] = useState([]);

  const findNearbyStores = (userLat, userLon) => {
    // Encode user location (precision 8 = ~60m cells)
    const userCode = encode(userLat, userLon, 8);

    // Search within 5 cells (~300m radius)
    const searchArea = getDisk(userCode, 5);

    // Query stores in this area
    const nearby = allStores.filter(store =>
      searchArea.some(code => store.digipin.startsWith(code))
    );

    setStores(nearby);
  };

  return (
    <div>
      <button onClick={() => findNearbyStores(28.6, 77.2)}>
        Find Stores Near Me
      </button>
      {stores.map(store => (
        <div key={store.id}>{store.name}</div>
      ))}
    </div>
  );
}
```

### 2. Delivery Zone Check (Node.js)

```javascript
const { encode, getDisk } = require('digipin-js');

class DeliveryService {
  constructor(warehouseLat, warehouseLon) {
    this.warehouseCode = encode(warehouseLat, warehouseLon, 8);
    this.deliveryZone = getDisk(this.warehouseCode, 10); // ~600m radius
  }

  canDeliver(customerLat, customerLon) {
    const customerCode = encode(customerLat, customerLon, 8);
    return this.deliveryZone.includes(customerCode);
  }

  getDeliveryFee(customerLat, customerLon) {
    if (!this.canDeliver(customerLat, customerLon)) {
      return null; // Out of range
    }

    const customerCode = encode(customerLat, customerLon, 8);
    const distance = this.calculateDistance(this.warehouseCode, customerCode);

    if (distance <= 5) return 0;    // Free delivery within 5 cells
    if (distance <= 10) return 30;  // ₹30 for 6-10 cells
    return 50;                       // ₹50 for 10+ cells
  }

  calculateDistance(code1, code2) {
    // Simplified distance (Chebyshev)
    const coord1 = decode(code1);
    const coord2 = decode(code2);

    const neighbors = getDisk(code1, 20);
    return neighbors.indexOf(code2);
  }
}

// Usage
const warehouse = new DeliveryService(28.65, 77.22);

console.log(warehouse.canDeliver(28.652, 77.221)); // true
console.log(warehouse.getDeliveryFee(28.652, 77.221)); // 0 (free)
```

### 3. Address Clustering (Data Analysis)

```javascript
const { encode, getParent, batchEncode } = require('digipin-js');

// Cluster addresses by region
function clusterAddresses(addresses, clusterLevel = 6) {
  const clusters = new Map();

  addresses.forEach(addr => {
    const code = encode(addr.lat, addr.lon);
    const clusterKey = getParent(code, clusterLevel);

    if (!clusters.has(clusterKey)) {
      clusters.set(clusterKey, []);
    }
    clusters.get(clusterKey).push(addr);
  });

  return clusters;
}

// Analyze delivery density
const addresses = [
  { id: 1, lat: 28.6, lon: 77.2 },
  { id: 2, lat: 28.601, lon: 77.201 },
  { id: 3, lat: 28.7, lon: 77.3 }
];

const clusters = clusterAddresses(addresses, 6);

clusters.forEach((addrs, region) => {
  console.log(`Region ${region}: ${addrs.length} addresses`);
});
```

### 4. Map Visualization (Leaflet)

```javascript
import L from 'leaflet';
import { decode, getBounds } from 'digipin-js';

function plotDigipinCell(map, code, options = {}) {
  const bounds = getBounds(code);
  const rectangle = L.rectangle(
    [[bounds.minLat, bounds.minLon], [bounds.maxLat, bounds.maxLon]],
    {
      color: options.color || '#3388ff',
      weight: 1,
      fillOpacity: 0.2
    }
  ).addTo(map);

  // Add marker at center
  const center = decode(code);
  L.marker([center.lat, center.lon])
    .bindPopup(`DIGIPIN: ${code}`)
    .addTo(map);

  return rectangle;
}

// Usage
const map = L.map('map').setView([28.6, 77.2], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

plotDigipinCell(map, '39J49LL8T4', { color: 'red' });
```

## TypeScript Types

Full type definitions included:

```typescript
interface Coordinate {
  lat: number;
  lon: number;
}

interface Bounds {
  minLat: number;
  maxLat: number;
  minLon: number;
  maxLon: number;
}

type Direction =
  | 'all'
  | 'cardinal'
  | 'north' | 'south' | 'east' | 'west'
  | 'northeast' | 'northwest' | 'southeast' | 'southwest';

function encode(lat: number, lon: number, precision?: number): string;
function decode(code: string): Coordinate;
function getBounds(code: string): Bounds;
function getNeighbors(code: string, direction?: Direction): string[];
// ... etc
```

## Browser Compatibility

- **Modern browsers**: Chrome, Firefox, Safari, Edge (latest versions)
- **Node.js**: >= 10.0.0
- **IE11**: Use Babel polyfills for ES6 features

## Performance

**Encoding:**
- ~10,000-50,000 operations/second (depends on browser)
- No external dependencies
- Minimal memory footprint (~20KB minified)

**Batch Operations:**
```javascript
// Encode 1000 locations
const start = Date.now();
const codes = batchEncode(locations, 10);
console.log(`Encoded ${codes.length} in ${Date.now() - start}ms`);
// ~20-50ms typical
```

## Testing

Run the test suite:

```bash
cd javascript/
node test.js
```

Example tests:

```javascript
const assert = require('assert');
const { encode, decode, isValid } = require('./digipin');

// Test encoding
const code = encode(28.6, 77.2);
assert(isValid(code), 'Encoded code should be valid');

// Test round-trip
const decoded = decode(code);
const reencoded = encode(decoded.lat, decoded.lon);
assert.strictEqual(reencoded, code, 'Round-trip should preserve code');
```

## Examples

See `javascript/example.js` for comprehensive examples:

```bash
cd javascript/
node example.js
```

## NPM Package Publishing

To publish to NPM:

```bash
cd javascript/
npm login
npm publish --access public
```

## Next Steps

- Integrate with [React/Vue/Angular applications](#real-world-examples)
- Use with mapping libraries (Leaflet, MapBox, Google Maps)
- See [Flask Integration](integrations-flask.md) for backend APIs
- Explore [Use Cases](use-cases.md) for more examples
