const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs');

const URL = 'https://dailycrimelog.cupolice.cornell.edu/index.cfm';
const LOCATION_MAP = JSON.parse(fs.readFileSync('location-map.json', 'utf-8'));

function normalizeLocation(raw) {
    for (const alias in LOCATION_MAP) {
        if (raw.includes(alias)) return LOCATION_MAP[alias];
    }
    return raw;
}

function parseDate(str) {
    return new Date(str).toISOString(); // for easier comparison
}

(async () => {
    try {
        const { data } = await axios.get(URL);
        const $ = cheerio.load(data);
        const crimeRows = [];

        $('table tr').each((i, row) => {
            const cells = $(row).find('td');
            if (cells.length < 7) return;

            const entry = {
                incidentType: $(cells[0]).text().trim(),
                reportNumber: $(cells[1]).text().trim(),
                reported: $(cells[2]).text().trim(),
                occurred: $(cells[3]).text().trim(),
                location: normalizeLocation($(cells[4]).text().trim()),
                narrative: $(cells[5]).text().trim(),
                disposition: $(cells[6]).text().trim()
            };

            crimeRows.push(entry);
        });

        const allPath = 'all-crimes.json';
        let allCrimes = fs.existsSync(allPath)
            ? JSON.parse(fs.readFileSync(allPath, 'utf-8'))
            : [];

        const reportMap = new Map(allCrimes.map(c => [c.reportNumber, c]));

        // Merge updates
        for (const newCrime of crimeRows) {
            if (reportMap.has(newCrime.reportNumber)) {
                const existing = reportMap.get(newCrime.reportNumber);
                if (existing.disposition !== newCrime.disposition) {
                    existing.disposition = newCrime.disposition; // Update status
                }
            } else {
                allCrimes.push(newCrime); // New entry
            }
        }

        // Write all crimes
        fs.writeFileSync(allPath, JSON.stringify(allCrimes, null, 2));

        // Write recent crimes
        const sixtyDaysAgo = Date.now() - 1000 * 60 * 60 * 24 * 60;
        const recent = allCrimes.filter(c => new Date(c.reported) > sixtyDaysAgo);
        fs.writeFileSync('recent-crimes.json', JSON.stringify(recent, null, 2));

        console.log(`✅ Scraped ${crimeRows.length} today | ${allCrimes.length} total stored`);
    } catch (err) {
        console.error('❌ Error scraping:', err.message);
    }
})();
