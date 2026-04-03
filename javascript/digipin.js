/**
 * DIGIPIN-JS
 * Official JavaScript implementation of India's national geocoding standard
 *
 * @version 1.2.0
 * @license MIT
 */

/**
 * India's bounding box coordinates
 */
const INDIA_BOUNDS = {
    MIN_LAT: 2.5,
    MAX_LAT: 38.5,
    MIN_LON: 63.5,
    MAX_LON: 99.5
};

/**
 * Valid characters for DIGIPIN codes (excluding 0, 1, A, B, D, E, etc.)
 */
const ALPHABET = '23456789CFJKLMPT';

/**
 * Grid size calculator for each precision level
 */
const GRID_SIZES = [
    { lat: 18.0, lon: 18.0 },      // Level 1
    { lat: 4.5, lon: 4.5 },        // Level 2
    { lat: 1.125, lon: 1.125 },    // Level 3
    { lat: 0.28125, lon: 0.28125 }, // Level 4
    { lat: 0.0703125, lon: 0.0703125 }, // Level 5
    { lat: 0.01757813, lon: 0.01757813 }, // Level 6
    { lat: 0.00439453, lon: 0.00439453 }, // Level 7
    { lat: 0.00109863, lon: 0.00109863 }, // Level 8
    { lat: 0.00027466, lon: 0.00027466 }, // Level 9
    { lat: 0.00006866, lon: 0.00006866 }  // Level 10
];

/**
 * Validates if coordinates are within India's bounding box
 * @param {number} lat - Latitude
 * @param {number} lon - Longitude
 * @returns {boolean} True if valid
 */
function isValidCoordinate(lat, lon) {
    return lat >= INDIA_BOUNDS.MIN_LAT &&
           lat <= INDIA_BOUNDS.MAX_LAT &&
           lon >= INDIA_BOUNDS.MIN_LON &&
           lon <= INDIA_BOUNDS.MAX_LON;
}

/**
 * Validates DIGIPIN code format
 * @param {string} code - DIGIPIN code to validate
 * @param {boolean} strict - If true, requires exactly 10 characters
 * @returns {boolean} True if valid
 */
function isValid(code, strict = false) {
    if (!code || typeof code !== 'string') return false;

    const upperCode = code.toUpperCase();
    const length = upperCode.length;

    // Check length
    if (strict && length !== 10) return false;
    if (length < 1 || length > 10) return false;

    // Check characters
    for (let char of upperCode) {
        if (!ALPHABET.includes(char)) return false;
    }

    return true;
}

/**
 * Encodes latitude/longitude into DIGIPIN code
 * @param {number} lat - Latitude (2.5 to 38.5)
 * @param {number} lon - Longitude (63.5 to 99.5)
 * @param {number} precision - Code length (1-10), default 10
 * @returns {string} DIGIPIN code
 * @throws {Error} If coordinates are invalid
 */
function encode(lat, lon, precision = 10) {
    // Validate inputs
    if (typeof lat !== 'number' || typeof lon !== 'number') {
        throw new Error('Latitude and longitude must be numbers');
    }

    if (!isValidCoordinate(lat, lon)) {
        throw new Error(
            `Coordinates (${lat}, ${lon}) are outside India's bounding box. ` +
            `Valid range: lat ${INDIA_BOUNDS.MIN_LAT}-${INDIA_BOUNDS.MAX_LAT}, ` +
            `lon ${INDIA_BOUNDS.MIN_LON}-${INDIA_BOUNDS.MAX_LON}`
        );
    }

    if (!Number.isInteger(precision) || precision < 1 || precision > 10) {
        throw new Error('Precision must be an integer between 1 and 10');
    }

    let code = '';
    let minLat = INDIA_BOUNDS.MIN_LAT;
    let maxLat = INDIA_BOUNDS.MAX_LAT;
    let minLon = INDIA_BOUNDS.MIN_LON;
    let maxLon = INDIA_BOUNDS.MAX_LON;

    for (let level = 0; level < precision; level++) {
        // Calculate grid dimensions for current level
        const latStep = (maxLat - minLat) / 4;
        const lonStep = (maxLon - minLon) / 4;

        // Determine which cell (0-15) contains the point
        const latIndex = Math.min(3, Math.floor((lat - minLat) / latStep));
        const lonIndex = Math.min(3, Math.floor((lon - minLon) / lonStep));

        // Calculate spiral index
        const cellIndex = _spiralIndex(latIndex, lonIndex);

        // Add character to code
        code += ALPHABET[cellIndex];

        // Update bounds for next iteration
        minLat += latIndex * latStep;
        maxLat = minLat + latStep;
        minLon += lonIndex * lonStep;
        maxLon = minLon + lonStep;
    }

    return code;
}

/**
 * Decodes DIGIPIN code to latitude/longitude (centroid)
 * @param {string} code - DIGIPIN code (1-10 characters)
 * @returns {{lat: number, lon: number}} Coordinates object
 * @throws {Error} If code is invalid
 */
function decode(code) {
    if (!isValid(code)) {
        throw new Error(`Invalid DIGIPIN code: ${code}`);
    }

    const upperCode = code.toUpperCase();
    let minLat = INDIA_BOUNDS.MIN_LAT;
    let maxLat = INDIA_BOUNDS.MAX_LAT;
    let minLon = INDIA_BOUNDS.MIN_LON;
    let maxLon = INDIA_BOUNDS.MAX_LON;

    for (let char of upperCode) {
        const cellIndex = ALPHABET.indexOf(char);
        const { row, col } = _reverseSpiral(cellIndex);

        const latStep = (maxLat - minLat) / 4;
        const lonStep = (maxLon - minLon) / 4;

        minLat += row * latStep;
        maxLat = minLat + latStep;
        minLon += col * lonStep;
        maxLon = minLon + lonStep;
    }

    // Return centroid
    return {
        lat: (minLat + maxLat) / 2,
        lon: (minLon + maxLon) / 2
    };
}

/**
 * Gets the bounding box for a DIGIPIN code
 * @param {string} code - DIGIPIN code
 * @returns {{minLat: number, maxLat: number, minLon: number, maxLon: number}}
 * @throws {Error} If code is invalid
 */
function getBounds(code) {
    if (!isValid(code)) {
        throw new Error(`Invalid DIGIPIN code: ${code}`);
    }

    const upperCode = code.toUpperCase();
    let minLat = INDIA_BOUNDS.MIN_LAT;
    let maxLat = INDIA_BOUNDS.MAX_LAT;
    let minLon = INDIA_BOUNDS.MIN_LON;
    let maxLon = INDIA_BOUNDS.MAX_LON;

    for (let char of upperCode) {
        const cellIndex = ALPHABET.indexOf(char);
        const { row, col } = _reverseSpiral(cellIndex);

        const latStep = (maxLat - minLat) / 4;
        const lonStep = (maxLon - minLon) / 4;

        minLat += row * latStep;
        maxLat = minLat + latStep;
        minLon += col * lonStep;
        maxLon = minLon + lonStep;
    }

    return { minLat, maxLat, minLon, maxLon };
}

/**
 * Gets parent code at specified level
 * @param {string} code - DIGIPIN code
 * @param {number} level - Target precision level (1-10)
 * @returns {string} Parent code
 * @throws {Error} If code is invalid or level is invalid
 */
function getParent(code, level) {
    if (!isValid(code)) {
        throw new Error(`Invalid DIGIPIN code: ${code}`);
    }

    if (!Number.isInteger(level) || level < 1 || level > 10) {
        throw new Error('Level must be an integer between 1 and 10');
    }

    const upperCode = code.toUpperCase();

    if (level >= upperCode.length) {
        return upperCode;
    }

    return upperCode.substring(0, level);
}

/**
 * Gets immediate neighboring cells
 * @param {string} code - Center DIGIPIN code
 * @param {string} direction - 'all' (8 neighbors), 'cardinal' (4 neighbors), or specific direction
 * @returns {string[]} Array of neighbor codes
 * @throws {Error} If code or direction is invalid
 */
function getNeighbors(code, direction = 'all') {
    if (!isValid(code)) {
        throw new Error(`Invalid DIGIPIN code: ${code}`);
    }

    const { lat, lon } = decode(code);
    const level = code.length;
    const gridSize = GRID_SIZES[level - 1];

    const offsets = {
        north: [1, 0],
        northeast: [1, 1],
        east: [0, 1],
        southeast: [-1, 1],
        south: [-1, 0],
        southwest: [-1, -1],
        west: [0, -1],
        northwest: [1, -1]
    };

    let selectedOffsets;

    if (direction === 'all') {
        selectedOffsets = Object.values(offsets);
    } else if (direction === 'cardinal') {
        selectedOffsets = [offsets.north, offsets.south, offsets.east, offsets.west];
    } else if (offsets[direction]) {
        selectedOffsets = [offsets[direction]];
    } else {
        throw new Error(`Invalid direction: ${direction}`);
    }

    const neighbors = [];
    const upperCode = code.toUpperCase();

    for (let [latMult, lonMult] of selectedOffsets) {
        const nLat = lat + (latMult * gridSize.lat);
        const nLon = lon + (lonMult * gridSize.lon);

        if (isValidCoordinate(nLat, nLon)) {
            try {
                const nCode = encode(nLat, nLon, level);
                if (nCode !== upperCode) {
                    neighbors.push(nCode);
                }
            } catch (e) {
                // Skip invalid coordinates
            }
        }
    }

    return neighbors;
}

/**
 * Gets all cells within a radius (filled disk)
 * @param {string} code - Center DIGIPIN code
 * @param {number} radius - Number of cell layers (0 = center only, 1 = 3x3 grid, etc.)
 * @returns {string[]} Array of codes covering the disk
 * @throws {Error} If code or radius is invalid
 */
function getDisk(code, radius = 1) {
    if (!isValid(code)) {
        throw new Error(`Invalid DIGIPIN code: ${code}`);
    }

    if (!Number.isInteger(radius) || radius < 0) {
        throw new Error('Radius must be a non-negative integer');
    }

    const { lat, lon } = decode(code);
    const level = code.length;
    const gridSize = GRID_SIZES[level - 1];

    const cells = new Set();

    for (let dy = -radius; dy <= radius; dy++) {
        for (let dx = -radius; dx <= radius; dx++) {
            const nLat = lat + (dy * gridSize.lat);
            const nLon = lon + (dx * gridSize.lon);

            if (isValidCoordinate(nLat, nLon)) {
                try {
                    const nCode = encode(nLat, nLon, level);
                    cells.add(nCode);
                } catch (e) {
                    // Skip invalid coordinates
                }
            }
        }
    }

    return Array.from(cells);
}

/**
 * Gets all cells at exactly radius distance (hollow ring)
 * Uses Chebyshev distance (chessboard distance) where diagonal moves count as 1 step
 * @param {string} code - Center DIGIPIN code
 * @param {number} radius - Distance in cells (must be >= 1)
 * @returns {string[]} Array of codes forming the ring at specified radius
 * @throws {Error} If code or radius is invalid
 * @example
 * // Get cells exactly 1 step away (8 immediate neighbors)
 * getRing('39J49LL8T4', 1); // Returns ~8 neighbors
 *
 * // Get cells exactly 2 steps away (outer ring)
 * getRing('39J49LL8T4', 2); // Returns up to 16 cells
 */
function getRing(code, radius) {
    if (!isValid(code)) {
        throw new Error(`Invalid DIGIPIN code: ${code}`);
    }

    if (!Number.isInteger(radius) || radius < 1) {
        throw new Error('Radius must be an integer >= 1');
    }

    const { lat, lon } = decode(code);
    const level = code.length;
    const gridSize = GRID_SIZES[level - 1];
    const upperCode = code.toUpperCase();

    const cells = new Set();

    // For a ring at radius R, we need cells where max(|dx|, |dy|) = R
    // This means either |dx| = R or |dy| = R (or both)

    // Top and bottom edges (full width)
    for (let dx = -radius; dx <= radius; dx++) {
        for (let dy of [radius, -radius]) {
            const nLat = lat + (dy * gridSize.lat);
            const nLon = lon + (dx * gridSize.lon);

            if (isValidCoordinate(nLat, nLon)) {
                try {
                    const nCode = encode(nLat, nLon, level);
                    if (nCode !== upperCode) {
                        cells.add(nCode);
                    }
                } catch (e) {
                    // Skip invalid coordinates
                }
            }
        }
    }

    // Left and right edges (excluding corners already added)
    for (let dy = -radius + 1; dy < radius; dy++) {
        for (let dx of [radius, -radius]) {
            const nLat = lat + (dy * gridSize.lat);
            const nLon = lon + (dx * gridSize.lon);

            if (isValidCoordinate(nLat, nLon)) {
                try {
                    const nCode = encode(nLat, nLon, level);
                    if (nCode !== upperCode) {
                        cells.add(nCode);
                    }
                } catch (e) {
                    // Skip invalid coordinates
                }
            }
        }
    }

    return Array.from(cells);
}

/**
 * Batch encode multiple coordinate pairs
 * @param {Array<{lat: number, lon: number}>} coordinates - Array of coordinate objects
 * @param {number} precision - Code length (1-10), default 10
 * @returns {string[]} Array of DIGIPIN codes
 */
function batchEncode(coordinates, precision = 10) {
    return coordinates.map(coord => encode(coord.lat, coord.lon, precision));
}

/**
 * Batch decode multiple DIGIPIN codes
 * @param {string[]} codes - Array of DIGIPIN codes
 * @returns {Array<{lat: number, lon: number}>} Array of coordinate objects
 */
function batchDecode(codes) {
    return codes.map(code => decode(code));
}

// -------------------------------------------------------------------------
// Internal Helper Functions
// -------------------------------------------------------------------------

/**
 * Converts row/col to spiral index (0-15)
 * Uses the official DIGIPIN spiral pattern
 */
function _spiralIndex(row, col) {
    const spiralMap = [
        [0, 1, 2, 9],
        [3, 4, 11, 10],
        [5, 12, 13, 8],
        [6, 7, 14, 15]
    ];
    return spiralMap[row][col];
}

/**
 * Converts spiral index to row/col
 */
function _reverseSpiral(index) {
    const reverseSpiralMap = [
        { row: 0, col: 0 }, { row: 0, col: 1 }, { row: 0, col: 2 }, { row: 1, col: 0 },
        { row: 1, col: 1 }, { row: 2, col: 0 }, { row: 3, col: 0 }, { row: 3, col: 1 },
        { row: 2, col: 3 }, { row: 0, col: 3 }, { row: 1, col: 3 }, { row: 1, col: 2 },
        { row: 2, col: 1 }, { row: 2, col: 2 }, { row: 3, col: 2 }, { row: 3, col: 3 }
    ];
    return reverseSpiralMap[index];
}

// -------------------------------------------------------------------------
// Exports
// -------------------------------------------------------------------------

// CommonJS
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        encode,
        decode,
        isValid,
        isValidCoordinate,
        getBounds,
        getParent,
        getNeighbors,
        getDisk,
        getRing,
        batchEncode,
        batchDecode,
        INDIA_BOUNDS,
        ALPHABET
    };
}

// ES6
if (typeof window !== 'undefined') {
    window.digipin = {
        encode,
        decode,
        isValid,
        isValidCoordinate,
        getBounds,
        getParent,
        getNeighbors,
        getDisk,
        getRing,
        batchEncode,
        batchDecode,
        INDIA_BOUNDS,
        ALPHABET
    };
}
