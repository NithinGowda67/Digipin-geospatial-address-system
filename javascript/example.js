/**
 * DIGIPIN-JS Usage Examples
 *
 * Run with: node example.js
 */

const digipin = require('./digipin.js');

console.log('\n' + '='.repeat(70));
console.log('DIGIPIN-JS - Usage Examples');
console.log('='.repeat(70) + '\n');

// -------------------------------------------------------------------------
// Example 1: Basic Encoding
// -------------------------------------------------------------------------

console.log('Example 1: Basic Encoding');
console.log('-'.repeat(70));

const dakBhawanLat = 28.622788;
const dakBhawanLon = 77.213033;

const code = digipin.encode(dakBhawanLat, dakBhawanLon);
console.log(`Location: Dak Bhawan, New Delhi`);
console.log(`Coordinates: ${dakBhawanLat}, ${dakBhawanLon}`);
console.log(`DIGIPIN Code: ${code}`);
console.log();

// -------------------------------------------------------------------------
// Example 2: Variable Precision
// -------------------------------------------------------------------------

console.log('Example 2: Variable Precision Levels');
console.log('-'.repeat(70));

const lat = 19.076090;
const lon = 72.877426;

console.log(`Location: Mumbai, Maharashtra`);
console.log(`Coordinates: ${lat}, ${lon}\n`);

for (let precision = 1; precision <= 10; precision++) {
    const code = digipin.encode(lat, lon, precision);
    const resolutions = [
        '~1000 km (Country)',
        '~250 km (State)',
        '~63 km (Region)',
        '~16 km (District)',
        '~4 km (City)',
        '~1 km (Area)',
        '~250 m (Neighborhood)',
        '~60 m (Street)',
        '~15 m (Building)',
        '~4 m (Door)'
    ];
    console.log(`Level ${String(precision).padStart(2)}: ${code.padEnd(10)} - ${resolutions[precision - 1]}`);
}
console.log();

// -------------------------------------------------------------------------
// Example 3: Decoding
// -------------------------------------------------------------------------

console.log('Example 3: Decoding DIGIPIN Codes');
console.log('-'.repeat(70));

const testCodes = [
    '39J49LL8T4',  // Delhi
    '25C3PP9KL6',  // Mumbai (approximate)
    '27F6MM7JC8'   // Bangalore (approximate)
];

testCodes.forEach(code => {
    const coord = digipin.decode(code);
    const bounds = digipin.getBounds(code);
    console.log(`Code: ${code}`);
    console.log(`  Centroid: ${coord.lat.toFixed(6)}, ${coord.lon.toFixed(6)}`);
    console.log(`  Bounds: [${bounds.minLat.toFixed(6)}, ${bounds.maxLat.toFixed(6)}] x [${bounds.minLon.toFixed(6)}, ${bounds.maxLon.toFixed(6)}]`);
    console.log();
});

// -------------------------------------------------------------------------
// Example 4: Validation
// -------------------------------------------------------------------------

console.log('Example 4: Code Validation');
console.log('-'.repeat(70));

const testValidation = [
    { code: '39J49LL8T4', desc: 'Valid full code' },
    { code: '39J49', desc: 'Valid short code' },
    { code: 'INVALID123', desc: 'Invalid characters' },
    { code: '01234ABCDE', desc: 'Disallowed characters' },
    { code: '', desc: 'Empty string' }
];

testValidation.forEach(({ code, desc }) => {
    const valid = digipin.isValid(code);
    const icon = valid ? '✓' : '✗';
    console.log(`${icon} ${desc.padEnd(25)} "${code}" - ${valid ? 'Valid' : 'Invalid'}`);
});
console.log();

// -------------------------------------------------------------------------
// Example 5: Hierarchical Relationships
// -------------------------------------------------------------------------

console.log('Example 5: Hierarchical Parent Codes');
console.log('-'.repeat(70));

const fullCode = '39J49LL8T4';
console.log(`Full Code: ${fullCode}\n`);

for (let level = 1; level <= 5; level++) {
    const parent = digipin.getParent(fullCode, level);
    console.log(`  Level ${level} parent: ${parent}`);
}
console.log();

// -------------------------------------------------------------------------
// Example 6: Neighbor Discovery
// -------------------------------------------------------------------------

console.log('Example 6: Finding Neighbors');
console.log('-'.repeat(70));

const centerCode = '39J49LL8T4';
console.log(`Center Code: ${centerCode}\n`);

// All neighbors
const allNeighbors = digipin.getNeighbors(centerCode);
console.log(`All neighbors (${allNeighbors.length}):`);
console.log(`  ${allNeighbors.slice(0, 4).join(', ')}`);
console.log(`  ${allNeighbors.slice(4).join(', ')}\n`);

// Cardinal directions only
const cardinalNeighbors = digipin.getNeighbors(centerCode, 'cardinal');
console.log(`Cardinal neighbors (${cardinalNeighbors.length}): ${cardinalNeighbors.join(', ')}\n`);

// Specific direction
const northNeighbor = digipin.getNeighbors(centerCode, 'north');
console.log(`North neighbor: ${northNeighbor.join(', ')}`);
console.log();

// -------------------------------------------------------------------------
// Example 7: Search Area (Disk)
// -------------------------------------------------------------------------

console.log('Example 7: Creating Search Areas');
console.log('-'.repeat(70));

const searchCenter = '39J49LL8T4';

for (let radius of [0, 1, 2]) {
    const disk = digipin.getDisk(searchCenter, radius);
    const gridSize = (2 * radius + 1);
    console.log(`Radius ${radius} (${gridSize}x${gridSize} grid): ${disk.length} cells`);
}
console.log();

// -------------------------------------------------------------------------
// Example 8: Batch Operations
// -------------------------------------------------------------------------

console.log('Example 8: Batch Encoding/Decoding');
console.log('-'.repeat(70));

const locations = [
    { name: 'Delhi', lat: 28.6, lon: 77.2 },
    { name: 'Mumbai', lat: 19.0, lon: 72.8 },
    { name: 'Bangalore', lat: 13.0, lon: 77.6 },
    { name: 'Chennai', lat: 13.0, lon: 80.2 },
    { name: 'Kolkata', lat: 22.5, lon: 88.3 }
];

const coords = locations.map(l => ({ lat: l.lat, lon: l.lon }));
const codes = digipin.batchEncode(coords, 5);

console.log('Batch Encoded Cities (Precision 5):\n');
locations.forEach((loc, i) => {
    console.log(`  ${loc.name.padEnd(12)}: ${codes[i]}`);
});
console.log();

// -------------------------------------------------------------------------
// Example 9: Real-World Use Case - Delivery Zone
// -------------------------------------------------------------------------

console.log('Example 9: Real-World Use Case - Delivery Zones');
console.log('-'.repeat(70));

const warehouseLat = 28.65;
const warehouseLon = 77.22;
const warehouseCode = digipin.encode(warehouseLat, warehouseLon, 8);

console.log(`Warehouse Location: ${warehouseLat}, ${warehouseLon}`);
console.log(`Warehouse Code (Level 8): ${warehouseCode}\n`);

// Define delivery radius (2 cells = ~120m at level 8)
const deliveryRadius = 2;
const deliveryZone = digipin.getDisk(warehouseCode, deliveryRadius);

console.log(`Delivery Zone:`);
console.log(`  Radius: ${deliveryRadius} cells`);
console.log(`  Coverage: ${deliveryZone.length} cells (5x5 grid)`);
console.log(`  Approximate area: ~${(deliveryZone.length * 60 * 60).toLocaleString()} sq meters\n`);

// Customer location
const customerLat = 28.652;
const customerLon = 77.221;
const customerCode = digipin.encode(customerLat, customerLon, 8);

const canDeliver = deliveryZone.includes(customerCode);
console.log(`Customer Location: ${customerLat}, ${customerLon}`);
console.log(`Customer Code: ${customerCode}`);
console.log(`Can Deliver: ${canDeliver ? '✓ YES' : '✗ NO'}`);
console.log();

// -------------------------------------------------------------------------
// Example 10: Constants and Metadata
// -------------------------------------------------------------------------

console.log('Example 10: Constants and Metadata');
console.log('-'.repeat(70));

console.log(`Valid Alphabet: ${digipin.ALPHABET}`);
console.log(`Alphabet Length: ${digipin.ALPHABET.length} characters`);
console.log(`\nIndia Bounding Box:`);
console.log(`  Latitude:  ${digipin.INDIA_BOUNDS.MIN_LAT}° to ${digipin.INDIA_BOUNDS.MAX_LAT}°`);
console.log(`  Longitude: ${digipin.INDIA_BOUNDS.MIN_LON}° to ${digipin.INDIA_BOUNDS.MAX_LON}°`);

console.log('\n' + '='.repeat(70));
console.log('End of Examples');
console.log('='.repeat(70) + '\n');
