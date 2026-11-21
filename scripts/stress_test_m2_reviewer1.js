/**
 * Adversarial Edge-Case Stress Testing for Milestone 2 Analytics & Logic Engines
 */

const fs = require('fs');
const path = require('path');

// Extract engines from stats.js into a sandboxed environment
const statsCode = fs.readFileSync(path.join(__dirname, '..', 'frontend', 'js', 'stats.js'), 'utf8');

// Mock window and document
const windowMock = {};
const documentMock = {
  querySelectorAll: () => [],
  getElementById: () => null,
  addEventListener: () => {}
};

const fn = new Function('window', 'document', 'performance', 'requestAnimationFrame', statsCode);
fn(windowMock, documentMock, { now: () => 0 }, () => {});

const { StayMartAccommodationStats, RecommerceVisuals } = windowMock;

console.log('===============================================================');
console.log('ADVERSARIAL STRESS-TESTING: EDGE CASES & BOUNDARY CONDITIONS');
console.log('===============================================================');

let passed = 0;
let failed = 0;

function assert(condition, desc) {
  if (condition) {
    console.log(`[PASS] ${desc}`);
    passed++;
  } else {
    console.error(`[FAIL] ${desc}`);
    failed++;
  }
}

// 1. Edge Case: Empty or Null Property
try {
  const occEmpty = StayMartAccommodationStats.getOccupancy({});
  assert(occEmpty.total === 1 && occEmpty.available >= 0 && occEmpty.rate >= 0, 'Empty property handles zero rooms gracefully');
} catch (e) {
  assert(false, 'Empty property throws error: ' + e.message);
}

// 2. Edge Case: Negative Rooms and Available Rooms > Total Rooms
try {
  const occNegative = StayMartAccommodationStats.getOccupancy({ totalRooms: -5, availableRooms: 10 });
  assert(occNegative.total === 1 && occNegative.available === 1, 'Negative total rooms clamped to at least 1, available rooms clamped to total');
} catch (e) {
  assert(false, 'Negative rooms throws error: ' + e.message);
}

// 3. Edge Case: Property Marked Unavailable
try {
  const occUnavailable = StayMartAccommodationStats.getOccupancy({ totalRooms: 5, availableRooms: 3, isAvailable: false });
  assert(occUnavailable.status === 'FULL' && occUnavailable.available === 0 && occUnavailable.badgeText.includes('Occupied'), 'isAvailable=false correctly forces status FULL with 0 available');
} catch (e) {
  assert(false, 'Unavailable property throws error: ' + e.message);
}

// 4. Edge Case: Unknown Location Zone Fallback
try {
  const zoneFallback = StayMartAccommodationStats.matchCampusZone('Unknown Village', 'Far away road', 'Random House');
  assert(zoneFallback.shortName === 'Dehradun Hub' && zoneFallback.medianRentPG === 7000, 'Unknown location safely defaults to DEHRADUN_GENERAL benchmark');
} catch (e) {
  assert(false, 'Unknown location throws error: ' + e.message);
}

// 5. Edge Case: Zero Rent Property
try {
  const zeroSavings = StayMartAccommodationStats.getSavings({ pricePerMonth: 0, area: 'Clement Town' });
  assert(zeroSavings.diff > 0 && zeroSavings.percentage === 100, 'Zero rent calculates valid savings diff and 100% discount against median');
} catch (e) {
  assert(false, 'Zero rent throws error: ' + e.message);
}

// 6. Edge Case: Extreme High Rent (Luxury Property Above Median)
try {
  const highRent = StayMartAccommodationStats.getPriceTrend({ pricePerMonth: 30000, area: 'Prem Nagar', type: 'PG' });
  assert(highRent.needlePct === 96 && highRent.verdictClass === 'premium', 'Excessive rent clamps needlePct to max 96% and classifies as premium');
} catch (e) {
  assert(false, 'High rent throws error: ' + e.message);
}

// 7. Edge Case: Extreme Low Rent (Below Min Benchmark)
try {
  const lowRent = StayMartAccommodationStats.getPriceTrend({ pricePerMonth: 1000, area: 'Prem Nagar', type: 'PG' });
  assert(lowRent.needlePct === 4 && lowRent.verdictClass === 'budget', 'Extreme low rent clamps needlePct to min 4% and classifies as budget');
} catch (e) {
  assert(false, 'Low rent throws error: ' + e.message);
}

// 8. Edge Case: Product with Price = 0 or Negative Price
try {
  const zeroProduct = RecommerceVisuals.getAnalytics({ id: 99, price: 0, title: 'Old Notes' });
  assert(zeroProduct.price === 1 && zeroProduct.retailPrice > 1 && zeroProduct.savingsAmount > 0, 'Zero product price clamped to 1 and generates authentic retail benchmark');
} catch (e) {
  assert(false, 'Zero product price throws error: ' + e.message);
}

// 9. Edge Case: Unknown Product Category and Lowercase Condition
try {
  const customProd = RecommerceVisuals.getAnalytics({ id: 101, price: 3500, category: { id: 999 }, condition: 'new', title: 'Casio fx-991EX Scientific Calculator' });
  assert(customProd.condScore === 10 && customProd.condTier === 'new' && customProd.categoryMedian === 4500, 'Case-insensitive condition parsing and fallback category config work seamlessly');
} catch (e) {
  assert(false, 'Custom product throws error: ' + e.message);
}

// 10. Edge Case: Retail Price Formatting Endings
try {
  const prodA = RecommerceVisuals.getAnalytics({ id: 5, price: 800, title: 'Drafting Kit' });
  const prodB = RecommerceVisuals.getAnalytics({ id: 6, price: 2500, title: 'Study Chair' });
  const prodC = RecommerceVisuals.getAnalytics({ id: 7, price: 32000, title: 'MacBook Air M1' });
  assert(prodA.retailPrice > prodA.price && prodB.retailPrice > prodB.price && prodC.retailPrice > prodC.price, 'Retail price consistently stays strictly greater than student selling price');
} catch (e) {
  assert(false, 'Retail price comparison throws error: ' + e.message);
}

console.log(`\nAdversarial Results: ${passed} passed, ${failed} failed`);
process.exit(failed > 0 ? 1 : 0);
