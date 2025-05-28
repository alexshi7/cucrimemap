import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import MarkerClusterGroup from 'react-leaflet-markercluster';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet.markercluster/dist/MarkerCluster.css';
import 'leaflet.markercluster/dist/MarkerCluster.Default.css';

import './App.css'; // For .dot styles

const CrimeMap = ({ dataUrl }) => {
    const [crimes, setCrimes] = useState([]);
    const [locationMap, setLocationMap] = useState({});
    const [aliases, setAliases] = useState({});
    const fallbackCoordinates = [42.447, -76.484]; // Cornell center

    useEffect(() => {
        fetch(dataUrl)
            .then(res => res.json())
            .then(data => setCrimes(data))
            .catch(err => console.error("Failed to load crime data:", err));
    }, [dataUrl]);

    useEffect(() => {
        fetch('/location-map.json')
            .then(res => res.json())
            .then(data => {
                const { aliases: a, ...rest } = data;
                setAliases(a || {});
                setLocationMap(rest);
            })
            .catch(err => console.error("Failed to load location map:", err));
    }, []);

    const normalize = (str) =>
        str.toLowerCase().replace(/[^a-z0-9]/g, '').trim();

    const getCoordinates = (location) => {
        if (!location || !locationMap) return fallbackCoordinates;

        let normLoc = normalize(location);

        // Tokenize to prevent false positive matches like "lynahrink" → "hr"
        const tokens = normLoc.split(/(?=[a-z])(?<=[0-9])|(?=[0-9])(?<=[a-z])/g); // splits letters/numbers

        for (const [aliasRaw, replacementRaw] of Object.entries(aliases)) {
            const alias = normalize(aliasRaw);
            const replacement = normalize(replacementRaw);

            // Only match if alias is an exact token
            if (tokens.includes(alias)) {
                normLoc = replacement;
                break;
            }
        }

        // Exact match
        for (const [locKey, coords] of Object.entries(locationMap)) {
            if (normalize(locKey) === normLoc) {
                return [coords.lat, coords.lng];
            }
        }

        // Fuzzy match
        for (const [locKey, coords] of Object.entries(locationMap)) {
            const normKey = normalize(locKey);
            if (normKey.includes(normLoc) || normLoc.includes(normKey)) {
                return [coords.lat, coords.lng];
            }
        }

        console.warn(`Fallback location used for: "${location}"`);
        return fallbackCoordinates;
    };


    const getStatusColor = (disposition = "") => {
        const status = disposition.toLowerCase();

        if (status.includes("arrest")) return "#d62728";
        if (status.includes("exceptional clearance")) return "#ff7f0e";
        if (status.includes("pending")) return "#1f77b4";
        if (status.includes("closed")) return "#2ca02c";
        if (status.includes("unfounded")) return "#9467bd";

        return "gray";
    };

    const getDotIcon = (disposition) => {
        const color = getStatusColor(disposition);
        return L.divIcon({
            className: 'dot-icon',
            html: `<div class="dot" style="background-color:${color}"></div>`,
            iconSize: [12, 12],
            iconAnchor: [6, 6],
            popupAnchor: [0, -6],
        });
    };

    return (
        <MapContainer center={fallbackCoordinates} zoom={16} style={{ height: '600px', width: '100%' }}>
            <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
            <MarkerClusterGroup>
                {crimes.map((crime, idx) => {
                    const position = getCoordinates(crime.location);
                    return (
                        <Marker key={idx} position={position} icon={getDotIcon(crime.disposition)}>
                            <Popup>
                                <strong>{crime.incidentType}</strong><br />
                                <em>{crime.location}</em><br />
                                {crime.reported}<br />
                                <small>{crime.disposition}</small><br />
                                <p>{crime.narrative}</p>
                            </Popup>
                        </Marker>
                    );
                })}
            </MarkerClusterGroup>
        </MapContainer>
    );
};

export default CrimeMap;
