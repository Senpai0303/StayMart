/**
 * StayMart Marketplace Statistics & Creative Visuals Engine
 * Milestone 2 - Features 8, 9, 10, 11, 13
 * 
 * Includes:
 * 1. IntersectionObserver Animated Metric Counters (Feature 8)
 * 2. Interactive Dual-Mode Student Savings Calculator (Feature 9)
 * 3. StayMartAccommodationStats Engine (Features 9, 10, 11, 13)
 * 4. RecommerceVisuals Deterministic Analytics Engine (Features 9, 11, 13)
 */

(function () {
  'use strict';

  /* ==========================================================================
     1. Animated Metric Counters (Feature 8)
     ========================================================================== */
  function initMetricCounters() {
    const counterElements = document.querySelectorAll('[data-counter]');
    if (!counterElements.length) return;

    if (!('IntersectionObserver' in window)) {
      // Fallback for browsers without IntersectionObserver
      return;
    }

    const observer = new IntersectionObserver((entries, obs) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          animateCounter(entry.target);
          obs.unobserve(entry.target);
        }
      });
    }, {
      root: null,
      threshold: 0.2,
      rootMargin: '0px 0px -30px 0px'
    });

    counterElements.forEach(el => observer.observe(el));
  }

  function animateCounter(el) {
    const target = parseFloat(el.getAttribute('data-target')) || 0;
    const prefix = el.getAttribute('data-prefix') || '';
    const suffix = el.getAttribute('data-suffix') || '';
    const duration = 1800; // 1.8 seconds smooth deceleration
    const startTime = performance.now();

    // High performance exponential deceleration (easeOutExpo)
    function easeOutExpo(t) {
      return t === 1 ? 1 : 1 - Math.pow(2, -10 * t);
    }

    function frame(now) {
      const elapsed = now - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const easedProgress = easeOutExpo(progress);
      const current = Math.round(target * easedProgress);

      el.textContent = `${prefix}${current.toLocaleString('en-IN')}${suffix}`;

      if (progress < 1) {
        requestAnimationFrame(frame);
      } else {
        el.textContent = `${prefix}${target.toLocaleString('en-IN')}${suffix}`;
      }
    }

    requestAnimationFrame(frame);
  }

  /* ==========================================================================
     2. Interactive Dual-Mode Student Savings Calculator (Feature 9)
     ========================================================================== */
  const calcState = {
    mode: 'accommodation', // 'accommodation' | 'gear'
    monthlyRent: 9000,
    durationMonths: 10,
    includeMeals: true,
    includeUtilities: true,
    selectedPackage: 'books'
  };

  const gearPackages = {
    books: { retail: 6500, senior: 1800, co2: 12, label: 'Textbooks & GATE Notes' },
    laptop: { retail: 56000, senior: 24500, co2: 185, label: 'Engineering Coding Setup' },
    room: { retail: 14500, senior: 4800, co2: 45, label: 'Room Setup & Cooler' },
    mobility: { retail: 12000, senior: 4200, co2: 80, label: 'Campus Cycle Commute' }
  };

  function switchCalcMode(mode) {
    calcState.mode = mode;
    const accBtn = document.getElementById('calcModeAccBtn');
    const gearBtn = document.getElementById('calcModeGearBtn');
    const accPane = document.getElementById('calcPaneAccommodation');
    const gearPane = document.getElementById('calcPaneGear');

    if (mode === 'accommodation') {
      if (accBtn) { accBtn.classList.add('active'); accBtn.setAttribute('aria-selected', 'true'); }
      if (gearBtn) { gearBtn.classList.remove('active'); gearBtn.setAttribute('aria-selected', 'false'); }
      if (accPane) { accPane.classList.add('active'); accPane.style.display = 'block'; }
      if (gearPane) { gearPane.classList.remove('active'); gearPane.style.display = 'none'; }
      updateAccommodationCalc();
    } else {
      if (accBtn) { accBtn.classList.remove('active'); accBtn.setAttribute('aria-selected', 'false'); }
      if (gearBtn) { gearBtn.classList.add('active'); gearBtn.setAttribute('aria-selected', 'true'); }
      if (accPane) { accPane.classList.remove('active'); accPane.style.display = 'none'; }
      if (gearPane) { gearPane.classList.add('active'); gearPane.style.display = 'block'; }
      updateGearCalc();
    }
  }

  function updateAccommodationCalc() {
    const slider = document.getElementById('calcRentSlider');
    if (slider) {
      calcState.monthlyRent = parseInt(slider.value, 10);
      const disp = document.getElementById('calcRentDisplay');
      if (disp) disp.textContent = `₹${calcState.monthlyRent.toLocaleString('en-IN')} / month`;
    }

    const mealsCheck = document.getElementById('calcIncludeMeals');
    calcState.includeMeals = mealsCheck ? mealsCheck.checked : true;

    const utilCheck = document.getElementById('calcIncludeUtilities');
    calcState.includeUtilities = utilCheck ? utilCheck.checked : true;

    // Financial formulation
    const brokerageSaved = calcState.monthlyRent; // 1 month full brokerage avoided
    const utilitySavings = calcState.includeUtilities ? (1200 * calcState.durationMonths) : 0;
    const mealSavings = calcState.includeMeals ? (2500 * calcState.durationMonths) : 0;
    const totalSavings = brokerageSaved + utilitySavings; // Direct zero-brokerage + bundled utilities

    // Update UI elements
    const totalEl = document.getElementById('calcAccTotalSavings');
    if (totalEl) totalEl.textContent = `₹${totalSavings.toLocaleString('en-IN')}`;

    const cbBrokerage = document.getElementById('cbBrokerageVal');
    if (cbBrokerage) cbBrokerage.textContent = `+₹${brokerageSaved.toLocaleString('en-IN')}`;

    const cbUtility = document.getElementById('cbUtilityVal');
    if (cbUtility) cbUtility.textContent = `+₹${utilitySavings.toLocaleString('en-IN')}`;

    const mealRow = document.getElementById('cbMealRow');
    const cbMeal = document.getElementById('cbMealVal');
    if (mealRow && cbMeal) {
      if (calcState.includeMeals) {
        mealRow.style.display = 'flex';
        cbMeal.textContent = `+₹${mealSavings.toLocaleString('en-IN')}`;
      } else {
        mealRow.style.display = 'none';
      }
    }

    // Comparison Bar
    const brokerTotal = (calcState.monthlyRent * calcState.durationMonths) + brokerageSaved + (calcState.includeUtilities ? utilitySavings : 0);
    const staymartTotal = calcState.monthlyRent * calcState.durationMonths;
    const brokerEl = document.getElementById('cbBrokerCost');
    const staymartEl = document.getElementById('cbStaymartCost');
    const barFill = document.getElementById('cbSavingsBar');

    if (brokerEl) brokerEl.textContent = `₹${brokerTotal.toLocaleString('en-IN')}`;
    if (staymartEl) staymartEl.textContent = `₹${staymartTotal.toLocaleString('en-IN')}`;
    if (barFill && brokerTotal > 0) {
      const pct = Math.round((staymartTotal / brokerTotal) * 100);
      barFill.style.width = `${Math.min(pct, 100)}%`;
    }

    // Dynamic CTA link
    const cta = document.getElementById('calcAccCta');
    if (cta) {
      cta.href = `search-properties.html?maxPrice=${calcState.monthlyRent}`;
    }
  }

  function setRentPreset(amount) {
    const slider = document.getElementById('calcRentSlider');
    if (slider) {
      slider.value = amount;
      document.querySelectorAll('.calc-chip').forEach(c => {
        c.classList.toggle('active', c.textContent.includes(amount.toLocaleString('en-IN')));
      });
      updateAccommodationCalc();
    }
  }

  function setDurationPreset(months) {
    calcState.durationMonths = months;
    document.querySelectorAll('#stayDurationPills .calc-pill').forEach(pill => {
      pill.classList.toggle('active', parseInt(pill.getAttribute('data-months'), 10) === months);
    });
    updateAccommodationCalc();
  }

  function selectGearPackage(pkgKey, cardEl) {
    calcState.selectedPackage = pkgKey;
    document.querySelectorAll('.package-card').forEach(c => c.classList.remove('active'));
    if (cardEl) {
      cardEl.classList.add('active');
    } else {
      const matching = document.querySelector(`.package-card[onclick*="'${pkgKey}'"]`);
      if (matching) matching.classList.add('active');
    }

    const pkg = gearPackages[pkgKey];
    if (!pkg) return;

    const retailEl = document.getElementById('calcGearRetail');
    const seniorEl = document.getElementById('calcGearSenior');
    const savingsEl = document.getElementById('calcGearSavings');
    const pctEl = document.getElementById('calcGearPercent');
    const co2El = document.getElementById('calcGearCo2');
    const cta = document.getElementById('calcGearCta');

    const saved = pkg.retail - pkg.senior;
    const pct = Math.round((saved / pkg.retail) * 100);

    if (retailEl) retailEl.textContent = `₹${pkg.retail.toLocaleString('en-IN')}`;
    if (seniorEl) seniorEl.textContent = `₹${pkg.senior.toLocaleString('en-IN')}`;
    if (savingsEl) savingsEl.textContent = `₹${saved.toLocaleString('en-IN')}`;
    if (pctEl) pctEl.textContent = `${pct}%`;
    if (co2El) co2El.textContent = `${pkg.co2} kg`;

    if (cta) {
      const catMap = {
        books: 'Books%20%26%20Stationery',
        laptop: 'Electronics',
        room: 'Furniture',
        mobility: 'Vehicles'
      };
      cta.href = `search-products.html?category=${catMap[pkgKey] || ''}`;
    }
  }

  function updateCustomGearCalc() {
    let totalRetail = 0;
    let totalSenior = 0;
    let totalCo2 = 0;

    const checks = document.querySelectorAll('#gearChecklist input[type="checkbox"]:checked');
    checks.forEach(chk => {
      totalRetail += parseFloat(chk.getAttribute('data-retail')) || 0;
      totalSenior += parseFloat(chk.getAttribute('data-senior')) || 0;
      totalCo2 += parseFloat(chk.getAttribute('data-co2')) || 0;
    });

    const retailEl = document.getElementById('calcGearRetail');
    const seniorEl = document.getElementById('calcGearSenior');
    const savingsEl = document.getElementById('calcGearSavings');
    const pctEl = document.getElementById('calcGearPercent');
    const co2El = document.getElementById('calcGearCo2');

    const saved = totalRetail - totalSenior;
    const pct = totalRetail > 0 ? Math.round((saved / totalRetail) * 100) : 0;

    if (retailEl) retailEl.textContent = `₹${totalRetail.toLocaleString('en-IN')}`;
    if (seniorEl) seniorEl.textContent = `₹${totalSenior.toLocaleString('en-IN')}`;
    if (savingsEl) savingsEl.textContent = `₹${saved.toLocaleString('en-IN')}`;
    if (pctEl) pctEl.textContent = `${pct}%`;
    if (co2El) co2El.textContent = `${totalCo2} kg`;
  }

  function updateGearCalc() {
    selectGearPackage(calcState.selectedPackage, document.querySelector(`.package-card[onclick*="'${calcState.selectedPackage}'"]`));
  }

  // Export functions to global scope
  window.switchCalcMode = switchCalcMode;
  window.updateAccommodationCalc = updateAccommodationCalc;
  window.setRentPreset = setRentPreset;
  window.setDurationPreset = setDurationPreset;
  window.selectGearPackage = selectGearPackage;
  window.updateCustomGearCalc = updateCustomGearCalc;

  /* ==========================================================================
     3. StayMartAccommodationStats Engine (Features 9, 10, 11, 13)
     ========================================================================== */
  const CAMPUS_ZONE_BENCHMARKS = {
    GRAPHIC_ERA: {
      zoneName: 'Graphic Era University Hub (Clement Town / Subhash Nagar)',
      shortName: 'Graphic Era',
      medianRentPG: 7500,
      medianRentFlat: 11000,
      medianRentRoom: 5200,
      keywords: ['clement town', 'graphic era', 'geu', 'gehu', 'subhash nagar', 'bell road']
    },
    UPES: {
      zoneName: 'UPES University Hub (Premnagar / Bidholi / Kandoli)',
      shortName: 'UPES Premnagar',
      medianRentPG: 8400,
      medianRentFlat: 13000,
      medianRentRoom: 5500,
      keywords: ['upes', 'premnagar', 'bidholi', 'kandoli', 'manduwala']
    },
    DIT: {
      zoneName: 'DIT University Hub (Mussoorie Diversion / Rajpur Road)',
      shortName: 'DIT Rajpur Rd',
      medianRentPG: 8200,
      medianRentFlat: 13500,
      medianRentRoom: 6000,
      keywords: ['dit', 'makkawala', 'mussoorie diversion', 'salan gaon']
    },
    DOON_UNIV: {
      zoneName: 'Doon University Hub (Mothrowala / Kedarpur)',
      shortName: 'Doon Univ',
      medianRentPG: 6500,
      medianRentFlat: 10000,
      medianRentRoom: 4800,
      keywords: ['doon university', 'mothrowala', 'kedarpur', 'defence colony']
    },
    IIT_ROORKEE: {
      zoneName: 'IIT Roorkee Hub (Civil Lines)',
      shortName: 'IIT Roorkee',
      medianRentPG: 6000,
      medianRentFlat: 9500,
      medianRentRoom: 4200,
      keywords: ['roorkee', 'civil lines', 'iit']
    },
    RISHIKESH: {
      zoneName: 'Rishikesh Co-Living Hub (Tapovan / Laxman Jhula)',
      shortName: 'Tapovan Rishikesh',
      medianRentPG: 5800,
      medianRentFlat: 11000,
      medianRentRoom: 5000,
      keywords: ['tapovan', 'rishikesh', 'laxman jhula', 'aiims']
    },
    DEHRADUN_GENERAL: {
      zoneName: 'Central Dehradun Hub (ISBT / Patel Nagar / Ballupur)',
      shortName: 'Dehradun Hub',
      medianRentPG: 7000,
      medianRentFlat: 12000,
      medianRentRoom: 5000,
      keywords: ['ballupur', 'isbt', 'patel nagar', 'rajpur road', 'jakhan', 'clock tower']
    }
  };

  const StayMartAccommodationStats = {
    benchmarks: CAMPUS_ZONE_BENCHMARKS,

    matchCampusZone: function (area, address, title) {
      const text = `${area || ''} ${address || ''} ${title || ''}`.toLowerCase();
      for (const key of Object.keys(CAMPUS_ZONE_BENCHMARKS)) {
        const zone = CAMPUS_ZONE_BENCHMARKS[key];
        if (zone.keywords.some(k => text.includes(k))) {
          return zone;
        }
      }
      return CAMPUS_ZONE_BENCHMARKS.DEHRADUN_GENERAL;
    },

    getOccupancy: function (property) {
      const total = Math.max(1, Number(property.totalRooms) || 1);
      const isAvail = property.isAvailable !== false;
      const available = isAvail
        ? (property.availableRooms !== undefined && property.availableRooms !== null
            ? Math.min(total, Math.max(0, Number(property.availableRooms)))
            : Math.ceil(total * 0.4))
        : 0;
      const occupied = Math.max(0, total - available);
      const rate = Math.round((occupied / total) * 100);
      const availRate = 100 - rate;

      let status = 'AMPLE';
      let badgeText = 'Immediate Move-In';
      let detailHeadline = 'Immediate Move-In Available';

      if (!isAvail || available === 0) {
        status = 'FULL';
        badgeText = 'Fully Occupied';
        detailHeadline = 'Fully Booked for Semester';
      } else if (available <= 2 || availRate <= 35) {
        status = 'LIMITED';
        badgeText = `Filling Fast (${available} Left)`;
        detailHeadline = `Filling Fast — Only ${available} ${available === 1 ? 'Bed' : 'Beds'} Left`;
      }

      return { total, available, occupied, rate, status, badgeText, detailHeadline };
    },

    getSavings: function (property) {
      const price = Number(property.pricePerMonth) || 0;
      const brokerage = price; // 1 full month brokerage saved on direct owner/senior listing
      const zone = this.matchCampusZone(property.area, property.address, property.title);

      let median = zone.medianRentPG;
      if (property.type === 'FLAT') median = zone.medianRentFlat;
      else if (property.type === 'ROOM') median = zone.medianRentRoom;

      const diff = median - price;
      const percentage = Math.round((diff / median) * 100);
      const annualTotal = (Math.max(0, diff) * 10) + brokerage;

      return {
        brokerage,
        zoneName: zone.zoneName,
        zoneShort: zone.shortName,
        zoneMedian: median,
        diff,
        percentage,
        annualTotal
      };
    },

    getPriceTrend: function (property) {
      const price = Number(property.pricePerMonth) || 0;
      const savings = this.getSavings(property);
      const zoneMedian = savings.zoneMedian;

      const minRent = Math.round(zoneMedian * 0.5);
      const maxRent = Math.round(zoneMedian * 1.6);
      const needlePct = Math.min(96, Math.max(4, Math.round(((price - minRent) / (maxRent - minRent)) * 100)));

      let verdictClass = 'fair';
      let verdictBadge = '⚖️ Fair Campus Market Value';
      let verdictNote = 'Normal campus rate';
      let score = 8.5;

      if (price < zoneMedian * 0.85) {
        verdictClass = 'budget';
        verdictBadge = '🌿 Budget-Friendly Deal';
        verdictNote = `${Math.abs(Math.round(((zoneMedian - price) / zoneMedian) * 100))}% below campus avg`;
        score = 9.4;
      } else if (price > zoneMedian * 1.15) {
        verdictClass = 'premium';
        verdictBadge = '👑 Premium Co-Living';
        verdictNote = 'Luxury student studio';
        score = 8.8;
      }

      return {
        needlePct,
        verdictClass,
        verdictBadge,
        verdictNote,
        studentValueScore: score,
        zoneMedian,
        zoneName: savings.zoneName,
        zoneShort: savings.zoneShort,
        cityAverage: 7400
      };
    },

    getEngagement: function (propertyId) {
      const seed = Number(propertyId) || 1;
      const viewsThisWeek = 22 + ((seed * 19) % 47);
      const inquiriesToday = 1 + ((seed * 7) % 6);
      const shortlistsCount = 6 + ((seed * 13) % 29);
      const responseMins = (8 + ((seed * 5) % 17)) <= 12 ? 'Under 15 mins' : 'Under 30 mins';

      return {
        viewsThisWeek,
        inquiriesToday,
        shortlistsCount,
        responseMins
      };
    }
  };

  window.StayMartAccommodationStats = StayMartAccommodationStats;

  /* ==========================================================================
     4. RecommerceVisuals Deterministic Analytics Engine (Features 9, 11, 13)
     ========================================================================== */
  const RECOMMERCE_CATEGORY_MEDIANS = {
    10: { name: 'Books & Stationery', median: 1850, mult: 2.85 },
    7:  { name: 'Electronics',        median: 38000, mult: 1.85 },
    8:  { name: 'Mobiles & Tablets',  median: 22500, mult: 1.90 },
    9:  { name: 'Furniture',          median: 14000, mult: 2.25 },
    11: { name: 'Appliances',         median: 9500, mult: 2.10 },
    12: { name: 'Vehicles',           median: 58000, mult: 1.65 },
    13: { name: 'Sports & Fitness',   median: 3500, mult: 2.20 },
    14: { name: 'Home & Kitchen',     median: 2800, mult: 2.15 },
    15: { name: 'Fashion & Clothing', median: 2200, mult: 2.70 },
    16: { name: 'Others',             median: 4500, mult: 1.95 }
  };

  const RecommerceVisuals = {
    getProductSeed: function (id) {
      const num = Number(id) || 1;
      return ((num * 9301 + 49297) % 233280) / 233280;
    },

    getAnalytics: function (product) {
      const price = Math.max(1, Number(product.price) || 0);
      const catId = (product.category && product.category.id) ? Number(product.category.id) : 16;
      const catConfig = RECOMMERCE_CATEGORY_MEDIANS[catId] || { median: 4500, mult: 2.0 };
      const seed = this.getProductSeed(product.id);
      const titleLower = String(product.title || '').toLowerCase();

      // Bespoke item multipliers based on authentic student items
      let multiplier = catConfig.mult;
      if (titleLower.includes('calculator') || titleLower.includes('fx-991')) {
        multiplier = 2.6;
      } else if (titleLower.includes('cycle') || titleLower.includes('bicycle')) {
        multiplier = 2.4;
      } else if (titleLower.includes('cooler') || titleLower.includes('symphony')) {
        multiplier = 2.2;
      } else if (titleLower.includes('drafter') || titleLower.includes('gate') || titleLower.includes('book')) {
        multiplier = 2.9;
      } else if (titleLower.includes('laptop') || titleLower.includes('thinkpad') || titleLower.includes('macbook')) {
        multiplier = 1.95;
      }

      // Condition modifier
      const cond = String(product.condition || 'GOOD').toUpperCase();
      let condScore = 7;
      let condLabel = 'Good Condition';
      let condTier = 'good';
      let condPct = 70;

      if (cond === 'NEW') {
        condScore = 10;
        condLabel = 'Brand New (Sealed)';
        condTier = 'new';
        condPct = 100;
        multiplier = Math.max(1.25, multiplier * 0.7);
      } else if (cond === 'LIKE_NEW') {
        condScore = 9;
        condLabel = 'Like New (Mint)';
        condTier = 'like-new';
        condPct = 90;
        multiplier = Math.max(1.5, multiplier * 0.85);
      } else if (cond === 'GOOD') {
        condScore = 7;
        condLabel = 'Good Condition';
        condTier = 'good';
        condPct = 70;
      } else if (cond === 'FAIR') {
        condScore = 5;
        condLabel = 'Fair / Functional';
        condTier = 'fair';
        condPct = 50;
        multiplier = multiplier * 1.15;
      } else if (cond === 'OLD') {
        condScore = 3;
        condLabel = 'Budget / Vintage';
        condTier = 'old';
        condPct = 30;
        multiplier = multiplier * 1.3;
      }

      // Raw retail price calculation
      let rawRetail = Math.round(price * multiplier);
      if (rawRetail <= price) rawRetail = Math.round(price * 1.6);

      // Clean consumer price endings (e.g. ₹2,499, ₹12,990)
      let retailPrice = rawRetail;
      if (rawRetail > 10000) {
        retailPrice = Math.round(rawRetail / 500) * 500 - 10; // Ends in 990 or 490
      } else if (rawRetail > 1000) {
        retailPrice = Math.round(rawRetail / 100) * 100 - 1; // Ends in 99
      } else {
        retailPrice = Math.round(rawRetail / 50) * 50 - 10; // Ends in 90 or 40
      }
      if (retailPrice <= price) retailPrice = Math.round(price * 1.4);

      const savingsAmount = retailPrice - price;
      const savingsPercent = Math.max(15, Math.min(85, Math.round((savingsAmount / retailPrice) * 100)));

      // Deal Quality Tiers
      let dealClass = 'fair';
      let dealBadge = '⚖️ Fair Campus Value';
      if (price >= 25000) {
        dealClass = 'premium';
        dealBadge = '⭐ High-Spec Gear';
      } else if (savingsPercent >= 60 || price <= catConfig.median * 0.65) {
        dealClass = 'steal';
        dealBadge = '🔥 Budget Steal';
      } else if (savingsPercent >= 42) {
        dealClass = 'great';
        dealBadge = '💎 Great Student Deal';
      }

      // Social proof & engagement stats
      const baseViews = product.viewsCount || (25 + Math.round(seed * 45));
      const savedCount = Math.max(3, Math.round(baseViews * 0.15) + (Number(product.id) % 9));
      const viewsLast24h = Math.max(12, Math.round(baseViews * 0.4) + ((Number(product.id) * 3) % 21));

      // Campus affiliation
      const locText = `${product.area || ''} ${(product.location && product.location.city) || ''}`.toLowerCase();
      let campusAffiliation = "Graphic Era (GEU '25)";
      if (locText.includes('premnagar') || locText.includes('bidholi') || locText.includes('upes')) {
        campusAffiliation = "UPES Dehradun ('24)";
      } else if (locText.includes('rajpur') || locText.includes('dit')) {
        campusAffiliation = "DIT University ('25)";
      } else if (locText.includes('roorkee')) {
        campusAffiliation = "IIT Roorkee ('25)";
      } else if (locText.includes('doon') || locText.includes('kedarpur')) {
        campusAffiliation = "Doon University ('24)";
      }

      const responseTime = seed > 0.55 ? 'Under 15 mins' : (seed > 0.25 ? 'Under 30 mins' : 'Under 1 hour');

      return {
        price,
        retailPrice,
        savingsAmount,
        savingsPercent,
        dealClass,
        dealBadge,
        categoryMedian: catConfig.median,
        categoryName: catConfig.name,
        condScore,
        condLabel,
        condTier,
        condPct,
        savedCount,
        viewsLast24h,
        campusAffiliation,
        responseTime
      };
    }
  };

  window.RecommerceVisuals = RecommerceVisuals;

  /* ==========================================================================
     DOM Ready Auto-Initialization
     ========================================================================== */
  document.addEventListener('DOMContentLoaded', () => {
    initMetricCounters();
    if (document.getElementById('calcRentSlider')) {
      updateAccommodationCalc();
    }
  });

})();
