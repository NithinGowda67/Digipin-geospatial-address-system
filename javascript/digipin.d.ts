/**
 * DIGIPIN-JS TypeScript Definitions
 * Official JavaScript implementation of India's national geocoding standard
 */

/**
 * Coordinate object
 */
export interface Coordinate {
    lat: number;
    lon: number;
}

/**
 * Bounding box for a DIGIPIN cell
 */
export interface Bounds {
    minLat: number;
    maxLat: number;
    minLon: number;
    maxLon: number;
}

/**
 * India's bounding box coordinates
 */
export interface IndiaBounds {
    MIN_LAT: number;
    MAX_LAT: number;
    MIN_LON: number;
    MAX_LON: number;
}

/**
 * Valid direction types for neighbor discovery
 */
export type Direction =
    | 'all'
    | 'cardinal'
    | 'north'
    | 'south'
    | 'east'
    | 'west'
    | 'northeast'
    | 'northwest'
    | 'southeast'
    | 'southwest';

/**
 * Encodes latitude/longitude into DIGIPIN code
 * @param lat - Latitude (2.5 to 38.5)
 * @param lon - Longitude (63.5 to 99.5)
 * @param precision - Code length (1-10), default 10
 * @returns DIGIPIN code
 * @throws {Error} If coordinates are invalid
 * @example
 * const code = encode(28.622788, 77.213033); // '39J49LL8T4'
 * const shortCode = encode(28.622788, 77.213033, 5); // '39J49'
 */
export function encode(lat: number, lon: number, precision?: number): string;

/**
 * Decodes DIGIPIN code to latitude/longitude (centroid)
 * @param code - DIGIPIN code (1-10 characters)
 * @returns Coordinate object with lat and lon
 * @throws {Error} If code is invalid
 * @example
 * const coord = decode('39J49LL8T4'); // { lat: 28.622788, lon: 77.213033 }
 */
export function decode(code: string): Coordinate;

/**
 * Validates DIGIPIN code format
 * @param code - DIGIPIN code to validate
 * @param strict - If true, requires exactly 10 characters
 * @returns True if valid
 * @example
 * isValid('39J49LL8T4'); // true
 * isValid('INVALID'); // false
 * isValid('39J49', true); // false (strict mode requires 10 chars)
 */
export function isValid(code: string, strict?: boolean): boolean;

/**
 * Validates if coordinates are within India's bounding box
 * @param lat - Latitude
 * @param lon - Longitude
 * @returns True if valid
 * @example
 * isValidCoordinate(28.6, 77.2); // true (Delhi)
 * isValidCoordinate(51.5, -0.1); // false (London)
 */
export function isValidCoordinate(lat: number, lon: number): boolean;

/**
 * Gets the bounding box for a DIGIPIN code
 * @param code - DIGIPIN code
 * @returns Bounds object with minLat, maxLat, minLon, maxLon
 * @throws {Error} If code is invalid
 * @example
 * const bounds = getBounds('39J49LL8T4');
 * // { minLat: 28.622..., maxLat: 28.623..., minLon: 77.212..., maxLon: 77.213... }
 */
export function getBounds(code: string): Bounds;

/**
 * Gets parent code at specified level
 * @param code - DIGIPIN code
 * @param level - Target precision level (1-10)
 * @returns Parent code
 * @throws {Error} If code is invalid or level is invalid
 * @example
 * getParent('39J49LL8T4', 5); // '39J49'
 * getParent('39J49LL8T4', 2); // '39'
 */
export function getParent(code: string, level: number): string;

/**
 * Gets immediate neighboring cells
 * @param code - Center DIGIPIN code
 * @param direction - 'all' (8 neighbors), 'cardinal' (4 neighbors), or specific direction
 * @returns Array of neighbor codes
 * @throws {Error} If code or direction is invalid
 * @example
 * // Get all 8 neighbors
 * const neighbors = getNeighbors('39J49LL8T4');
 *
 * // Get only cardinal directions (N, S, E, W)
 * const cardinalNeighbors = getNeighbors('39J49LL8T4', 'cardinal');
 *
 * // Get specific direction
 * const northNeighbor = getNeighbors('39J49LL8T4', 'north');
 */
export function getNeighbors(code: string, direction?: Direction): string[];

/**
 * Gets all cells within a radius (filled disk)
 * @param code - Center DIGIPIN code
 * @param radius - Number of cell layers (0 = center only, 1 = 3x3 grid, etc.)
 * @returns Array of codes covering the disk
 * @throws {Error} If code or radius is invalid
 * @example
 * // Get 3x3 grid (center + 8 neighbors)
 * const area = getDisk('39J49LL8T4', 1);
 *
 * // Get 5x5 grid
 * const largerArea = getDisk('39J49LL8T4', 2);
 */
export function getDisk(code: string, radius?: number): string[];

/**
 * Gets all cells at exactly radius distance (hollow ring)
 * Uses Chebyshev distance (chessboard distance) where diagonal moves count as 1 step
 * @param code - Center DIGIPIN code
 * @param radius - Distance in cells (must be >= 1)
 * @returns Array of codes forming the ring at specified radius
 * @throws {Error} If code or radius is invalid
 * @example
 * // Get cells exactly 1 step away (8 immediate neighbors)
 * const ring1 = getRing('39J49LL8T4', 1);
 *
 * // Get cells exactly 2 steps away (outer ring)
 * const ring2 = getRing('39J49LL8T4', 2); // Up to 16 cells
 */
export function getRing(code: string, radius: number): string[];

/**
 * Batch encode multiple coordinate pairs
 * @param coordinates - Array of coordinate objects
 * @param precision - Code length (1-10), default 10
 * @returns Array of DIGIPIN codes
 * @example
 * const coords = [
 *   { lat: 28.6, lon: 77.2 },
 *   { lat: 19.0, lon: 72.8 }
 * ];
 * const codes = batchEncode(coords); // ['39J4...', '25C3...']
 */
export function batchEncode(coordinates: Coordinate[], precision?: number): string[];

/**
 * Batch decode multiple DIGIPIN codes
 * @param codes - Array of DIGIPIN codes
 * @returns Array of coordinate objects
 * @example
 * const codes = ['39J49LL8T4', '25C3...'];
 * const coords = batchDecode(codes);
 * // [{ lat: 28.6..., lon: 77.2... }, { lat: 19.0..., lon: 72.8... }]
 */
export function batchDecode(codes: string[]): Coordinate[];

/**
 * India's bounding box constants
 */
export const INDIA_BOUNDS: IndiaBounds;

/**
 * Valid DIGIPIN alphabet (16 characters)
 */
export const ALPHABET: string;

/**
 * Default export containing all functions
 */
declare const digipin: {
    encode: typeof encode;
    decode: typeof decode;
    isValid: typeof isValid;
    isValidCoordinate: typeof isValidCoordinate;
    getBounds: typeof getBounds;
    getParent: typeof getParent;
    getNeighbors: typeof getNeighbors;
    getDisk: typeof getDisk;
    getRing: typeof getRing;
    batchEncode: typeof batchEncode;
    batchDecode: typeof batchDecode;
    INDIA_BOUNDS: IndiaBounds;
    ALPHABET: string;
};

export default digipin;
