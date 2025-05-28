import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
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
        str.toLowerCase().replace(/[^\w\s]/gi, '').trim();

    const getCoordinates = (location) => {
        if (!location || !locationMap) return fallbackCoordinates;

        let normLoc = normalize(location);

        // Alias substitution (e.g. "lr" → "Low Rise")
        for (const [alias, replacement] of Object.entries(aliases)) {
            if (normLoc.includes(alias)) {
                normLoc = normLoc.replace(alias, normalize(replacement));
            }
        }

        // Fuzzy match
        const key = Object.keys(locationMap).find(k =>
            normalize(k).includes(normLoc) || normLoc.includes(normalize(k))
        );

        if (key) {
            return [locationMap[key].lat, locationMap[key].lng];
        }

        return fallbackCoordinates;
    };

    const getStatusColor = (disposition = "") => {
        const status = disposition.toLowerCase();

        if (status.includes("arrest")) return "#d62728";               // Red
        if (status.includes("exceptional clearance")) return "#ff7f0e"; // Orange
        if (status.includes("pending")) return "#1f77b4";               // Blue
        if (status.includes("closed")) return "#2ca02c";                // Green
        if (status.includes("unfounded")) return "#9467bd";             // Purple

        return "gray"; // Unknown or fallback
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
        </MapContainer>
    );
};

export default CrimeMap;
