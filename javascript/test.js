/**
 * DIGIPIN-JS Test Suite
 *
 * Run with: node test.js
 */

const digipin = require('./digipin.js');

let testsRun = 0;
let testsPassed = 0;
let testsFailed = 0;

function assert(condition, message) {
    testsRun++;
    if (condition) {
        testsPassed++;
        console.log(`✓ ${message}`);
    } else {
        testsFailed++;
        console.error(`✗ ${message}`);
    }
}

function assertEquals(actual, expected, message) {
    testsRun++;
    if (JSON.stringify(actual) === JSON.stringify(expected)) {
        testsPassed++;
        console.log(`✓ ${message}`);
    } else {
        testsFailed++;
        console.error(`✗ ${message}`);
        console.error(`  Expected: ${JSON.stringify(expected)}`);
        console.error(`  Actual:   ${JSON.stringify(actual)}`);
    }
}

function assertThrows(fn, message) {
    testsRun++;
    try {
        fn();
        testsFailed++;
        console.error(`✗ ${message} (expected error, but none was thrown)`);
    } catch (e) {
        testsPassed++;
        console.log(`✓ ${message}`);
    }
}

console.log('\n' + '='.repeat(60));
console.log('DIGIPIN-JS Test Suite');
console.log('='.repeat(60) + '\n');

// -------------------------------------------------------------------------
// Encoding Tests
// -------------------------------------------------------------------------

console.log('Encoding Tests:');
console.log('-'.repeat(60));

const delhiLat = 28.622788;
const delhiLon = 77.213033;
const delhiCode = digipin.encode(delhiLat, delhiLon);

assertEquals(delhiCode.length, 10, 'Encode returns 10-character code by default');
assert(digipin.isValid(delhiCode), 'Encoded code is valid');

const shortCode = digipin.encode(delhiLat, delhiLon, 5);
assertEquals(shortCode.length, 5, 'Encode respects precision parameter');

assertThrows(
    () => digipin.encode(100, 77),
    'Encode throws error for invalid latitude'
);

assertThrows(
    () => digipin.encode(28, 200),
    'Encode throws error for invalid longitude'
);

assertThrows(
    () => digipin.encode(28, 77, 15),
    'Encode throws error for precision > 10'
);

// -------------------------------------------------------------------------
// Decoding Tests
// -------------------------------------------------------------------------

console.log('\nDecoding Tests:');
console.log('-'.repeat(60));

const decoded = digipin.decode(delhiCode);
assert(typeof decoded.lat === 'number', 'Decode returns coordinate object with lat');
assert(typeof decoded.lon === 'number', 'Decode returns coordinate object with lon');

// Round-trip test
const roundTripCode = digipin.encode(decoded.lat, decoded.lon);
assertEquals(roundTripCode, delhiCode, 'Round-trip encoding preserves code');

assertThrows(
    () => digipin.decode('INVALID'),
    'Decode throws error for invalid code'
);

assertThrows(
    () => digipin.decode(''),
    'Decode throws error for empty code'
);

// -------------------------------------------------------------------------
// Validation Tests
// -------------------------------------------------------------------------

console.log('\nValidation Tests:');
console.log('-'.repeat(60));

assert(digipin.isValid('39J49LL8T4'), 'Valid 10-character code passes validation');
assert(digipin.isValid('39J49'), 'Valid 5-character code passes validation');
assert(digipin.isValid('2'), 'Valid 1-character code passes validation');
assert(!digipin.isValid('INVALID123'), 'Invalid characters fail validation');
assert(!digipin.isValid('01234'), 'Disallowed characters (0, 1) fail validation');
assert(!digipin.isValid('ABCDE'), 'Disallowed characters (A, B, D, E) fail validation');
assert(!digipin.isValid(''), 'Empty string fails validation');
assert(!digipin.isValid(null), 'Null fails validation');

assert(digipin.isValid('39J49', false), 'Short code passes non-strict validation');
assert(!digipin.isValid('39J49', true), 'Short code fails strict validation');

assert(digipin.isValidCoordinate(28.6, 77.2), 'Valid Delhi coordinates pass validation');
assert(!digipin.isValidCoordinate(51.5, -0.1), 'London coordinates fail validation');
assert(!digipin.isValidCoordinate(0, 0), 'Coordinates outside India fail validation');

// -------------------------------------------------------------------------
// Bounds Tests
// -------------------------------------------------------------------------

console.log('\nBounds Tests:');
console.log('-'.repeat(60));

const bounds = digipin.getBounds(delhiCode);
assert(typeof bounds.minLat === 'number', 'getBounds returns minLat');
assert(typeof bounds.maxLat === 'number', 'getBounds returns maxLat');
assert(typeof bounds.minLon === 'number', 'getBounds returns minLon');
assert(typeof bounds.maxLon === 'number', 'getBounds returns maxLon');
assert(bounds.minLat < bounds.maxLat, 'minLat < maxLat');
assert(bounds.minLon < bounds.maxLon, 'minLon < maxLon');

// Decoded centroid should be within bounds
assert(
    decoded.lat >= bounds.minLat && decoded.lat <= bounds.maxLat,
    'Decoded lat is within bounds'
);
assert(
    decoded.lon >= bounds.minLon && decoded.lon <= bounds.maxLon,
    'Decoded lon is within bounds'
);

// -------------------------------------------------------------------------
// Parent Tests
// -------------------------------------------------------------------------

console.log('\nParent Tests:');
console.log('-'.repeat(60));

const parent5 = digipin.getParent(delhiCode, 5);
assertEquals(parent5.length, 5, 'getParent returns correct length');
assertEquals(parent5, delhiCode.substring(0, 5), 'getParent truncates correctly');

const parent2 = digipin.getParent(delhiCode, 2);
assertEquals(parent2.length, 2, 'getParent level 2 works');

assertThrows(
    () => digipin.getParent(delhiCode, 15),
    'getParent throws error for invalid level'
);

// -------------------------------------------------------------------------
// Neighbor Tests
// -------------------------------------------------------------------------

console.log('\nNeighbor Tests:');
console.log('-'.repeat(60));

const neighbors = digipin.getNeighbors(delhiCode);
assert(Array.isArray(neighbors), 'getNeighbors returns array');
assert(neighbors.length <= 8, 'getNeighbors returns at most 8 neighbors');
assert(neighbors.length > 0, 'getNeighbors returns at least some neighbors');
assert(!neighbors.includes(delhiCode), 'getNeighbors does not include center');

const cardinal = digipin.getNeighbors(delhiCode, 'cardinal');
assert(cardinal.length <= 4, 'Cardinal direction returns at most 4 neighbors');

const north = digipin.getNeighbors(delhiCode, 'north');
assert(north.length <= 1, 'Specific direction returns at most 1 neighbor');

assertThrows(
    () => digipin.getNeighbors(delhiCode, 'invalid'),
    'getNeighbors throws error for invalid direction'
);

// -------------------------------------------------------------------------
// Disk Tests
// -------------------------------------------------------------------------

console.log('\nDisk Tests:');
console.log('-'.repeat(60));

const disk0 = digipin.getDisk(delhiCode, 0);
assertEquals(disk0.length, 1, 'getDisk radius 0 returns only center');
assert(disk0.includes(delhiCode), 'getDisk radius 0 includes center');

const disk1 = digipin.getDisk(delhiCode, 1);
assert(disk1.length <= 9, 'getDisk radius 1 returns at most 9 cells (3x3)');
assert(disk1.includes(delhiCode), 'getDisk radius 1 includes center');

const disk2 = digipin.getDisk(delhiCode, 2);
assert(disk2.length <= 25, 'getDisk radius 2 returns at most 25 cells (5x5)');

assertThrows(
    () => digipin.getDisk(delhiCode, -1),
    'getDisk throws error for negative radius'
);

// -------------------------------------------------------------------------
// Batch Operations Tests
// -------------------------------------------------------------------------

console.log('\nBatch Operations Tests:');
console.log('-'.repeat(60));

const coords = [
    { lat: 28.6, lon: 77.2 },
    { lat: 19.0, lon: 72.8 },
    { lat: 13.0, lon: 77.6 }
];

const codes = digipin.batchEncode(coords);
assertEquals(codes.length, 3, 'batchEncode returns correct number of codes');
assert(codes.every(c => digipin.isValid(c)), 'All batch encoded codes are valid');

const decodedCoords = digipin.batchDecode(codes);
assertEquals(decodedCoords.length, 3, 'batchDecode returns correct number of coordinates');
assert(decodedCoords.every(c => typeof c.lat === 'number'), 'All batch decoded have lat');
assert(decodedCoords.every(c => typeof c.lon === 'number'), 'All batch decoded have lon');

// -------------------------------------------------------------------------
// Constants Tests
// -------------------------------------------------------------------------

console.log('\nConstants Tests:');
console.log('-'.repeat(60));

assert(typeof digipin.ALPHABET === 'string', 'ALPHABET is defined');
assertEquals(digipin.ALPHABET.length, 16, 'ALPHABET has 16 characters');
assert(typeof digipin.INDIA_BOUNDS === 'object', 'INDIA_BOUNDS is defined');
assert(digipin.INDIA_BOUNDS.MIN_LAT === 2.5, 'INDIA_BOUNDS.MIN_LAT is correct');

// -------------------------------------------------------------------------
// Test Summary
// -------------------------------------------------------------------------

console.log('\n' + '='.repeat(60));
console.log('Test Summary');
console.log('='.repeat(60));
console.log(`Total tests:  ${testsRun}`);
console.log(`Passed:       ${testsPassed} ✓`);
console.log(`Failed:       ${testsFailed} ✗`);
console.log(`Success rate: ${((testsPassed / testsRun) * 100).toFixed(1)}%`);
console.log('='.repeat(60) + '\n');

if (testsFailed === 0) {
    console.log('🎉 All tests passed!\n');
    process.exit(0);
} else {
    console.error('❌ Some tests failed.\n');
    process.exit(1);
}
